import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

FIG_W, FIG_H = 6.27, 4.5
OUT = Path(__file__).resolve().parents[1] / "outputs"

HP_LABEL = "Horsepower (hp)"
PRICE_LABEL = "Price (US dollars)"
MPG_LABEL = "Highway fuel economy (mpg)"
MPG_SHORT = "Highway mpg"
INK = "#333333"
POINT = "#3b6ea5"

MPG_REFERENCE = (16, 35, 54)
HP_LIMITS = (40, 270)
PRICE_LIMITS = (4000, 46000)


def setup():
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["font.size"] = 8
    plt.rcParams["axes.edgecolor"] = INK
    plt.rcParams["axes.linewidth"] = 0.6
    OUT.mkdir(exist_ok=True)


def style_axes(ax, labels=True):
    ax.set_xlim(*HP_LIMITS)
    ax.set_ylim(*PRICE_LIMITS)
    ax.yaxis.set_major_formatter(lambda value, _: f"${value / 1000:.0f}k")
    ax.grid(color="#e6e6e6", linewidth=0.5)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    if labels:
        ax.set_xlabel(HP_LABEL)
        ax.set_ylabel(PRICE_LABEL)


def size_for(mpg):
    return (np.asarray(mpg) - 10) * 1.7


def size_handles(color=POINT):
    return [Line2D([], [], marker="o", linestyle="", color=color, alpha=0.7,
                   markersize=np.sqrt(size_for(mpg)), label=str(mpg))
            for mpg in MPG_REFERENCE]


def add_caption(fig, text, width=105):
    wrapped = textwrap.fill(text, width)
    fig.text(0.02, 0.012, wrapped, fontsize=7, va="bottom", color=INK)


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf")
    fig.savefig(OUT / f"{name}.png", dpi=300)
    plt.close(fig)
    print("Saved", name)