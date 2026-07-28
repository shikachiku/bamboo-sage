import pandas as pd


# ===================================
# Parameter
# ===================================

INDICATOR = "heikin_ashi"


# ===================================
# Heikin Ashi
# ===================================

def calculate(data):

    result = data.copy()


    # ===================================
    # HA Close
    # ===================================

    result["HA_Close"] = (
        result["Open"]
        + result["High"]
        + result["Low"]
        + result["Close"]
    ) / 4


    # ===================================
    # HA Open
    # ===================================

    result["HA_Open"] = 0.0


    result.iloc[
        0,
        result.columns.get_loc("HA_Open")
    ] = (
        result["Open"].iloc[0]
        + result["Close"].iloc[0]
    ) / 2


    for i in range(1, len(result)):

        result.iloc[
            i,
            result.columns.get_loc("HA_Open")
        ] = (
            result["HA_Open"].iloc[i - 1]
            + result["HA_Close"].iloc[i - 1]
        ) / 2



    # ===================================
    # HA High
    # ===================================

    result["HA_High"] = (
        result[
            [
                "High",
                "HA_Open",
                "HA_Close",
            ]
        ]
        .max(axis=1)
    )


    # ===================================
    # HA Low
    # ===================================

    result["HA_Low"] = (
        result[
            [
                "Low",
                "HA_Open",
                "HA_Close",
            ]
        ]
        .min(axis=1)
    )


    # ===================================
    # HA Color
    # ===================================

    result["HA_COLOR"] = (
        result["HA_Close"]
        >
        result["HA_Open"]
    ).map(
        {
            True: "BLUE",
            False: "RED",
        }
    )


    return result


