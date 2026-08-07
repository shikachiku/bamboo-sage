import pandas as pd



# ===================================
# Parameter
# ===================================

INDICATOR = "macd"

FAST = 12
SLOW = 26
SIGNAL = 9



# ===================================
# EMA
# TradingView compatible
# ===================================

def ema(series, length):

    return (
        series
        .ewm(
            span=length,
            adjust=False
        )
        .mean()
    )



# ===================================
# MACD Calculation
# ===================================

def calculate(data):

    import numpy as np


    result = data.copy()


    close = result["Close"]



    # ===================================
    # EMA
    # ===================================

    fast_ema = ema(
        close,
        FAST
    )


    slow_ema = ema(
        close,
        SLOW
    )



    # ===================================
    # MACD Line
    # ===================================

    result["MACD"] = (
        fast_ema
        -
        slow_ema
    )



    # ===================================
    # Signal Line
    # ===================================

    result["MACD_SIGNAL"] = ema(
        result["MACD"],
        SIGNAL
    )



    # ===================================
    # Histogram
    # ===================================

    result["MACD_HIST"] = (
        result["MACD"]
        -
        result["MACD_SIGNAL"]
    )



    # ===================================
    # MACD Color
    # ===================================

    result["MACD_COLOR"] = (
        result["MACD_HIST"]
        >
        0
    ).map(
        {
            True: "BLUE",
            False: "RED",
        }
    )



    # ===================================
    # MACD Cross
    # NumPy Vectorized
    # ===================================

    macd = (
        result["MACD"]
        .to_numpy()
    )


    signal = (
        result["MACD_SIGNAL"]
        .to_numpy()
    )


    cross = np.full(
        len(result),
        "",
        dtype=object
    )


    golden = (
        (macd[:-1] <= signal[:-1])
        &
        (macd[1:] > signal[1:])
    )


    dead = (
        (macd[:-1] >= signal[:-1])
        &
        (macd[1:] < signal[1:])
    )


    cross[1:][golden] = "GOLDEN"

    cross[1:][dead] = "DEAD"


    result["MACD_CROSS"] = cross



    # ===================================
    # MACD Level
    # ===================================

    macd_min = (
        result["MACD"]
        .min()
    )


    macd_max = (
        result["MACD"]
        .max()
    )


    if macd_max != macd_min:

        result["MACD_LEVEL"] = (
            result["MACD"]
            -
            macd_min
        ) / (
            macd_max
            -
            macd_min
        )

    else:

        result["MACD_LEVEL"] = 0.5



    # ===================================
    # MACD Slope
    # ===================================

    result["MACD_SLOPE"] = (
        result["MACD"]
        -
        result["MACD"].shift(1)
    )


    result["MACD_SLOPE"] = (
        result["MACD_SLOPE"]
        .fillna(0)
    )



    return result

