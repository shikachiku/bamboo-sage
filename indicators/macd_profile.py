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
# MACD STATE
# ==========================================

def get_macd_state(macd, signal):

    if macd > signal:

        return "BULL"

    else:

        return "BEAR"



# ==========================================
# HISTOGRAM STATE
# ==========================================

def get_hist_state(hist_series):

    if len(hist_series) < 2:

        return "NONE"


    current = hist_series.iloc[-1]

    previous = hist_series.iloc[-2]


    if current > previous:

        return "EXPANDING"


    elif current < previous:

        return "CONTRACTING"


    else:

        return "FLAT"



# ==========================================
# CROSS
# ==========================================

def get_cross(macd_series, signal_series):


    if len(macd_series) < 2:

        return "NONE"


    prev_macd = macd_series.iloc[-2]

    prev_signal = signal_series.iloc[-2]


    current_macd = macd_series.iloc[-1]

    current_signal = signal_series.iloc[-1]



    if (
        prev_macd <= prev_signal
        and
        current_macd > current_signal
    ):

        return "GOLDEN"



    elif (
        prev_macd >= prev_signal
        and
        current_macd < current_signal
    ):

        return "DEAD"



    else:

        return "NONE"



# ==========================================
# ZERO LINE ZONE
# ==========================================

def get_zone(value):

    if value >= 0:

        return "ABOVE_ZERO"

    else:

        return "BELOW_ZERO"



# ==========================================
# PROFILE
# ==========================================

def create_profile(macd, tf):


    current_macd = macd["MACD"].iloc[-1]

    current_signal = macd["MACD_SIGNAL"].iloc[-1]

    current_hist = macd["MACD_HIST"].iloc[-1]



    minimum = macd["MACD_HIST"].min()

    maximum = macd["MACD_HIST"].max()

    average = macd["MACD_HIST"].mean()

    median = macd["MACD_HIST"].median()

    std = macd["MACD_HIST"].std()



    if maximum != minimum:

        position = (
            current_hist - minimum
        ) / (
            maximum - minimum
        )

    else:

        position = 0



    profile = {


        "CURRENT_MACD": round(
            current_macd,
            3
        ),


        "CURRENT_SIGNAL": round(
            current_signal,
            3
        ),


        "CURRENT_HIST": round(
            current_hist,
            3
        ),



        "HIST_MIN": round(
            minimum,
            3
        ),


        "HIST_MAX": round(
            maximum,
            3
        ),


        "HIST_AVERAGE": round(
            average,
            3
        ),


        "HIST_MEDIAN": round(
            median,
            3
        ),


        "HIST_STD": round(
            std,
            3
        ),



        "POSITION": round(
            position,
            3
        ),



        "ZONE": get_zone(
            current_hist
        ),



        "STATE": get_macd_state(
            current_macd,
            current_signal,
        ),



        "CROSS": get_cross(
            macd["MACD"],
            macd["MACD_SIGNAL"],
        ),



        "HIST_STATE": get_hist_state(
            macd["MACD_HIST"]
        ),



        "DATA_USED":

            len(macd),


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

        "macd"

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

        f"MACD_PROFILE_{tf}.csv"

    )



    macd = pd.read_csv(

        input_csv,

        index_col=0,

        parse_dates=True,

    )



    profile = create_profile(

        macd,

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

    print("MACD PROFILE START")

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

    print("MACD PROFILE Complete")

    print("==============================")