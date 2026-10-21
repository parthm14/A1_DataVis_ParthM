import textwrap

from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from panel import (COLD, HOT, MISSING, MORTALITY, REFERENCE, SALUBRITY,
                   draw_panel, label_scales)

PAGE_W, PAGE_H = 210 / 25.4, 297 / 25.4
KEY_SIZE = 1.55
TOP = 0.215
COLUMNS = [0.265, 0.495, 0.73]
WRAP = 38
LINE = 0.0108
TEXT_SIZE = 6.6

SWATCHES = [
    (MORTALITY, "Mortality: deaths above average"),
    (SALUBRITY, "Salubrity: deaths below average"),
    (HOT, "Hot: temperature above average"),
    (COLD, "Cold: temperature below average"),
    (MISSING, "Value missing in the data"),
]

HOW_TO_READ = [
    "One circle per year. January is at the bottom and time runs clockwise, "
    "one spoke per week.",
    "Outer ring: weekly deaths. Inner ring: weekly mean temperature in degrees "
    "Fahrenheit.",
    "Colour shows above or below average. Distance from the dashed circle "
    "shows by how much.",
    "Grid circles mark every 100 deaths and every 10 degrees, on one scale "
    "for all circles. The key circle shows values.",
]

NOTES = [
    "Death averages are population adjusted, so the dashed circle varies "
    "slightly by year. Temperature average: 48.4 degrees.",
    "Mean: weekly mean of observed values, 1840 to 1850. Missing weeks are "
    "skipped, so high death years may be understated.",
    "Area grows with distance from the centre, so compare distances from the "
    "dashed circle, not areas. Missing values are not estimated.",
]

SOURCE = ("Source: W. Farr, Temperature and Mortality of London (1852). Values "
          "extracted from the archive chart; some errors are possible.")


def write_text(fig, x, y, paragraphs, width=WRAP):
    for paragraph in paragraphs:
        wrapped = textwrap.fill(paragraph, width)
        fig.text(x, y, wrapped, fontsize=TEXT_SIZE, va="top", linespacing=1.3)
        y -= LINE * (wrapped.count("\n") + 1) + 0.007
    return y


def write_heading(fig, x, y, heading):
    fig.text(x, y, heading, fontsize=8, fontweight="bold", va="top")
    return y - 0.022


def write_swatches(fig, x, y):
    for color, label in SWATCHES:
        fig.add_artist(Rectangle((x, y - 0.0045), 0.02, 0.009, color=color,
                                 transform=fig.transFigure))
        fig.text(x + 0.028, y, label, fontsize=TEXT_SIZE, va="center")
        y -= 0.0155
    fig.add_artist(Line2D([x, x + 0.02], [y, y], color=REFERENCE, linewidth=0.8,
                          linestyle="--", transform=fig.transFigure))
    fig.text(x + 0.028, y, "Average for each ring", fontsize=TEXT_SIZE,
             va="center")


def draw_key(fig, data):
    ax = fig.add_axes([0.05, 0.05, KEY_SIZE / PAGE_W, KEY_SIZE / PAGE_H],
                      projection="polar")
    draw_panel(ax, data[data["year"] == 1846], "Key")
    label_scales(ax)

    x1, x2, x3 = COLUMNS
    y = write_heading(fig, x1, TOP, "Colour key")
    write_swatches(fig, x1, y)

    y = write_heading(fig, x2, TOP, "How to read each circle")
    write_text(fig, x2, y, HOW_TO_READ)

    y = write_heading(fig, x3, TOP, "Notes")
    write_text(fig, x3, y, NOTES)

    fig.text(0.03, 0.0165, SOURCE, fontsize=6, va="bottom", color="#444444")