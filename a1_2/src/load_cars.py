from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "cars.csv"


def load_cars(path=DATA_PATH):
    cars = pd.read_csv(path)
    cars.columns = [name.replace("-", "_") for name in cars.columns]
    return cars