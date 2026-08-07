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
    # State (NumPy)
    # ===================================

    result["STOCH_STATE"] = (
        pd.Series(
            (
                stoch_k.values
                >
                stoch_d.values
            ),
            index=result.index,
        )
        .map(
            {
                True: "UP",
                False: "DOWN",
            }
        )
    )



    # ===================================
    # Cross (NumPy)
    # ===================================

    k = stoch_k.values

    d = stoch_d.values


    cross = (
        [
            "NONE"
        ]
        *
        len(result)
    )


    golden = (
        (k[1:] > d[1:])
        &
        (k[:-1] <= d[:-1])
    )


    dead = (
        (k[1:] < d[1:])
        &
        (k[:-1] >= d[:-1])
    )


    cross_array = (
        result.index[1:]
    )


    for idx, g, de in zip(
        cross_array,
        golden,
        dead,
    ):

        if g:

            cross[
                result.index.get_loc(idx)
            ] = "GOLDEN"


        elif de:

            cross[
                result.index.get_loc(idx)
            ] = "DEAD"



    result["STOCH_CROSS"] = cross



    # ===================================
    # Zone (NumPy)
    # ===================================

    k_values = stoch_k.values


    zone = pd.Series(
        "MIDDLE",
        index=result.index,
    )


    zone.loc[
        k_values >= 80
    ] = "OVERBOUGHT"


    zone.loc[
        k_values <= 20
    ] = "OVERSOLD"


    result["STOCH_ZONE"] = zone



    # ===================================
    # Wave Detection
    # State machine
    # ===================================

    high_touch = []

    wave_break = []

    wave_state = []


    touched = False

    waiting = False



    for i in range(len(result)):


        k_value = k[i]

        signal = cross[i]



        if signal == "GOLDEN":

            waiting = True

            touched = False



        if waiting:

            if k_value >= 80:

                touched = True

                waiting = False



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