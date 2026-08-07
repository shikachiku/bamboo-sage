from pathlib import Path

import sys
import os
from concurrent.futures import ProcessPoolExecutor


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

def load_raw(symbol, timeframe, source="tv"):


    if source == "investing":

        folder = "investraw"

    else:

        folder = "raw"



    filename = (
        DATA_PATH
        / symbol["Folder"]
        / folder
        / f"{timeframe}.csv"
    )


    if not filename.exists():

        print(f"RAW Not Found : {filename}")

        return None


    return pd.read_csv(filename)


# ======================================
# Save Analysis
# ======================================

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


    filename = (
        folder
        / f"{timeframe}.csv"
    )


    temp_filename = (
        folder
        / f"{timeframe}.tmp"
    )


    dataframe.to_csv(
        temp_filename,
        index=False,
        float_format="%.6f",
        na_rep="",
    )


    temp_filename.replace(
        filename
    )


    print(
        f"Saved : {filename}"
    )


# ======================================
# Process
# ======================================


def process(
    symbol,
    timeframe,
    source="tv",
):

    import time

    total_start = time.perf_counter()

    df = load_raw(
        symbol,
        timeframe,
        source,
    )

    if df is None:
        return

    print()
    print(f"[{symbol['Name']} {timeframe}]")

    # -----------------------------
    # Wick
    # -----------------------------
    start = time.perf_counter()
    df = wick(df)
    print(f"Wick             : {time.perf_counter() - start:.3f} sec")

    # -----------------------------
    # Heikin Ashi
    # -----------------------------
    start = time.perf_counter()
    df = heikin_ashi(df)
    print(f"Heikin Ashi      : {time.perf_counter() - start:.3f} sec")

    # -----------------------------
    # ADX
    # -----------------------------
    start = time.perf_counter()
    df = adx(df)
    print(f"ADX              : {time.perf_counter() - start:.3f} sec")

    # -----------------------------
    # HighLow5
    # -----------------------------
    start = time.perf_counter()
    df = highlow5(df)
    print(f"HighLow5         : {time.perf_counter() - start:.3f} sec")

    # -----------------------------
    # Swing
    # -----------------------------
    start = time.perf_counter()
    df = swing(df)
    print(f"Swing            : {time.perf_counter() - start:.3f} sec")

    # -----------------------------
    # MACD
    # -----------------------------
    start = time.perf_counter()
    df = macd(df)
    print(f"MACD             : {time.perf_counter() - start:.3f} sec")

    # -----------------------------
    # Stochastic
    # -----------------------------
    start = time.perf_counter()
    df = stochastic(df)
    print(f"Stochastic       : {time.perf_counter() - start:.3f} sec")

    # -----------------------------
    # Moving Average
    # -----------------------------
    start = time.perf_counter()
    df = moving_average(df)
    print(f"Moving Average   : {time.perf_counter() - start:.3f} sec")

    save_analysis(
        symbol,
        timeframe,
        df,
    )

    print(f"TOTAL            : {time.perf_counter() - total_start:.3f} sec")

# ======================================
# Process One Symbol
# ======================================

def process_symbol(
    symbol,
    source,
):

    print()
    print("=" * 60)
    print(symbol["Name"])
    print("=" * 60)

    for timeframe in TIMEFRAMES:

        process(
            symbol,
            timeframe,
            source,
        )

# ======================================
# MAIN
# ======================================

def main():

    print("=" * 40)
    print("ANALYSIS ENGINE START")
    print("=" * 40)

    SOURCE = "investing"

    print()
    print(
        "SOURCE:",
        SOURCE
    )
    print()

    symbols = load_symbols(
        "invest_symbols.csv"
    )

    cpu_count = os.cpu_count() or 1

    workers = min(
        cpu_count,
        len(symbols)
    )

    print(
        f"CPU CORES   : {cpu_count}"
    )

    print(
        f"CPU WORKERS : {workers}"
    )

    print()

    with ProcessPoolExecutor(
        max_workers=workers
    ) as executor:

        executor.map(
            process_symbol,
            symbols,
            [SOURCE] * len(symbols)
        )

    print()
    print("=" * 40)
    print("ANALYSIS ENGINE COMPLETE")
    print("=" * 40)


if __name__ == "__main__":

    main()