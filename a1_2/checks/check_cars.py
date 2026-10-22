import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from load_cars import load_cars

cars = load_cars()
assert len(cars) == 201
assert cars.isna().sum().sum() == 0
assert cars.make.nunique() == 22
assert cars.price.between(5118, 45400).all()
assert cars.horsepower.between(48, 262).all()
assert cars.highway_mpg.between(16, 54).all()
print("All checks passed")