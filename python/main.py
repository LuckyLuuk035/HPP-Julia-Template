import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('timing_data.xlsx')

df_openmp = df[df['OpenMP'] == True]
df_no_openmp = df[df['OpenMP'] == False]

# video opslaan tijd zone
v_openmp = df.iloc[0::2]
v_no_openmp = df.iloc[1::2]

def plot_totale_tijd():
    # Plot lijnen met en zonder OpenMP
    plt.plot(df_openmp['aantal cores'], df_openmp['tijd totaal'],
             marker='x', color='red', label='Met OpenMP')
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
             marker='+', color='forestgreen', label='Zonder OpenMP')
    plt.fill_between(df_openmp['aantal cores'],
                     df_openmp['bereken tijd'],
                     df_no_openmp['bereken tijd'],
                     alpha=0.2, color='limegreen')

    # Labels en titel
    plt.xlabel('Aantal cores')
    plt.ylabel('Tijd totaal (s)')
    plt.title('Performance vergelijking Bereken tijd OpenMP vs Zonder OpenMP')
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
             marker='+', color='forestgreen', label='Zonder OpenMP')
    plt.fill_between(df_openmp['aantal cores'],
                     df_openmp['bereken tijd'],
                     df_no_openmp['bereken tijd'],
                     alpha=0.2, color='limegreen')

    # Plot totale tijd lijnen met en zonder OpenMP
    plt.plot(df_openmp['aantal cores'], df_openmp['tijd totaal'],
             marker='x', color='red', label='Met OpenMP')
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
    plot_alles()
