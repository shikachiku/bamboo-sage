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
        .rolling(LENGTH)
        .min()
    )


    highest_high = (
        high
        .rolling(LENGTH)
        .max()
    )



    # ===================================
    # Raw %K
    # ===================================

    raw_k = (
        (
            close - lowest_low
        )
        /
        (
            highest_high - lowest_low
        )
    ) * 100


    raw_k = raw_k.fillna(0)



    # ===================================
    # Smooth K
    # ===================================

    stoch_k = (
        raw_k
        .rolling(SMOOTH_K)
        .mean()
    )



    # ===================================
    # Smooth D
    # ===================================

    stoch_d = (
        stoch_k
        .rolling(SMOOTH_D)
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

            cross.append("NONE")

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



    # ===================================
    # Wave Detection
    # ===================================

    high_touch = []

    wave_break = []

    wave_state = []


    touched = False

    waiting = False



    for i in range(len(result)):


        k = result["STOCH_K"].iloc[i]

        signal = result["STOCH_CROSS"].iloc[i]



        # -------------------------------
        # Golden Cross
        # -------------------------------

        if signal == "GOLDEN":

            waiting = True

            touched = False



        # -------------------------------
        # 80到達
        # -------------------------------

        if waiting:

            if k >= 80:

                touched = True

                waiting = False



        # -------------------------------
        # Dead Cross
        # -------------------------------

        if signal == "DEAD":

            if waiting and not touched:

                wave_break.append(True)

                wave_state.append(
                    "BREAK"
                )

                waiting = False

                touched = False

            else:

                wave_break.append(False)

                if touched:

                    wave_state.append(
                        "RISING"
                    )

                else:

                    wave_state.append(
                        "NONE"
                    )

        else:

            wave_break.append(False)


            if touched:

                wave_state.append(
                    "RISING"
                )

            elif waiting:

                wave_state.append(
                    "WAIT_HIGH"
                )

            else:

                wave_state.append(
                    "NONE"
                )



        high_touch.append(touched)



    result["STOCH_HIGH_TOUCH"] = high_touch

    result["STOCH_WAVE_BREAK"] = wave_break

    result["STOCH_WAVE_STATE"] = wave_state



    return result