from pathlib import Path
import sys
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )

import pandas as pd


# ===================================
# Parameter
# ===================================

INDICATOR = "adx"

# TradingView Pine v4
PERIOD = 10

# ADX smoothing
ADX_SMOOTH = 5

# Threshold
TREND_ON = 5



# ===================================
# Wilder RMA
# Pine style
# ===================================

def rma(series, length):

    import numpy as np

    if len(series) == 0:

        return pd.Series(
            index=series.index,
            dtype=float
        )


    values = series.to_numpy(
        dtype=float
    )


    result = np.empty(
        len(values),
        dtype=float
    )


    # ---------------------------------
    # Pine style seed
    # ---------------------------------

    result[0] = values[0]


    for i in range(
        1,
        len(values)
    ):

        result[i] = (
            (
                result[i - 1]
                *
                (length - 1)
            )
            +
            values[i]
        ) / length


    return pd.Series(
        result,
        index=series.index
    )



# ===================================
# ADX Calculation
# TradingView Pine v4 style
# ===================================

def calculate(df):

    result = df.copy()


    high = result["High"]
    low = result["Low"]
    close = result["Close"]


    # =================================
    # True Range
    # Vectorized
    # =================================

    prev_close = close.shift(1)


    tr1 = high - low

    tr2 = (
        high
        -
        prev_close
    ).abs()

    tr3 = (
        low
        -
        prev_close
    ).abs()


    tr = pd.concat(
        [
            tr1,
            tr2,
            tr3,
        ],
        axis=1
    ).max(
        axis=1
    )


    # First bar = High-Low

    tr.iloc[0] = (
        high.iloc[0]
        -
        low.iloc[0]
    )



    # =================================
    # Directional Movement
    # Vectorized
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
        index=df.index
    )


    minus_dm = pd.Series(
        0.0,
        index=df.index
    )


    plus_condition = (
        (up_move > down_move)
        &
        (up_move > 0)
    )


    minus_condition = (
        (down_move > up_move)
        &
        (down_move > 0)
    )


    plus_dm.loc[
        plus_condition
    ] = up_move.loc[
        plus_condition
    ]


    minus_dm.loc[
        minus_condition
    ] = down_move.loc[
        minus_condition
    ]



    # =================================
    # Wilder RMA
    # =================================

    smooth_tr = rma(
        tr,
        PERIOD
    )


    smooth_plus = rma(
        plus_dm,
        PERIOD
    )


    smooth_minus = rma(
        minus_dm,
        PERIOD
    )



    # =================================
    # DI
    # =================================

    plus_di = (
        smooth_plus
        /
        smooth_tr
        *
        100
    )


    minus_di = (
        smooth_minus
        /
        smooth_tr
        *
        100
    )


    plus_di = (
        plus_di
        .replace(
            [float("inf")],
            0
        )
        .fillna(0)
    )


    minus_di = (
        minus_di
        .replace(
            [float("inf")],
            0
        )
        .fillna(0)
    )



    # =================================
    # DX
    # =================================

    dx = (
        (
            plus_di
            -
            minus_di
        )
        .abs()
        /
        (
            plus_di
            +
            minus_di
        )
        *
        100
    )


    dx = (
        dx
        .replace(
            [float("inf")],
            0
        )
        .fillna(0)
    )



    # =================================
    # ADX
    # =================================

    adx = rma(
        dx,
        ADX_SMOOTH
    )


    result["ADX"] = adx

    result["+DI"] = plus_di

    result["-DI"] = minus_di



    # =================================
    # ADX Level
    # =================================

    adx_min = (
        result["ADX"]
        .expanding()
        .min()
    )


    adx_max = (
        result["ADX"]
        .expanding()
        .max()
    )


    result["ADX_LEVEL"] = (
        (
            result["ADX"]
            -
            adx_min
        )
        /
        (
            adx_max
            -
            adx_min
        )
    )


    result["ADX_LEVEL"] = (
        result["ADX_LEVEL"]
        .replace(
            [float("inf")],
            0
        )
        .fillna(0)
    )



    # =================================
    # ADX Slope
    # =================================

    result["ADX_SLOPE"] = (
        result["ADX"]
        -
        result["ADX"].shift(1)
    )


    result["ADX_SLOPE"] = (
        result["ADX_SLOPE"]
        .fillna(0)
    )



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