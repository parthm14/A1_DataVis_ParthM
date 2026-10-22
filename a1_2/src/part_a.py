import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from common import (FIG_H, FIG_W, INK, MPG_LABEL, MPG_SHORT, POINT, add_caption,
                    save, setup, size_for, size_handles, style_axes)
from load_cars import load_cars

BINS = [0, 24, 30, 37, 100]
BIN_NAMES = ["16 to 24", "25 to 30", "31 to 37", "38 to 54"]
BIN_MARKERS = ["v", "D", "o", "^"]


def caption(cars, text):
    return f"{text} Each point is one car ({len(cars)} cars)."


def new_axes():
    fig = plt.figure(figsize=(FIG_W, FIG_H))
    ax = fig.add_axes([0.10, 0.20, 0.70, 0.76])
    style_axes(ax)
    return fig, ax


def chart_colour(cars):
    fig, ax = new_axes()
    dots = ax.scatter(cars.horsepower, cars.price, c=cars.highway_mpg,
                      cmap="viridis", s=20, alpha=0.85, edgecolor=INK,
                      linewidth=0.25)
    bar = fig.colorbar(dots, cax=fig.add_axes([0.86, 0.20, 0.03, 0.76]))
    bar.set_label(MPG_LABEL)
    add_caption(fig, caption(cars, "Chart 1. Horsepower is encoded by x position "
                "and price by y position. Highway fuel economy is encoded by "
                "colour (dark purple is less efficient, yellow is more efficient)."))
    save(fig, "chart1_colour")


def chart_size(cars):
    fig, ax = new_axes()
    ax.scatter(cars.horsepower, cars.price, s=size_for(cars.highway_mpg),
               color=POINT, alpha=0.6, edgecolor=INK, linewidth=0.25)
    ax.legend(handles=size_handles(), title=MPG_SHORT, frameon=False,
              loc="upper left", bbox_to_anchor=(1.02, 1.0), labelspacing=1.2,
              fontsize=7, title_fontsize=7)
    add_caption(fig, caption(cars, "Chart 2. Horsepower is encoded by x position "
                "and price by y position. Highway fuel economy is encoded by "
                "symbol size (larger circles are more efficient)."))
    save(fig, "chart2_size")


def chart_shape(cars):
    fig, ax = new_axes()
    group = np.digitize(cars.highway_mpg, BINS[1:-1], right=True)
    for index, marker in enumerate(BIN_MARKERS):
        part = cars[group == index]
        ax.scatter(part.horsepower, part.price, marker=marker, s=18,
                   color="none", edgecolor=INK, linewidth=0.7, alpha=0.9)
    handles = [Line2D([], [], marker=m, linestyle="", markerfacecolor="none",
                      markeredgecolor=INK, markersize=5, label=name)
               for m, name in zip(BIN_MARKERS, BIN_NAMES)]
    ax.legend(handles=handles, title=MPG_SHORT, frameon=False,
              loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=7,
              title_fontsize=7, labelspacing=1.0)
    add_caption(fig, caption(cars, "Chart 3. Horsepower is encoded by x position "
                "and price by y position. Highway fuel economy is grouped into "
                "four ordered bands and encoded by marker shape."))
    save(fig, "chart3_shape")


if __name__ == "__main__":
    setup()
    cars = load_cars()
    chart_colour(cars)
    chart_size(cars)
    chart_shape(cars)