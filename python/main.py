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
             marker='x', label='Met OpenMP')
    plt.plot(df_no_openmp['aantal cores'], df_no_openmp['tijd totaal'],
             marker='x', label='Zonder OpenMP')
    # Labels en titel
    plt.xlabel('Aantal cores')
    plt.ylabel('Tijd totaal (s)')
    plt.title('Performance vergelijking OpenMP vs Zonder OpenMP')
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
             marker='+', label='Bereken tijd - Met OpenMP')
    plt.plot(df_no_openmp['aantal cores'], df_no_openmp['bereken tijd'],
             marker='+', label='Bereken tijd - Zonder OpenMP')

    # Plot totale tijd lijnen met en zonder OpenMP
    plt.plot(df_openmp['aantal cores'], df_openmp['tijd totaal'],
             marker='x', label='Totale tijd - Met OpenMP')
    plt.plot(df_no_openmp['aantal cores'], df_no_openmp['tijd totaal'],
             marker='x', label='Totale tijd - Zonder OpenMP')
    # Labels en titel
    plt.xlabel('Aantal cores')
    plt.ylabel('Tijd totaal (s)')
    plt.title('Performance vergelijking OpenMP vs Zonder OpenMP')
    plt.legend()

    plt.show()

if __name__ == '__main__':
    plot_alles()
