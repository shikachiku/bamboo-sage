import pandas as pd

from indicator_base import run_indicator


# ======================================
# Parameter
# ======================================

INDICATOR = "highlow"


LENGTHS = [
    5,
    10,
    20,
    60,
]


# ======================================
# High Low Engine
# ======================================

def calculate(data):

    result = data.copy()


    for length in LENGTHS:


        # --------------------------
        # High MA
        # --------------------------

        high_name = f"High{length}MA"

        result[high_name] = (
            data["High"]
            .rolling(length)
            .mean()
        )


        # --------------------------
        # Low MA
        # --------------------------

        low_name = f"Low{length}MA"

        result[low_name] = (
            data["Low"]
            .rolling(length)
            .mean()
        )


        # --------------------------
        # Distance
        # --------------------------

        result[f"DIST_TO_HIGH{length}"] = (
            result[high_name]
            -
            result["Close"]
        )


        result[f"DIST_TO_LOW{length}"] = (
            result["Close"]
            -
            result[low_name]
        )


        # --------------------------
        # Break
        # --------------------------

        result[f"BREAK_HIGH{length}"] = (
            result["Close"]
            >
            result[high_name]
        )


        result[f"BREAK_LOW{length}"] = (
            result["Close"]
            <
            result[low_name]
        )


        # --------------------------
        # Stop
        # --------------------------

        result[f"STOP_PRICE_{length}"] = (
            result[low_name]
        )


        result[f"RISK_{length}"] = (
            result["Close"]
            -
            result[f"STOP_PRICE_{length}"]
        )


    return result



# ======================================
# MAIN
# ======================================

if __name__ == "__main__":

    run_indicator(
        INDICATOR,
        calculate,
    )