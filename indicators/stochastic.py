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

INDICATOR = "stochastic"


# TradingView setting
LENGTH = 5

SMOOTH_K = 5

SMOOTH_D = 3



# ===================================
# Stochastic Calculation
# ===================================

def calculate(data):

    result = data.copy()


    high = result["High"]

    low = result["Low"]

    close = result["Close"]



    # ===================================
    # Lowest / Highest
    # ===================================

    lowest_low = (
        low
        .rolling(
            LENGTH
        )
        .min()
    )


    highest_high = (
        high
        .rolling(
            LENGTH
        )
        .max()
    )



    # ===================================
    # Raw %K
    # ===================================

    raw_k = (

        (
            close
            -
            lowest_low
        )

        /

        (
            highest_high
            -
            lowest_low
        )

    ) * 100



    raw_k = raw_k.fillna(0)



    # ===================================
    # Smooth K
    # ===================================

    stoch_k = (

        raw_k

        .rolling(
            SMOOTH_K
        )

        .mean()

    )



    # ===================================
    # Smooth D
    # ===================================

    stoch_d = (

        stoch_k

        .rolling(
            SMOOTH_D
        )

        .mean()

    )



    result["STOCH_K"] = stoch_k

    result["STOCH_D"] = stoch_d



    # ===================================
    # State
    # ===================================

    result["STOCH_STATE"] = (

        result["STOCH_K"]

        >

        result["STOCH_D"]

    ).map(

        {
            True: "UP",

            False: "DOWN",

        }

    )



    # ===================================
    # Cross
    # ===================================

    cross = []

    for i in range(len(result)):


        if i == 0:

            cross.append(
                "NONE"
            )

            continue



        prev_k = result["STOCH_K"].iloc[i-1]

        prev_d = result["STOCH_D"].iloc[i-1]


        current_k = result["STOCH_K"].iloc[i]

        current_d = result["STOCH_D"].iloc[i]



        if (

            prev_k <= prev_d

            and

            current_k > current_d

        ):

            cross.append(
                "GOLDEN"
            )



        elif (

            prev_k >= prev_d

            and

            current_k < current_d

        ):

            cross.append(
                "DEAD"
            )


        else:

            cross.append(
                "NONE"
            )



    result["STOCH_CROSS"] = cross



    # ===================================
    # Zone
    # ===================================

    def zone(value):

        if value >= 80:

            return "OVERBOUGHT"


        elif value <= 20:

            return "OVERSOLD"


        else:

            return "MIDDLE"



    result["STOCH_ZONE"] = (

        result["STOCH_K"]

        .apply(zone)

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