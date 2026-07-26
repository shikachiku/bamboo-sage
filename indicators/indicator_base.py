import pandas as pd

import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from settings import DATA_PATH



from symbol_loader import load_symbols
from color import title


# ===================================
# Timeframes
# ===================================

TIMEFRAMES = [
    "1M",
    "1W",
    "1D",
    "4H",
]


# ===================================
# Symbols
# ===================================

def get_symbols():

    return load_symbols()


# ===================================
# Load RAW
# ===================================

def load_raw(symbol, timeframe):

    filename = (
        DATA_PATH
        / symbol["Folder"]
        / "raw"
        / f"{timeframe}.csv"
    )

    if not filename.exists():

        print(f"RAW Not Found : {filename}")

        return None

    return pd.read_csv(
        filename,
        index_col=0,
        parse_dates=True,
    )


# ===================================
# Save Indicator
# ===================================

def save_indicator(
    symbol,
    indicator,
    timeframe,
    dataframe,
):

    folder = (
        DATA_PATH
        / symbol["Folder"]
        / "indicator"
        / indicator
    )

    folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = folder / f"{timeframe}.csv"

    dataframe.to_csv(filename)

    print(f"Saved : {filename}")


# ===================================
# Display
# ===================================

def print_symbol(symbol):

    print()
    print("=" * 60)
    print(symbol["Name"])
    print("=" * 60)


def print_complete(indicator):

    print()
    print("=" * 60)
    print(f"{indicator.upper()} COMPLETE")
    print("=" * 60)


# ===================================
# Runner
# ===================================

def run_indicator(
    indicator,
    calculate,
):

    title(f"{indicator.upper()} START")

    symbols = get_symbols()

    for symbol in symbols:

        print_symbol(symbol)

        for timeframe in TIMEFRAMES:

            data = load_raw(
                symbol,
                timeframe,
            )

            if data is None:

                continue

            result = calculate(data)

            save_indicator(
                symbol,
                indicator,
                timeframe,
                result,
            )

    print_complete(indicator)