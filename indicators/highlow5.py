import pandas as pd


# ======================================
# Parameter
# ======================================

INDICATOR = "highlow5"

LENGTH = 5


# ======================================
# High Low 5
# Heikin Ashi based
# Previous period only
# ======================================

def calculate(data):

    result = data.copy()


    # ----------------------------
    # Previous HA High / Low 5 MA
    # ----------------------------

    result["High5MA"] = (
        data["HA_High"]
        .shift(1)
        .rolling(LENGTH)
        .mean()
    )


    result["Low5MA"] = (
        data["HA_Low"]
        .shift(1)
        .rolling(LENGTH)
        .mean()
    )


    # ----------------------------
    # Distance
    # HA_Close based
    # ----------------------------

    result["DIST_TO_HIGH5"] = (
        result["High5MA"]
        -
        result["HA_Close"]
    )


    result["DIST_TO_LOW5"] = (
        result["HA_Close"]
        -
        result["Low5MA"]
    )


    # ----------------------------
    # Break
    # HA_Close based
    # ----------------------------

    result["BREAK_HIGH5"] = (
        result["HA_Close"]
        >
        result["High5MA"]
    )


    result["BREAK_LOW5"] = (
        result["HA_Close"]
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
        result["HA_Close"]
        -
        result["STOP_PRICE_5"]
    )


    return result