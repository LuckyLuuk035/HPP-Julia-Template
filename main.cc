#include <cmath>
#include <complex>
#include <numbers>
#include <ostream>
#include <omp.h>
#include <iostream>
#include <mpi.h>

#include "consts.h"
#include "frame.h"
#include "animation.h"

#define cimg_display 0        // No window plz
#include "CImg.h"

using std::cout, std::endl;
using namespace std::literals::complex_literals;

// Colour based on ratio between number of iterations and MAX_ITER
inline constexpr pixel COLOURISE(double iter) { 
  iter = fmod(4 - iter * 5 / MAX_ITER, 6);
  byte x = static_cast<byte>(255 * (1 - std::abs(fmod(iter, 2) - 1)));
  byte r, g, b;

  if      (             iter < 1) { r = 255; g =   x; b =   0; }
  else if (iter >= 1 && iter < 2) { r =   x; g = 255; b =   0; }
  else if (iter >= 2 && iter < 3) { r =   0; g = 255; b =   x; }
  else if (iter >= 3 && iter < 4) { r =   0; g =   x; b = 255; }
  else if (iter >= 4 && iter < 5) { r =   x; g =   0; b = 255; }
  else                            { r = 255; g =   0; b =   x; }
  return { r, g, b };
}

void renderFrame(animation &frames, unsigned int t, unsigned int offset) {
  // constante
  double a = 2 * std::numbers::pi * t / CYCLE_FRAMES;
  double r = 0.7885;
  std::complex<double> c = r * cos(a) + static_cast<std::complex<double>>(1i) * r * sin(a);

  double x_y_range = 2;

  //double scale = 1.5 - 1.45 * t / FRAMES;                           // iets simpeler
  double scale = 1.5 - 1.45 * log(1 + 9.0 * t / FRAMES) / log(10);    // iets interessanter om naar te kijken

  // Loop over elke pixel.
  #pragma omp parallel for collapse(2)
  for (unsigned int x = 0; x < WIDTH; x++) {
    for (unsigned int y = 0; y < HEIGHT; y++){
      // Bepaal startwaarde z
      std::complex<double> z = 2 * x_y_range * std::complex(static_cast<double>(x)/WIDTH, static_cast<double>(y)/HEIGHT) - std::complex(x_y_range*3/4, x_y_range);
      z *= scale;
      unsigned int iter = 0;
      // Gebruiken abs(z) aangezien het getal tussen de 0 en 2 moet zitten ipv alleen lager dan 2.
      while (std::abs(z) < x_y_range && iter < MAX_ITER) {
        z = z*z + c;
        iter++;
      }
      // Kleur wordt bepaald aan de hand van onderstaande check.
      pixel colour = (iter == MAX_ITER) ? pixel{0, 0, 0} : COLOURISE(iter); // als iter = MAX_ITER, kleur is zwart anders -> COLOURISE iter 
      frames[t - offset].set_colour(x, y, colour);
    }
  }


}

int main (int argc, char *argv[]) {
  // Variabelen aanmaken
  int id = -1, numProcesses = -1;
  unsigned int start = 0, stop = 0;

  MPI_Init(&argc, &argv);

  MPI_Comm_rank(MPI_COMM_WORLD, &id);
  MPI_Comm_size(MPI_COMM_WORLD, &numProcesses);

  // Needed to send frames over MPI
  MPI_Datatype mpi_img;
  MPI_Type_contiguous(FRAME_SIZE, MPI_BYTE, &mpi_img);
  MPI_Type_commit(&mpi_img);

  // Aangezien het 750 frames zijn blijven deze exact deelbaar door het aantal processes.
  start = id * (FRAMES / numProcesses);
  stop = (id + 1) * (FRAMES / numProcesses);
  unsigned chunksize = stop - start;
  
  // Aangepast naar local frames met chunksize
  animation local_frames(chunksize);

  for (unsigned int f = start; f < stop; f++) {
    // cout << endl << "Rendering frame " << f << endl;
    cout << id << "Rendering frame " << f << endl;
    renderFrame(local_frames, f, start); // Start is de offset om bij renderFrame de correcte lokale index te hebben
  }

  // De eerste batch verzameld alle frames en maakt de animatie.
  // Dit is basicly het bakje waar de data uit andere processen in komen te vallen.
  animation frames;
  if (id == 0) frames.initialise(FRAMES);

  MPI_Gather(
    local_frames.data(), chunksize, mpi_img,  // start adress, aantal elementen en datatype
    frames.data(), chunksize, mpi_img,        // ontvangend adress, aantal elementen en datatype
    0, MPI_COMM_WORLD                         // root en communicator
  );


  // alleen in eerste chunck de video opslaan.
  if (id == 0) {
    cimg_library::CImg<byte> img(WIDTH,HEIGHT,FRAMES,3);
    cimg_forXYZ(img, x, y, z) { 
      img(x,y,z,RED) = (frames)[z].get_channel(x,y,RED);
      img(x,y,z,GREEN) = (frames)[z].get_channel(x,y,GREEN);
      img(x,y,z,BLUE) = (frames)[z].get_channel(x,y,BLUE);
    }

    std::string filename = std::string("animation.avi");
    img.save_video(filename.c_str());
  }

  // Also needed to send frames over MPI
  MPI_Type_free(&mpi_img);
  MPI_Finalize();
}
