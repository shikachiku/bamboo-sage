import os
import pandas as pd

# ===================================
# Parameter
# ===================================

BASE = "data"

SYMBOL = "WHSELFINVEST_JAPAN225CFD"

TIMEFRAMES = [
    "1M",
    "1W",
    "1D",
    "4H",
]

PERIOD = 14

TREND_ON = 25


# ===================================
# ADX
# ===================================

def calculate_adx(data, period=14):

    high = data["High"]

    low = data["Low"]

    close = data["Close"]

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

    result["+DI"] = plus_di

    result["-DI"] = minus_di

    # DI方向
    result["DI_DIRECTION"] = result.apply(
        lambda r:
            "UP"
            if r["+DI"] > r["-DI"]
            else "DOWN",
        axis=1,
    )

    # トレンド判定
    result["TREND_ON"] = (
        result["ADX"] >= TREND_ON
    )

    return result


# ===================================
# Process
# ===================================

def process(tf):

    input_csv = (
        f"{BASE}/{SYMBOL}/raw/{tf}.csv"
    )

    output_csv = (
        f"{BASE}/{SYMBOL}/live/adx/{tf}.csv"
    )

    data = pd.read_csv(
        input_csv,
        index_col=0,
        parse_dates=True,
    )

    adx = calculate_adx(
        data,
        PERIOD,
    )

    os.makedirs(
        os.path.dirname(output_csv),
        exist_ok=True,
    )

    adx.to_csv(output_csv)

    print(
        f"Saved -> {output_csv}"
    )


# ===================================
# MAIN
# ===================================

if __name__ == "__main__":

    for tf in TIMEFRAMES:

        process(tf)

    print()
    print("==============================")
    print("ADX Complete")
    print("==============================")