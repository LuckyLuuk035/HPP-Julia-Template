all: julia

ifeq ($(UNAME), Darwin)
    LDFLAGS = -L/opt/homebrew/opt/libomp/lib -lomp
endif

ffmpeg:
	@echo "Ervan uitgaande dat ffmpeg lokaal is geïnstalleerd."

%.o: %.cc %.h consts.h
	g++ -O2 $(LDFLAGS) -c -o $@ $<

julia: main.cc frame.o animation.o consts.h
	mpic++ -O2 $(LDFLAGS) -o julia main.cc frame.o animation.o --std=c++23

run: ffmpeg julia
	mpiexec -n $(or $(NP),4) ./julia.exe

help:
	@echo "Use \`make\` to build and \`make run\` to execute on 4 processes (default). Use \`make run NP=2\` to choose the number of processes."

clean:
	rm *.o julia