import pandas as pd


# ======================================
# Parameter
# ======================================

INDICATOR = "swing"

SWING_LENGTH = 5


# ======================================
# Swing High / Low
# Vectorized
# ======================================

def calculate(data):

    result = data.copy()


    result["SWING_HIGH"] = False
    result["SWING_LOW"] = False


    high = result["High"]
    low = result["Low"]


    # ==================================
    # Left / Right Range
    # ==================================

    left_high = (
        high
        .rolling(
            window=SWING_LENGTH,
            min_periods=SWING_LENGTH
        )
        .max()
        .shift(1)
    )


    right_high = (
        high
        .rolling(
            window=SWING_LENGTH,
            min_periods=SWING_LENGTH
        )
        .max()
        .shift(
            -(SWING_LENGTH)
        )
    )



    left_low = (
        low
        .rolling(
            window=SWING_LENGTH,
            min_periods=SWING_LENGTH
        )
        .min()
        .shift(1)
    )


    right_low = (
        low
        .rolling(
            window=SWING_LENGTH,
            min_periods=SWING_LENGTH
        )
        .min()
        .shift(
            -(SWING_LENGTH)
        )
    )



    # ==================================
    # Swing High
    # current_high >= left_high
    # current_high > right_high
    # ==================================

    swing_high = (
        (high >= left_high)
        &
        (high > right_high)
    )


    # ==================================
    # Swing Low
    # current_low <= left_low
    # current_low < right_low
    # ==================================

    swing_low = (
        (low <= left_low)
        &
        (low < right_low)
    )



    # ==================================
    # Latest future unavailable rows
    # remain False
    # ==================================

    result["SWING_HIGH"] = (
        swing_high
        .fillna(False)
    )


    result["SWING_LOW"] = (
        swing_low
        .fillna(False)
    )


    return result