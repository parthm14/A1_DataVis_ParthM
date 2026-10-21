import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from load_data import load_farr

df = load_farr()

assert len(df) == 572
assert sorted(df["year"].unique()) == list(range(1840, 1851))
assert (df.groupby("year")["week"].count() == 52).all()
assert df["deaths"].isna().sum() == 102
assert df["mean_temperature"].isna().sum() == 46
assert (df["deaths"].isna() & df["mean_temperature"].isna()).sum() == 10
assert (df["temperature_reference"] == 48.4).all()
assert df["deaths"].min() == 765 and df["deaths"].max() == 1930
assert df["mean_temperature"].min() == 17 and df["mean_temperature"].max() == 73

print("All checks passed")