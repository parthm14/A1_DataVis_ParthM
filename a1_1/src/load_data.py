from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "farr.csv"


def load_farr(path=DATA_PATH):
    # "?" marks values the extraction could not read
    return pd.read_csv(path, na_values=["?"], parse_dates=["week_ending"])