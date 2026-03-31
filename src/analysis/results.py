import matplotlib.pyplot as plt

def main():
    # Tvoji stvarni podaci
    labels = ['Baseline (-O0)', 'Random Search', 'Greedy Search']
    values = [638, 287, 271]
    colors = ['#ff9999', '#66b3ff', '#99ff99'] # Crvena, Plava, Zelena

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=colors, edgecolor='black')

    # Dodavanje vrednosti na stubice
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 10, int(yval), 
                 ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.title('Poređenje metoda optimizacije veličine koda (cBench/qsort)', fontsize=14)
    plt.ylabel('Broj instrukcija (LLVM IR)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Linija ustede
    plt.axhline(y=638, color='gray', linestyle='--', linewidth=1)
    
    plt.savefig('results.png')
    print("Grafik sačuvan kao 'results.png'")

if __name__ == "__main__":
    main()
