from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from load_data import load_farr
from callouts import label_missing, label_peak
from key import draw_key
from panel import draw_panel

PAGE = (210 / 25.4, 297 / 25.4)
ROWS, COLS = 4, 3
OUT = Path(__file__).resolve().parents[1] / "outputs"

NAME = "Parth Maheshwari (22331169)"
MODULE = "CSU44056 Data Visualization 2026-27 Assignment 1.1"


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

    by_year = {y: data[data["year"] == y] for y in range(1840, 1851)}
    label_peak(panels[7], by_year[1847], (34, -12), va="top")
    label_peak(panels[9], by_year[1849], (16, 26), va="bottom")
    label_missing(panels[9], by_year[1849], 44, (26, -14), va="top")

    draw_key(fig, data)

    fig.text(0.03, 0.982, NAME, fontsize=7.5, va="top", color="#444444")
    fig.text(0.97, 0.982, MODULE, fontsize=7.5, va="top", ha="right",
             color="#444444")
    fig.suptitle("Temperature and Mortality of London, 1840 to 1850",
                 fontsize=12, y=0.9625)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.924, bottom=0.24,
                        wspace=0.0, hspace=0.3)

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / "poster_draft.pdf")
    fig.savefig(OUT / "poster_draft.png", dpi=150)
    print("Saved", OUT / "poster_draft.pdf")


if __name__ == "__main__":
    main()