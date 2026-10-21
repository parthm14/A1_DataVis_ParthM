from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from key import draw_key
from load_data import load_farr
from panel import draw_panel

PAGE = (210 / 25.4, 297 / 25.4)
ROWS, COLS = 4, 3
OUT = Path(__file__).resolve().parents[1] / "outputs"

NAME = "Parth Maheshwari (22331169)"
MODULE = "CS7DS4 / CSU44065 Data Visualization 2025-26 | Assignment 1"


def average_year(data):
    weekly = data.groupby("week").agg(
        deaths=("deaths", "mean"),
        mean_temperature=("mean_temperature", "mean"),
        mortality_reference=("mortality_reference", "mean"),
        temperature_reference=("temperature_reference", "mean"),
    )
    return weekly.reset_index()


def main():
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["font.family"] = "DejaVu Sans"
    data = load_farr()

    fig, axes = plt.subplots(ROWS, COLS, figsize=PAGE,
                             subplot_kw={"projection": "polar"})
    panels = list(axes.flat)
    for ax, year in zip(panels, range(1840, 1851)):
        draw_panel(ax, data[data["year"] == year], str(year))
    draw_panel(panels[-1], average_year(data), "Mean")

    draw_key(fig, data)

    fig.text(0.03, 0.997, NAME, fontsize=7.5, va="top", color="#444444")
    fig.text(0.97, 0.997, MODULE, fontsize=7.5, va="top", ha="right",
             color="#444444")
    fig.suptitle("Temperature and Mortality of London, 1840 to 1850",
                 fontsize=14, y=0.98)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.945, bottom=0.235,
                        wspace=0.0, hspace=0.3)

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / "poster_draft.pdf")
    fig.savefig(OUT / "poster_draft.png", dpi=150)
    print("Saved", OUT / "poster_draft.pdf")


if __name__ == "__main__":
    main()