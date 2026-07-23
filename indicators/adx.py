import os
import pandas as pd

# ======================================================
# TradingView Parameter
# ======================================================

ADX_LENGTH = 10
ADX_THRESHOLD = 5

# ======================================================
# ADX
# ======================================================

def calculate_adx(data, period=ADX_LENGTH):

    high = data["HA_High"]
    low = data["HA_Low"]
    close = data["HA_Close"]

    plus_dm = high.diff()
    minus_dm = -low.diff()

    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm < 0] = 0

    tr = pd.concat(
        [
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)

    atr = tr.rolling(period).mean()

    plus_di = (
        100
        * plus_dm.rolling(period).mean()
        / atr
    )

    minus_di = (
        100
        * minus_dm.rolling(period).mean()
        / atr
    )

    dx = (
        (plus_di - minus_di).abs()
        / (plus_di + minus_di)
    ) * 100

    adx = dx.rolling(period).mean()

    result = pd.DataFrame(index=data.index)

    result["ADX"] = adx
    result["PLUS_DI"] = plus_di
    result["MINUS_DI"] = minus_di

    # ==================================================
    # Trend
    # ==================================================

    result["TREND"] = "SIDE"

    result.loc[
        result["PLUS_DI"] > result["MINUS_DI"],
        "TREND",
    ] = "UP"

    result.loc[
        result["PLUS_DI"] < result["MINUS_DI"],
        "TREND",
    ] = "DOWN"

    # ==================================================
    # ADX Threshold
    # ==================================================

    result["ADX_OK"] = result["ADX"] >= ADX_THRESHOLD

    return result


# ======================================================
# CSV
# ======================================================

def process_file(input_csv, output_csv):

    data = pd.read_csv(
        input_csv,
        index_col=0,
        parse_dates=True,
    )

    adx = calculate_adx(data)

    os.makedirs(
        os.path.dirname(output_csv),
        exist_ok=True,
    )

    adx.to_csv(output_csv)

    print(f"Saved -> {output_csv}")


# ======================================================
# Main
# ======================================================

if __name__ == "__main__":

    BASE = "data"

    SYMBOL = "WHSELFINVEST_JAPAN225CFD"

    TIMEFRAMES = [
        "1M",
        "1W",
        "1D",
        "4H",
    ]

    for tf in TIMEFRAMES:

        process_file(
            f"{BASE}/{SYMBOL}/live/HA_{tf}.csv",
            f"{BASE}/{SYMBOL}/live/ADX_{tf}.csv",
        )

    print()
    print("==============================")
    print("ADX Complete")
    print("==============================")