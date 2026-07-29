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
    # Cross Signal
    # ===================================

    result["MACD_CROSS"] = ""



    for i in range(1, len(result)):


        # Golden Cross

        if (
            result["MACD"].iloc[i - 1]
            <=
            result["MACD_SIGNAL"].iloc[i - 1]

            and

            result["MACD"].iloc[i]
            >
            result["MACD_SIGNAL"].iloc[i]
        ):

            result.iloc[
                i,
                result.columns.get_loc(
                    "MACD_CROSS"
                )
            ] = "GOLDEN"



        # Dead Cross

        elif (
            result["MACD"].iloc[i - 1]
            >=
            result["MACD_SIGNAL"].iloc[i - 1]

            and

            result["MACD"].iloc[i]
            <
            result["MACD_SIGNAL"].iloc[i]
        ):

            result.iloc[
                i,
                result.columns.get_loc(
                    "MACD_CROSS"
                )
            ] = "DEAD"



    return result

