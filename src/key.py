import textwrap

import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from panel import (COLD, HOT, MISSING, MORTALITY, REFERENCE, SALUBRITY,
                   death_radius, draw_panel, temp_radius)

PAGE_W, PAGE_H = 210 / 25.4, 297 / 25.4
KEY_SIZE = 1.65
TOP = 0.215
COLUMNS = [0.265, 0.495, 0.73]
WRAP = 38
LINE = 0.0108
TEXT_SIZE = 6.8

SWATCHES = [
    (MORTALITY, "Deaths above average"),
    (SALUBRITY, "Deaths below average"),
    (HOT, "Temperature above average"),
    (COLD, "Temperature below average"),
    (MISSING, "Value missing in the data"),
]

COLOUR_NOTES = [
    "Farr's names for these: mortality (black), salubrity (yellow), "
    "hot (red) and cold (blue).",
    "The dashed circle in each ring marks that ring's average.",
]

HOW_TO_READ = [
    "One circle per year. January is at the bottom and time runs clockwise, "
    "one spoke per week.",
    "Outer ring: weekly deaths. Inner ring: weekly mean temperature in degrees "
    "Fahrenheit.",
    "Colour shows whether a week is above or below the average. The distance "
    "from the dashed circle shows by how much.",
    "Grid circles mark every 100 deaths and every 10 degrees, on the same scale "
    "in every circle. The key circle (1846) is labelled at 20, 40 and 60 degrees "
    "and at 800, 1200 and 1600 deaths.",
]

NOTES = [
    "Deaths average is population adjusted, so the dashed circle varies slightly "
    "by year. Temperature average: 48.4 degrees.",
    "Mean: weekly mean of observed values, 1840 to 1850. Missing weeks are "
    "skipped, so it may understate the high death years.",
    "Area grows with distance from the centre: compare distances from the "
    "dashed circle, not areas.",
    "1849: only 10 of 52 weekly death values are available. Highest value: "
    "1930 deaths, week ending 15 September 1849.",
]

SOURCE = ("Source: W. Farr, Temperature and Mortality of London (1852). Values "
          "extracted from the archive chart; some errors are possible.")


def write_text(fig, x, y, paragraphs, width=WRAP):
    for paragraph in paragraphs:
        wrapped = textwrap.fill(paragraph, width)
        fig.text(x, y, wrapped, fontsize=TEXT_SIZE, va="top", linespacing=1.3)
        y -= LINE * (wrapped.count("\n") + 1) + 0.005
    return y


def write_heading(fig, x, y, heading):
    fig.text(x, y, heading, fontsize=8, fontweight="bold", va="top")
    return y - 0.02


def write_swatches(fig, x, y):
    for color, label in SWATCHES:
        fig.add_artist(Rectangle((x, y - 0.0045), 0.02, 0.009, color=color,
                                 transform=fig.transFigure))
        fig.text(x + 0.028, y, label, fontsize=TEXT_SIZE, va="center")
        y -= 0.0145
    fig.add_artist(Line2D([x, x + 0.02], [y, y], color=REFERENCE, linewidth=0.8,
                          linestyle="--", transform=fig.transFigure))
    fig.text(x + 0.028, y, "Average level (dashed)", fontsize=TEXT_SIZE,
             va="center")
    return y - 0.018


def label_scales(ax):
    angle = np.pi
    box = dict(boxstyle="square,pad=0.1", fc="white", ec="none", alpha=0.9)
    for temp in (20, 40, 60):
        ax.text(angle, temp_radius(temp), str(temp), fontsize=5, ha="center",
                va="center", bbox=box, zorder=5)
    for deaths in (800, 1200, 1600):
        ax.text(angle, death_radius(deaths), str(deaths), fontsize=5,
                ha="center", va="center", bbox=box, zorder=5)


def draw_key(fig, data):
    ax = fig.add_axes([0.03, 0.04, KEY_SIZE / PAGE_W, KEY_SIZE / PAGE_H],
                      projection="polar")
    draw_panel(ax, data[data["year"] == 1846], "Key")
    label_scales(ax)

    x1, x2, x3 = COLUMNS
    y = write_heading(fig, x1, TOP, "Colour key")
    y = write_swatches(fig, x1, y)
    write_text(fig, x1, y, COLOUR_NOTES)

    y = write_heading(fig, x2, TOP, "How to read each circle")
    write_text(fig, x2, y, HOW_TO_READ)

    y = write_heading(fig, x3, TOP, "Notes")
    write_text(fig, x3, y, NOTES)

    fig.text(0.03, 0.004, SOURCE, fontsize=5.5, va="bottom", color="#444444")