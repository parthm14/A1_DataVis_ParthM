from pathlib import Path
import matplotlib

matplotlib.use("pdf")
import matplotlib.pyplot as plt

A4 = (210 / 25.4, 297 / 25.4)
OUT = Path(__file__).resolve().parents[1] / "outputs"


def main():
    plt.rcParams["pdf.fonttype"] = 42
    fig = plt.figure(figsize=A4)
    fig.text(0.5, 0.5, "A4 smoke test", ha="center", va="center", fontsize=20)
    OUT.mkdir(exist_ok=True)
    # bbox_inches="tight" would change the page size, so it is left out
    fig.savefig(OUT / "smoke_test.pdf")
    print("Saved", OUT / "smoke_test.pdf")


if __name__ == "__main__":
    main()