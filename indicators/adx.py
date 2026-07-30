from pathlib import Path
import sys

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

# Threshold
TREND_ON = 5



# ===================================
# Wilder RMA
# ===================================

def rma(series, length):

    result = pd.Series(
        index=series.index,
        dtype=float
    )

    if len(series) == 0:
        return result


    # Pine v4 style:
    # x := nz(x[1]) - nz(x[1])/length + value

    result.iloc[0] = series.iloc[0]


    for i in range(
        1,
        len(series)
    ):

        result.iloc[i] = (
            result.iloc[i - 1]
            -
            (
                result.iloc[i - 1]
                /
                length
            )
            +
            series.iloc[i]
        )


    return result



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
    # =================================

    tr = pd.Series(
        0.0,
        index=df.index
    )


    for i in range(len(df)):

        if i == 0:
            tr.iloc[i] = 0.0

        else:

            tr.iloc[i] = max(
                high.iloc[i] - low.iloc[i],
                abs(
                    high.iloc[i]
                    -
                    close.iloc[i - 1]
                ),
                abs(
                    low.iloc[i]
                    -
                    close.iloc[i - 1]
                )
            )



    # =================================
    # Directional Movement
    # =================================

    plus_dm = pd.Series(
        0.0,
       index=df.index
    )

    minus_dm = pd.Series(
        0.0,
        index=df.index
    )


    for i in range(1, len(df)):

        up_move = (
            high.iloc[i]
            -
            high.iloc[i - 1]
        )

        down_move = (
            low.iloc[i - 1]
            -
            low.iloc[i]
        )


        if (
            up_move > down_move
            and
            up_move > 0
        ):

            plus_dm.iloc[i] = up_move


        elif (
            down_move > up_move
            and
            down_move > 0
        ):

            minus_dm.iloc[i] = down_move



    # =================================
    # Pine v4 Wilder smoothing
    # Start from 0.0
    # =================================

    smooth_tr = pd.Series(
        0.0,
        index=df.index
    )

    smooth_plus = pd.Series(
        0.0,
        index=df.index
    )

    smooth_minus = pd.Series(
        0.0,
        index=df.index
    )


    for i in range(len(df)):

        smooth_tr.iloc[i] = (
            (
                smooth_tr.iloc[i - 1]
                if i > 0
                else 0.0
            )
            -
            (
                (
                    smooth_tr.iloc[i - 1]
                    if i > 0
                    else 0.0
                )
                /
                PERIOD
            )
            +
            tr.iloc[i]
        )


        smooth_plus.iloc[i] = (
            (
                smooth_plus.iloc[i - 1]
                if i > 0
                else 0.0
            )
            -
            (
                (
                    smooth_plus.iloc[i - 1]
                    if i > 0
                    else 0.0
                )
                /
                PERIOD
            )
            +
            plus_dm.iloc[i]
        )


        smooth_minus.iloc[i] = (
            (
                smooth_minus.iloc[i - 1]
                if i > 0
                else 0.0
            )
            -
            (
                (
                    smooth_minus.iloc[i - 1]
                    if i > 0
                    else 0.0
                )
                /
                PERIOD
            )
            +
            minus_dm.iloc[i]
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


    plus_di = plus_di.fillna(0)

    minus_di = minus_di.fillna(0)



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
    ) * 100


    dx = dx.replace(
        [float("inf")],
        0
    )

    dx = dx.fillna(0)



    # =================================
    # ADX
    # Pine v4:
    # ADX = SMA(DX, PERIOD)
    # =================================

    adx = (
        dx
        .rolling(
            PERIOD
        )
        .mean()
    )


    result["ADX"] = adx

    result["+DI"] = plus_di

    result["-DI"] = minus_di
    
    
        # =================================
    # ADX Level
    # Historical Relative Position
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
        .fillna(0)
    )


    # =================================
    # ADX Slope
    # =================================

    result["ADX_SLOPE"] = (
        result["ADX"]
        -
        result["ADX"]
        .shift(1)
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

