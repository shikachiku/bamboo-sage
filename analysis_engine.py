from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

from settings import DATA_PATH
from symbol_loader import load_symbols

from indicators.heikin_ashi import calculate as heikin_ashi
from indicators.adx import calculate as adx
from indicators.highlow5 import calculate as highlow5
from indicators.macd import calculate as macd
from indicators.stochastic import calculate as stochastic
from indicators.swing import calculate as swing
from indicators.moving_average import calculate as moving_average
from indicators.wick import calculate as wick


# ======================================
# Parameter
# ======================================

TIMEFRAMES = [
    "1M",
    "1W",
    "1D",
    "4H",
]


# ======================================
# Load RAW
# ======================================

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

    return pd.read_csv(filename)


# ======================================
# Save Analysis
# ======================================

def save_analysis(
    symbol,
    timeframe,
    dataframe,
):

    folder = (
        DATA_PATH
        / symbol["Folder"]
        / "analysis"
    )

    folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = folder / f"{timeframe}.csv"

    dataframe.to_csv(
        filename,
        index=False,
    )

    print(f"Saved : {filename}")


# ======================================
# Process
# ======================================

def process(
    symbol,
    timeframe,
):

    df = load_raw(
        symbol,
        timeframe,
    )

    if df is None:
        return

    # -----------------------------
    # Wick
    # -----------------------------

    df = wick(df)

    # -----------------------------
    # Heikin Ashi
    # -----------------------------

    df = heikin_ashi(df)
    
    
    # -----------------------------
    # ADX
    # -----------------------------
    df = adx(df)
    
    # -----------------------------
    # HighLow5
    # -----------------------------
    df = highlow5(df)
    
    # -----------------------------
    # Swing
    # -----------------------------
    df = swing(df)
    
    # -----------------------------
    # MACD
    # -----------------------------
    df = macd(df)
    
    # -----------------------------
    # Stochastic
    # -----------------------------
    df = stochastic(df)
    
    # -----------------------------
    # Moving Average
    # -----------------------------

    df = moving_average(df)
    

    save_analysis(
        symbol,
        timeframe,
        df,
    )


# ======================================
# MAIN
# ======================================

def main():

    print("=" * 40)
    print("ANALYSIS ENGINE START")
    print("=" * 40)

    symbols = load_symbols()

    for symbol in symbols:

        print()
        print("=" * 60)
        print(symbol["Name"])
        print("=" * 60)

        for timeframe in TIMEFRAMES:

            process(
                symbol,
                timeframe,
            )

    print()
    print("=" * 40)
    print("ANALYSIS ENGINE COMPLETE")
    print("=" * 40)


if __name__ == "__main__":

    main()