from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patheffects import withStroke

from load_data import load_farr

R_TEMP = 0.33
K_TEMP = 0.0085
TEMP_MID = 48.4

R_DEATH = 0.70
K_DEATH = 0.0003
DEATH_MID = 1000

STEPS = 8
WEEK_WIDTH = 2 * np.pi / 52

HOT = "#c0392b"
COLD = "#2f6fb5"
MORTALITY = "#222222"
SALUBRITY = "#f2c230"
MISSING = "#c9a0dc"
GRID = "#e4e4e4"
SPOKE_STRONG = "#c8c8c8"
SPOKE_BANDS = [(0.1, 0.53), (0.62, 1.0)]
REFERENCE = "#555555"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def temp_radius(temp):
    return R_TEMP + K_TEMP * (temp - TEMP_MID)


def death_radius(deaths):
    return R_DEATH + K_DEATH * (deaths - DEATH_MID)


def densify(theta, values):
    # straight lines between weekly points, NaN wherever either end is missing
    t_parts, v_parts = [], []
    for i in range(len(theta) - 1):
        t_parts.append(np.linspace(theta[i], theta[i + 1], STEPS, endpoint=False))
        v_parts.append(np.linspace(values[i], values[i + 1], STEPS, endpoint=False))
    t_parts.append([theta[-1]])
    v_parts.append([values[-1]])
    return np.concatenate(t_parts), np.concatenate(v_parts)


def fill_deviation(ax, theta, curve, ref, above_color, below_color):
    ax.fill_between(theta, ref, curve, where=curve >= ref, interpolate=True,
                    color=above_color, linewidth=0, zorder=1)
    ax.fill_between(theta, ref, curve, where=curve <= ref, interpolate=True,
                    color=below_color, linewidth=0, zorder=1)


def mark_missing(ax, theta, values, ref_radius):
    gaps = np.isnan(values)
    ax.bar(theta[gaps], 0.03, width=WEEK_WIDTH, bottom=ref_radius - 0.015,
           color=MISSING, linewidth=0, zorder=3)


def draw_grid(ax):
    circle = np.linspace(0, 2 * np.pi, 300)
    for temp in range(20, 80, 10):
        ax.plot(circle, np.full_like(circle, temp_radius(temp)),
                color=GRID, linewidth=0.3, zorder=0)
    for deaths in range(800, 2000, 100):
        ax.plot(circle, np.full_like(circle, death_radius(deaths)),
                color=GRID, linewidth=0.3, zorder=0)
    for week in range(52):
        edge = WEEK_WIDTH * week
        strong = week % 4 == 0
        for low, high in SPOKE_BANDS:
            ax.plot([edge, edge], [low, high],
                    color=SPOKE_STRONG if strong else GRID,
                    linewidth=0.3 if strong else 0.15, zorder=0)


def label_scales(ax, size=6):
    halo = [withStroke(linewidth=1.6, foreground="white")]
    for temp in (20, 40, 60):
        ax.text(np.pi, temp_radius(temp), str(temp), fontsize=size, ha="center",
                va="center", path_effects=halo, zorder=5)
    for deaths in (800, 1200, 1600):
        ax.text(np.pi, death_radius(deaths), str(deaths), fontsize=size,
                ha="center", va="center", path_effects=halo, zorder=5)


def draw_panel(ax, year_df, title, scale=False):
    year_df = year_df.sort_values("week")
    week_theta = WEEK_WIDTH * (year_df["week"].to_numpy() - 0.5)
    deaths = year_df["deaths"].to_numpy()
    temps = year_df["mean_temperature"].to_numpy()
    death_ref = death_radius(year_df["mortality_reference"].iloc[0])
    temp_ref = temp_radius(year_df["temperature_reference"].iloc[0])

    # repeat week 1 at the end so the curve closes the circle
    closed_theta = np.append(week_theta, week_theta[0] + 2 * np.pi)
    dense_theta, dense_deaths = densify(closed_theta, np.append(deaths, deaths[0]))
    _, dense_temps = densify(closed_theta, np.append(temps, temps[0]))

    draw_grid(ax)
    fill_deviation(ax, dense_theta, death_radius(dense_deaths), death_ref,
                   MORTALITY, SALUBRITY)
    fill_deviation(ax, dense_theta, temp_radius(dense_temps), temp_ref,
                   HOT, COLD)

    circle = np.linspace(0, 2 * np.pi, 300)
    for ref in (death_ref, temp_ref):
        ax.plot(circle, np.full_like(circle, ref), color=REFERENCE,
                linewidth=0.8, linestyle="--", zorder=2)

    mark_missing(ax, week_theta, deaths, death_ref)
    mark_missing(ax, week_theta, temps, temp_ref)

    ax.set_theta_zero_location("S")
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xticks(np.deg2rad(np.arange(12) * 30 + 15))
    ax.set_xticklabels(MONTHS, fontsize=7)
    ax.tick_params(axis="x", pad=-4)
    ax.grid(False)
    ax.spines["polar"].set_visible(False)
    ax.text(-0.03, 1.07, title, transform=ax.transAxes, ha="left", va="top",
            fontsize=9.5, fontweight="bold")
    if scale:
        label_scales(ax)


if __name__ == "__main__":
    data = load_farr()
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"projection": "polar"})
    draw_panel(ax, data[data["year"] == 1846], "1846")
    out = Path(__file__).resolve().parents[1] / "outputs" / "prototype_1846.png"
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, dpi=200)
    print("Saved", out)