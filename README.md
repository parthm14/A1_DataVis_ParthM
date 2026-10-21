# CS7DS4 / CSU44056 Data Visualization, Assignment 1

Parth Maheshwari, student number 22331169. Trinity College Dublin, 2026-27.

This repository holds the source code for both parts of Assignment 1.

- **A1.1:** a one page A4 mini poster that recreates Farr's 1852 chart of temperature and mortality in London, 1840 to 1850.
- **A1.2:** a set of seven charts comparing visual encoding channels, built from `cars.csv`.

The submitted PDF is not stored in the zip. It combines the poster, the A1.1 description and the A1.2 charts with their captions.

## Folder structure

```
A1_DataVis_ParthM/
  README.md
  .gitignore
  requirements.txt
  notes/        design decisions for both parts
  a1_1/         Farr poster
    data/raw/farr.csv
    src/        poster code
    checks/     data check
    outputs/    generated files, ignored by Git
  a1_2/         encoding charts
    data/raw/cars.csv
    src/        chart code
    outputs/    generated files, ignored by Git
```

## Setup

The project uses Python 3.11 with pandas, NumPy and matplotlib.

```bash
python -m venv ~/.venvs/farr_a1
source ~/.venvs/farr_a1/bin/activate
pip install -r requirements.txt
```

## A1.1: Farr poster

Run these commands from the repository root.

```bash
python a1_1/checks/check_data.py
python a1_1/src/build_chart.py
```

The first command checks `farr.csv` (572 weekly rows, 102 missing death values, 46 missing temperatures). The second writes the poster to `a1_1/outputs/poster_draft.pdf`.

Files in `a1_1/src`:

- `load_data.py` reads the data. A question mark in the file is read as a missing value.
- `panel.py` draws one circle: grid, deviation rings, reference circles and missing value wedges.
- `callouts.py` adds the peak death labels and the missing data note.
- `key.py` draws the key circle, the colour key and the notes.
- `build_chart.py` lays out the page and exports the PDF.

Design notes:

- The radius scales are linear and the same for every circle.
- Missing values are shown as lavender wedges and never estimated.
- The Mean circle averages all eleven years over observed weeks, although the brief describes ten.
- The temperature unit is assumed to be degrees Fahrenheit.

## A1.2: Encoding charts

To be completed. This section will list the chart scripts, the encoding channel used in each chart, and the command to rebuild every figure.

## Data

- `farr.csv`: provided for the module, extracted from Farr's archive chart. Some extraction errors are possible.
- `cars.csv`: provided for the module.

## Tools and AI use

Python, pandas, NumPy and matplotlib. Minimal AI help