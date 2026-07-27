from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )


import pandas as pd

from indicator_base import run_indicator


# ===================================
# Parameter
# ===================================

INDICATOR = "adx"

# TradingView ADX Length
PERIOD = 10

# TradingView Threshold
TREND_ON = 5



# ===================================
# Wilder RMA
# ===================================

def rma(series, length):

    return (
        series
        .ewm(
            alpha=1 / length,
            adjust=False
        )
        .mean()
    )



# ===================================
# ADX Calculation
# ===================================

def calculate(data):

    result = data.copy()


    high = result["High"]

    low = result["Low"]

    close = result["Close"]



    # =================================
    # True Range
    # =================================

    tr1 = high - low

    tr2 = (
        high
        -
        close.shift(1)
    ).abs()

    tr3 = (
        low
        -
        close.shift(1)
    ).abs()


    tr = pd.concat(
        [
            tr1,
            tr2,
            tr3,
        ],
        axis=1,
    ).max(axis=1)



    # =================================
    # Directional Movement
    # =================================

    up_move = (
        high
        -
        high.shift(1)
    )

    down_move = (
        low.shift(1)
        -
        low
    )


    plus_dm = pd.Series(
        0.0,
        index=data.index
    )

    minus_dm = pd.Series(
        0.0,
        index=data.index
    )


    plus_dm[
        (
            up_move > down_move
        )
        &
        (
            up_move > 0
        )
    ] = up_move


    minus_dm[
        (
            down_move > up_move
        )
        &
        (
            down_move > 0
        )
    ] = down_move



    # =================================
    # Wilder smoothing
    # =================================

    atr = rma(
        tr,
        PERIOD
    )


    plus_di = (
        100
        *
        rma(
            plus_dm,
            PERIOD
        )
        /
        atr
    )


    minus_di = (
        100
        *
        rma(
            minus_dm,
            PERIOD
        )
        /
        atr
    )



    # =================================
    # DX
    # =================================

    di_sum = (
        plus_di
        +
        minus_di
    )


    dx = (
        (
            plus_di
            -
            minus_di
        )
        .abs()
        /
        di_sum.replace(
            0,
            pd.NA
        )
    ) * 100


    dx = dx.fillna(0)



    # =================================
    # ADX (Wilder / TradingView style)
    # =================================

    adx = pd.Series(
        index=dx.index,
        dtype=float
    )


    if len(dx) >= PERIOD:

        adx.iloc[PERIOD - 1] = (
            dx.iloc[:PERIOD]
            .mean()
        )


        for i in range(
            PERIOD,
            len(dx)
        ):

            adx.iloc[i] = (
                (
                    adx.iloc[i - 1]
                    *
                    (PERIOD - 1)
                )
                +
                dx.iloc[i]
            ) / PERIOD



    result["ADX"] = adx

    result["+DI"] = plus_di

    result["-DI"] = minus_di



    # =================================
    # Direction
    # =================================

    result["DI_DIRECTION"] = (
        result["+DI"]
        >
        result["-DI"]
    ).map(
        {
            True: "UP",
            False: "DOWN",
        }
    )



    # =================================
    # Trend
    # =================================

    result["TREND_ON"] = (
        result["ADX"]
        >=
        TREND_ON
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