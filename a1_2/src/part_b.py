import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from common import (FIG_H, FIG_W, HP_LABEL, INK, MPG_SHORT, POINT, PRICE_LABEL,
                    add_caption, save, setup, size_for, size_handles, style_axes)
from load_cars import load_cars
from part_a import caption

MARKERS = ["o", "s", "^", "v", "D", "P", "X", "*", "<", ">", "h"]
EXTRA_COLOURS = ["#000000", "#393b79", "#8c6d31", "#7f7f7f"]
GREYS = {"#7f7f7f", "#c7c7c7"}
PANEL_SCALE = 1.6
SHAPE_SCALE = 1.25


def make_names(cars):
    return sorted(cars.make.unique())


def hue_for(names):
    tab = [matplotlib.colors.to_hex(c) for c in plt.get_cmap("tab20").colors]
    base = [c for c in tab if c not in GREYS] + EXTRA_COLOURS
    return dict(zip(names, base))


def label_make(name):
    return name.replace("alfa-romero", "alfa romeo").replace("peugot", "peugeot")


def new_axes():
    fig = plt.figure(figsize=(FIG_W, FIG_H))
    ax = fig.add_axes([0.10, 0.20, 0.64, 0.76])
    style_axes(ax)
    return fig, ax


def add_legends(ax, handles, scale=1.0):
    make_legend = ax.legend(handles=handles, title="Make", frameon=False,
                            loc="upper left", bbox_to_anchor=(1.01, 1.02),
                            fontsize=6, title_fontsize=7, labelspacing=0.35)
    ax.add_artist(make_legend)
    ax.legend(handles=size_handles("#bbbbbb", scale), title=MPG_SHORT, frameon=False,
              loc="lower right", fontsize=6, title_fontsize=7, labelspacing=1.0)


def chart_hue(cars):
    names = make_names(cars)
    colours = hue_for(names)
    fig, ax = new_axes()
    ordered = cars.sort_values("highway_mpg", ascending=False)
    ax.scatter(ordered.horsepower, ordered.price, s=size_for(ordered.highway_mpg),
               color=ordered.make.map(colours), alpha=0.85, edgecolor=INK, linewidth=0.25)
    handles = [Line2D([], [], marker="o", linestyle="", color=colours[n],
                      markeredgecolor=INK, markeredgewidth=0.3, markersize=5,
                      label=label_make(n)) for n in names]
    add_legends(ax, handles)
    add_caption(fig, caption(cars, "Chart 4. Horsepower is x position, price is y "
                "position and highway fuel economy is symbol size. Make is encoded "
                "by colour hue (22 hues)."))
    save(fig, "chart4_hue")


def chart_panels(cars):
    names = make_names(cars)
    fig, axes = plt.subplots(4, 6, figsize=(FIG_W, FIG_H), sharex=True,
                             sharey=True)
    for ax, name in zip(axes.flat, names):
        part = cars[cars.make == name]
        ax.scatter(part.horsepower, part.price, s=size_for(part.highway_mpg) / PANEL_SCALE,
                   color=POINT, alpha=0.7, edgecolor=INK, linewidth=0.25)
        style_axes(ax, labels=False)
        ax.set_xlim(30, 285)
        ax.set_ylim(2000, 49000)
        ax.set_title(label_make(name), fontsize=6.5, pad=1.5)
        ax.tick_params(labelsize=5.5, length=2, pad=1)
        ax.set_xticks([50, 150, 250])
        ax.set_yticks([10000, 25000, 40000])
    for ax in axes[2, 4:]:
        ax.tick_params(labelbottom=True)
    for ax in list(axes.flat)[len(names):]:
        ax.set_visible(False)
    key = axes.flat[-1]
    key.set_visible(True)
    key.axis("off")
    key.legend(handles=size_handles(scale=PANEL_SCALE), title=MPG_SHORT, frameon=False,
               loc="center", fontsize=5.5, title_fontsize=6, labelspacing=0.8)
    fig.subplots_adjust(left=0.11, right=0.98, top=0.95, bottom=0.21,
                        wspace=0.12, hspace=0.45)
    fig.text(0.55, 0.135, HP_LABEL, ha="center", fontsize=7)
    fig.text(0.015, 0.60, PRICE_LABEL, rotation=90, va="center", fontsize=7)
    add_caption(fig, caption(cars, "Chart 5. In every panel horsepower is x position, "
                "price is y position and highway fuel economy is symbol size. Make "
                "is encoded by spatial region (one panel per make)."))
    save(fig, "chart5_panels")


def chart_shape(cars):
    names = make_names(cars)
    fig, ax = new_axes()
    style = {}
    handles = []
    for index, name in enumerate(names):
        marker = MARKERS[index % len(MARKERS)]
        face = INK if index < len(MARKERS) else "none"
        style[name] = (marker, face)
        handles.append(Line2D([], [], marker=marker, linestyle="",
                              markerfacecolor=face, markeredgecolor=INK,
                              markersize=5, label=label_make(name)))
    for _, car in cars.sort_values("highway_mpg", ascending=False).iterrows():
        marker, face = style[car.make]
        ax.scatter(car.horsepower, car.price, marker=marker,
                   s=size_for(car.highway_mpg) / SHAPE_SCALE, facecolor=face,
                   edgecolor=INK, linewidth=0.7, alpha=0.9)
    add_legends(ax, handles, SHAPE_SCALE)
    add_caption(fig, caption(cars, "Chart 6. Horsepower is x position, price is y "
                "position and highway fuel economy is symbol size. Make is encoded "
                "by marker shape (11 shapes, each filled or hollow)."))
    save(fig, "chart6_shape")


if __name__ == "__main__":
    setup()
    cars = load_cars()
    chart_hue(cars)
    chart_panels(cars)
    chart_shape(cars)