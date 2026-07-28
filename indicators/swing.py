import pandas as pd

from indicator_base import run_indicator


# ======================================
# Parameter
# ======================================

INDICATOR = "swing"

SWING_LENGTH = 5


# ======================================
# Swing High / Low
# ======================================

def calculate(data):

    result = data.copy()

    result["SWING_HIGH"] = False
    result["SWING_LOW"] = False


    for i in range(
        SWING_LENGTH,
        len(result) - SWING_LENGTH,
    ):

        # -------------------------
        # Swing High
        # -------------------------

        current_high = result["High"].iloc[i]

        left_high = result["High"].iloc[
            i - SWING_LENGTH:i
        ].max()

        right_high = result["High"].iloc[
            i + 1:i + SWING_LENGTH + 1
        ].max()


        if (
            current_high > left_high
            and
            current_high > right_high
        ):

            result.iloc[
                i,
                result.columns.get_loc(
                    "SWING_HIGH"
                )
            ] = True


        # -------------------------
        # Swing Low
        # -------------------------

        current_low = result["Low"].iloc[i]

        left_low = result["Low"].iloc[
            i - SWING_LENGTH:i
        ].min()

        right_low = result["Low"].iloc[
            i + 1:i + SWING_LENGTH + 1
        ].min()


        if (
            current_low < left_low
            and
            current_low < right_low
        ):

            result.iloc[
                i,
                result.columns.get_loc(
                    "SWING_LOW"
                )
            ] = True


    return result


# ======================================
# MAIN
# ======================================

if __name__ == "__main__":

    run_indicator(
        INDICATOR,
        calculate,
    )