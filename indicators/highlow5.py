import pandas as pd

from indicator_base import run_indicator


# ======================================
# Parameter
# ======================================

INDICATOR = "highlow5"

LENGTH = 5


# ======================================
# High Low 5
# ======================================

def calculate(data):

    result = data.copy()


    # ----------------------------
    # High5MA
    # ----------------------------

    result["High5MA"] = (
        data["High"]
        .rolling(LENGTH)
        .mean()
    )


    # ----------------------------
    # Low5MA
    # ----------------------------

    result["Low5MA"] = (
        data["Low"]
        .rolling(LENGTH)
        .mean()
    )


    # ----------------------------
    # Distance
    # ----------------------------

    result["DIST_TO_HIGH5"] = (
        result["High5MA"]
        -
        result["Close"]
    )


    result["DIST_TO_LOW5"] = (
        result["Close"]
        -
        result["Low5MA"]
    )


    # ----------------------------
    # Break
    # ----------------------------

    result["BREAK_HIGH5"] = (
        result["Close"]
        >
        result["High5MA"]
    )


    result["BREAK_LOW5"] = (
        result["Close"]
        <
        result["Low5MA"]
    )


    # ----------------------------
    # Stop
    # ----------------------------

    result["STOP_PRICE_5"] = (
        result["Low5MA"]
    )


    result["RISK_5"] = (
        result["Close"]
        -
        result["STOP_PRICE_5"]
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