from panel import WEEK_WIDTH, death_radius

LINE = dict(arrowstyle="-", color="#333333", linewidth=0.6,
            shrinkA=0, shrinkB=0)


def peak_row(year_df):
    return year_df.loc[year_df["deaths"].idxmax()]


def label_peak(ax, year_df, offset, ha="left", va="center"):
    row = peak_row(year_df)
    day = row["week_ending"]
    text = f"{int(row['deaths'])} deaths\nweek ending\n{day.day} {day:%b}"
    theta = WEEK_WIDTH * (row["week"] - 0.5)
    ax.annotate(text, xy=(theta, death_radius(row["deaths"])),
                xytext=offset, textcoords="offset points", fontsize=6.5,
                ha=ha, va=va, arrowprops=LINE, annotation_clip=False)


def label_missing(ax, year_df, week, offset, ha="left", va="center"):
    gaps = int(year_df["deaths"].isna().sum())
    ref = death_radius(year_df["mortality_reference"].iloc[0])
    theta = WEEK_WIDTH * (week - 0.5)
    ax.annotate(f"Death data missing\nfor {gaps} of 52 weeks",
                xy=(theta, ref), xytext=offset, textcoords="offset points",
                fontsize=6.5, ha=ha, va=va, color="#6a4a86",
                arrowprops=dict(arrowstyle="-", color="#9a78b8",
                                linewidth=0.6, shrinkA=0, shrinkB=0),
                annotation_clip=False)