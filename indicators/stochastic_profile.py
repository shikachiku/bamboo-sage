from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )


import pandas as pd

from settings import DATA_PATH
from symbol_loader import load_symbols


# ==========================================
# Parameter
# ==========================================



TIMEFRAMES = [
    "1M",
    "1W",
    "1D",
    "4H",
]



# ==========================================
# STATE
# ==========================================

def get_state(k, d):

    if k > d:

        return "UP"

    else:

        return "DOWN"



# ==========================================
# CROSS
# ==========================================

def get_cross(k_series, d_series):


    if len(k_series) < 2:

        return "NONE"



    prev_k = k_series.iloc[-2]

    prev_d = d_series.iloc[-2]


    current_k = k_series.iloc[-1]

    current_d = d_series.iloc[-1]



    if (

        prev_k <= prev_d

        and

        current_k > current_d

    ):

        return "GOLDEN"



    elif (

        prev_k >= prev_d

        and

        current_k < current_d

    ):

        return "DEAD"



    else:

        return "NONE"



# ==========================================
# ZONE
# ==========================================

def get_zone(value):


    if value >= 80:

        return "OVERBOUGHT"


    elif value <= 20:

        return "OVERSOLD"


    else:

        return "MIDDLE"



# ==========================================
# WAVE
# ==========================================

def get_wave(series):


    if len(series) < 2:

        return "NONE"



    current = series.iloc[-1]

    previous = series.iloc[-2]



    if current > previous:

        return "RISING"


    elif current < previous:

        return "FALLING"


    else:

        return "FLAT"



# ==========================================
# PROFILE
# ==========================================

def create_profile(stoch, tf):


    current_k = stoch["STOCH_K"].iloc[-1]

    current_d = stoch["STOCH_D"].iloc[-1]



    minimum = stoch["STOCH_K"].min()

    maximum = stoch["STOCH_K"].max()

    average = stoch["STOCH_K"].mean()



    if maximum != minimum:

        position = (

            current_k - minimum

        ) / (

            maximum - minimum

        )


    else:

        position = 0



    profile = {


        "CURRENT_K":

            round(
                current_k,
                3
            ),



        "CURRENT_D":

            round(
                current_d,
                3
            ),



        "K_MIN":

            round(
                minimum,
                3
            ),



        "K_MAX":

            round(
                maximum,
                3
            ),



        "K_AVERAGE":

            round(
                average,
                3
            ),



        "POSITION":

            round(
                position,
                3
            ),



        "STATE":

            get_state(
                current_k,
                current_d
            ),



        "CROSS":

            get_cross(
                stoch["STOCH_K"],
                stoch["STOCH_D"]
            ),



        "ZONE":

            get_zone(
                current_k
            ),



        "WAVE":

            get_wave(
                stoch["STOCH_K"]
            ),



        "DATA_USED":

            len(stoch),

    }


    return profile



# ==========================================
# PROCESS
# ==========================================

def process(
    symbol,
    tf,
):


    input_csv = (

        DATA_PATH

        /

        symbol["Folder"]

        /

        "indicator"

        /

        "stochastic"

        /

        f"{tf}.csv"

    )


    if not input_csv.exists():

        return



    output_csv = (

        DATA_PATH

        /

        symbol["Folder"]

        /

        "profile"

        /

        f"STOCHASTIC_PROFILE_{tf}.csv"

    )



    stoch = pd.read_csv(

        input_csv,

        index_col=0,

        parse_dates=True,

    )



    profile = create_profile(

        stoch,

        tf,

    )



    output_csv.parent.mkdir(

        parents=True,

        exist_ok=True,

    )



    df = pd.DataFrame(

        profile.items(),

        columns=[

            "ITEM",

            "VALUE",

        ],

    )



    df.to_csv(

        output_csv,

        index=False,

    )



    print(
        f"Saved -> {output_csv}"
    )



# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":


    print()

    print("==============================")

    print("STOCHASTIC PROFILE START")

    print("==============================")


    symbols = load_symbols()



    for symbol in symbols:


        print()

        print("=" * 60)

        print(symbol["Name"])

        print("=" * 60)



        for tf in TIMEFRAMES:


            process(

                symbol,

                tf,

            )



    print()

    print("==============================")

    print("STOCHASTIC PROFILE Complete")

    print("==============================")