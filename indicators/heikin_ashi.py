import pandas as pd
import numpy as np

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

    ha_close = (
        result["Open"]
        + result["High"]
        + result["Low"]
        + result["Close"]
    ) / 4


    # ===================================
    # HA Open
    # NumPy
    # ===================================

    ha_close_np = ha_close.to_numpy()

    ha_open_np = np.empty(
        len(result),
        dtype=float,
    )

    ha_open_np[0] = (
        result["Open"].iloc[0]
        + result["Close"].iloc[0]
    ) / 2

    for i in range(1, len(result)):

        ha_open_np[i] = (
            ha_open_np[i - 1]
            + ha_close_np[i - 1]
        ) / 2

    result["HA_Close"] = ha_close
    result["HA_Open"] = ha_open_np


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


