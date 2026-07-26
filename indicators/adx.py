import pandas as pd

from indicator_base import run_indicator


# ===================================
# Parameter
# ===================================

INDICATOR = "adx"

PERIOD = 14

TREND_ON = 25


# ===================================
# ADX
# ===================================

def calculate(data):

    result = data.copy()

    high = result["High"]

    low = result["Low"]

    close = result["Close"]

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

    atr = tr.rolling(PERIOD).mean()

    plus_di = (
        100
        * plus_dm.rolling(PERIOD).mean()
        / atr
    )

    minus_di = (
        100
        * minus_dm.rolling(PERIOD).mean()
        / atr
    )

    dx = (
        (plus_di - minus_di).abs()
        / (plus_di + minus_di)
    ) * 100

    adx = dx.rolling(PERIOD).mean()

    result["ADX"] = adx

    result["+DI"] = plus_di

    result["-DI"] = minus_di

    result["DI_DIRECTION"] = (
        result["+DI"] > result["-DI"]
    ).map(
        {
            True: "UP",
            False: "DOWN",
        }
    )

    result["TREND_ON"] = (
        result["ADX"] >= TREND_ON
    )

    return result


# ===================================
# MAIN
# ===================================

if __name__ == "__main__":

    run_indicator(
        INDICATOR,
        calculate,
    )