from pathlib import Path
import pandas as pd

from settings import DATA_PATH
from symbol_loader import load_symbols
from color import title


# ===================================
# Parameter
# ===================================

INDICATOR = "indicator_name"

TIMEFRAMES = [
    "1M",
    "1W",
    "1D",
    "4H",
]


# ===================================
# Indicator
# ===================================

def calculate(data):
    """
    インジケータ計算
    この関数だけを書き換える
    """

    result = data.copy()

    return result


# ===================================
# Process
# ===================================

def process(symbol, tf):

    input_csv = (
        DATA_PATH
        / symbol["Folder"]
        / "raw"
        / f"{tf}.csv"
    )

    if not input_csv.exists():

        print(f"Skip : {input_csv}")

        return

    output_folder = (
        DATA_PATH
        / symbol["Folder"]
        / "indicator"
        / INDICATOR
    )

    output_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_csv = (
        output_folder
        / f"{tf}.csv"
    )

    data = pd.read_csv(
        input_csv,
        index_col=0,
        parse_dates=True,
    )

    result = calculate(data)

    result.to_csv(output_csv)

    print(f"Saved : {output_csv}")


# ===================================
# MAIN
# ===================================

def main():

    title(f"{INDICATOR.upper()} START")

    symbols = load_symbols()

    for symbol in symbols:

        print()
        print("=" * 60)
        print(symbol["Name"])
        print("=" * 60)

        for tf in TIMEFRAMES:

            process(
                symbol,
                tf,
            )

    print()

    title(f"{INDICATOR.upper()} COMPLETE")


if __name__ == "__main__":

    main()