# Legacy one-off chart from an early exploration run. The paper's figures
# come from scripts/generate_figures.py and generate_battery_figure.py.
# Kept for provenance only.
import matplotlib.pyplot as plt


def main():
    # Sample data from an early run
    labels = ["Baseline (-O0)", "Random Search", "Greedy Search"]
    values = [638, 287, 271]
    colors = ["#ff9999", "#66b3ff", "#99ff99"]  # red, blue, green

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=colors, edgecolor="black")

    # Add value labels above each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 10, int(yval),
                 ha="center", va="bottom", fontsize=12, fontweight="bold")

    plt.title("Comparison of code-size optimization methods (cBench/qsort)", fontsize=14)
    plt.ylabel("Instruction count (LLVM IR)", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Reference line at the baseline
    plt.axhline(y=638, color="gray", linestyle="--", linewidth=1)

    plt.savefig("results.png")
    print("Chart saved as 'results.png'")


if __name__ == "__main__":
    main()
