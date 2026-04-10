import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from networkx.algorithms.efficiency_measures import efficiency

df = pd.read_excel('timing_data.xlsx')

df_openmp = df[df['OpenMP'] == True]
df_no_openmp = df[df['OpenMP'] == False]

# Video opslaan tijd zone
v_openmp = df.iloc[0::2]
v_no_openmp = df.iloc[1::2]

def plot_totale_tijd():
    # Ideale lijn
    # speedup = df_openmp['tijd totaal'] / df_openmp['aantal cores']
    plt.plot(df_openmp['aantal cores'], df_openmp['tijd totaal'] / df_openmp['aantal cores'],
             marker='*', color='gold', label='Ideale Speedup - S(p) = p')

    # Plot lijnen met en zonder OpenMP
    plt.plot(df_openmp['aantal cores'], df_openmp['tijd totaal'],
             marker='+', color='red', label='Met OpenMP')
    plt.plot(df_no_openmp['aantal cores'], df_no_openmp['tijd totaal'],
             marker='x', color='orangered', label='Zonder OpenMP')
    plt.fill_between(df_openmp['aantal cores'],
                     df_openmp['tijd totaal'],
                     df_no_openmp['tijd totaal'],
                     alpha=0.2, color='lightsalmon')
    # Labels en titel
    plt.xlabel('Aantal cores')
    plt.ylabel('Tijd totaal (s)')
    plt.title('Performance vergelijking Totale tijd OpenMP vs Zonder OpenMP')
    plt.legend()

    plt.show()

def plot_berekening_tijd():
    # Plot bereken pixel tijd lijnen met en zonder OpenMP
    plt.plot(df_openmp['aantal cores'], df_openmp['bereken tijd'],
             marker='+',color='green', label='Met OpenMP')
    plt.plot(df_no_openmp['aantal cores'], df_no_openmp['bereken tijd'],
             marker='x', color='forestgreen', label='Zonder OpenMP')
    plt.fill_between(df_openmp['aantal cores'],
                     df_openmp['bereken tijd'],
                     df_no_openmp['bereken tijd'],
                     alpha=0.2, color='limegreen')

    plt.plot(df_openmp['aantal cores'], df_openmp['bereken tijd'] / df_openmp['aantal cores'],
             marker='*', color='lime', label='Ideale Speedup - S(p) = p')

    # Labels en titel
    plt.xlabel('Aantal cores')
    plt.ylabel('Tijd totaal (s)')
    plt.title('Performance vergelijking Bereken tijd OpenMP vs Zonder OpenMP')
    plt.legend()

    plt.show()

def plot_video_opslaan_tijd():
    # Plot video opslaan tijd
    plt.plot(v_openmp['aantal cores'], v_openmp['video opslaan'],
             marker='.', color='lightskyblue', label='Video opslaan')
    plt.plot(v_no_openmp['aantal cores'], v_no_openmp['video opslaan'],
             marker='.', color='lightskyblue')
    plt.fill_between(v_openmp['aantal cores'],
                     v_openmp['video opslaan'],
                     v_no_openmp['video opslaan'],
                     alpha=0.2, color='lightblue')

    # Labels en titel
    plt.xlabel('Aantal cores')
    plt.ylabel('Tijd totaal (s)')
    plt.title('Performance van de video opslaan tijd')
    plt.legend()

    plt.show()

def plot_speedup():
    speedup = df_openmp['tijd totaal'].iloc[0] / df_openmp['tijd totaal']

    plt.plot(df_openmp['aantal cores'], speedup,
             marker='+', color='cornflowerblue', label='Gemeten Speedup')
    plt.plot(df_openmp['aantal cores'], df_openmp['aantal cores'],
             linestyle='--', color='gray', label='Ideale Speedup')

    # Labels en titel
    plt.xlabel('Aantal cores')
    plt.ylabel('Speedup factor')
    plt.title('Speedup analyse')
    plt.legend()
    plt.show()

def plot_efficiency():
    speedup = df_openmp['tijd totaal'].iloc[0] / df_openmp['tijd totaal']
    efficiency = speedup / df_openmp['aantal cores']

    plt.plot(df_openmp['aantal cores'], efficiency,
             marker='x', color='royalblue', label='Gemeten Efficiency')
    plt.plot(df_openmp['aantal cores'], np.ones(len(df_openmp['aantal cores'])),
             linestyle='--', color='gray', label='Ideale Efficiency')

    # Labels en titel
    plt.xlabel('Aantal cores')
    plt.ylabel('Efficiency (Sn / n)')
    plt.title('Efficiency Analyse')
    plt.legend()
    plt.show()


def plot_alles():
    # Plot video opslaan tijd
    plt.plot(v_openmp['aantal cores'], v_openmp['video opslaan'],
             marker='.', color='lightskyblue', label='Video opslaan')
    plt.plot(v_no_openmp['aantal cores'], v_no_openmp['video opslaan'],
             marker='.', color='lightskyblue')
    plt.fill_between(v_openmp['aantal cores'],
                     v_openmp['video opslaan'],
                     v_no_openmp['video opslaan'],
                     alpha=0.2, color='lightblue')

    # Plot bereken pixel tijd lijnen met en zonder OpenMP
    plt.plot(df_openmp['aantal cores'], df_openmp['bereken tijd'],
             marker='+', color='green', label='Met OpenMP')
    plt.plot(df_no_openmp['aantal cores'], df_no_openmp['bereken tijd'],
             marker='x', color='forestgreen', label='Zonder OpenMP')
    plt.fill_between(df_openmp['aantal cores'],
                     df_openmp['bereken tijd'],
                     df_no_openmp['bereken tijd'],
                     alpha=0.2, color='limegreen')

    # Plot totale tijd lijnen met en zonder OpenMP
    plt.plot(df_openmp['aantal cores'], df_openmp['tijd totaal'],
             marker='+', color='red', label='Met OpenMP')
    plt.plot(df_no_openmp['aantal cores'], df_no_openmp['tijd totaal'],
             marker='x', color='orangered', label='Zonder OpenMP')
    plt.fill_between(df_openmp['aantal cores'],
                     df_openmp['tijd totaal'],
                     df_no_openmp['tijd totaal'],
                     alpha=0.2, color='lightsalmon')

    # Labels en titel
    plt.xlabel('Aantal cores')
    plt.ylabel('Tijd totaal (s)')
    plt.title('Vergelijking van alle metingen')
    plt.legend()

    plt.show()

if __name__ == '__main__':
    plot_totale_tijd()
    plot_berekening_tijd()
    plot_video_opslaan_tijd()
    plot_speedup()
    plot_efficiency()
    plot_alles()
