from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import os
import pandas as pd

from settings import DATA_PATH


# ==========================================
# Parameter
# ==========================================

SYMBOL = "WHSELFINVEST_JAPAN225CFD"

TIMEFRAMES = [
    "1M",
    "1W",
    "1D",
    "4H",
]


# ==========================================
# ADX RULE
# ==========================================

def get_adx_state(tf, value):

    # ------------------------------
    # Monthly
    # ------------------------------

    if tf == "1M":

        if value < 20:
            return "NONE"

        elif value < 35:
            return "NORMAL"

        elif value < 50:
            return "STRONG"

        else:
            return "EXTREME"


    # ------------------------------
    # Weekly
    # ------------------------------

    elif tf == "1W":

        if value < 20:
            return "NONE"

        elif value < 35:
            return "NORMAL"

        elif value < 50:
            return "STRONG"

        elif value < 70:
            return "VERY_STRONG"

        else:
            return "SUPER_TREND"


    # ------------------------------
    # Daily
    # ------------------------------

    elif tf == "1D":

        if value < 20:
            return "NONE"

        elif value < 35:
            return "NORMAL"

        elif value < 50:
            return "STRONG"

        elif value < 70:
            return "VERY_STRONG"

        else:
            return "EXTREME"


    # ------------------------------
    # 4H
    # ------------------------------

    else:

        if value < 20:
            return "NONE"

        elif value < 35:
            return "NORMAL"

        elif value < 50:
            return "STRONG"

        elif value < 70:
            return "CAUTION"

        else:
            return "EXTREME"



# ==========================================
# ZONE
# ==========================================

def get_zone(tf, value):

    if tf == "1M":

        if value < 20:
            return "LOW"

        elif value < 35:
            return "NORMAL"

        elif value < 50:
            return "HIGH_NORMAL"

        else:
            return "HIGH"


    else:

        if value < 20:
            return "LOW"

        elif value < 35:
            return "NORMAL"

        elif value < 50:
            return "HIGH_NORMAL"

        else:
            return "HIGH"



# ==========================================
# PROFILE
# ==========================================

def create_profile(adx, tf):


    # ======================================
    # Monthly initial data exclusion
    # ======================================

    if tf == "1M" and len(adx) > 30:

        calc = adx.iloc[30:]

    else:

        calc = adx



    current = calc["ADX"].iloc[-1]

    minimum = calc["ADX"].min()

    maximum = calc["ADX"].max()

    average = calc["ADX"].mean()

    median = calc["ADX"].median()

    std = calc["ADX"].std()



    if maximum != minimum:

        position = (
            current - minimum
        ) / (
            maximum - minimum
        )

    else:

        position = 0



    state = get_adx_state(
        tf,
        current
    )


    zone = get_zone(
        tf,
        current
    )



    profile = {

        "CURRENT": round(
            current,
            3
        ),

        "MIN": round(
            minimum,
            3
        ),

        "MAX": round(
            maximum,
            3
        ),

        "AVERAGE": round(
            average,
            3
        ),

        "MEDIAN": round(
            median,
            3
        ),

        "STD": round(
            std,
            3
        ),

        "POSITION": round(
            position,
            3
        ),

        "ZONE": zone,

        "STATE": state,

        "TREND_STRENGTH": state,

        "DATA_USED":

            len(calc),

        "DATA_EXCLUDED":

            len(adx)-len(calc),

        "TO_MIN": round(
            current-minimum,
            3
        ),

        "TO_MAX": round(
            maximum-current,
            3
        ),

    }


    return profile



# ==========================================
# PROCESS
# ==========================================

def process(tf):


    input_csv = (
        DATA_PATH
        /
        SYMBOL
        /
        "indicator"
        /
        "adx"
        /
        f"{tf}.csv"
    )


    output_csv = (
        DATA_PATH
        /
        SYMBOL
        /
        "profile"
        /
        f"ADX_PROFILE_{tf}.csv"
    )


    adx = pd.read_csv(

        input_csv,

        index_col=0,

        parse_dates=True,

    )



    profile = create_profile(
        adx,
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


    for tf in TIMEFRAMES:

        process(tf)



    print()

    print("==============================")

    print("ADX PROFILE Complete")

    print("==============================")