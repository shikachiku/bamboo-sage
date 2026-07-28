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


# ======================================
# Parameter
# ======================================

TIMEFRAMES = [
    "1D",
    "4H",
]


# ======================================
# Load Profile
# ======================================

def load_profile(
    symbol,
    name,
    tf,
):

    file = (

        DATA_PATH

        /

        symbol["Folder"]

        /

        "profile"

        /

        f"{name}_PROFILE_{tf}.csv"

    )


    if not file.exists():

        print(
            f"Profile Not Found : {file}"
        )

        return None



    df = pd.read_csv(
        file
    )


    profile = {}


    for _, row in df.iterrows():

        profile[row["ITEM"]] = row["VALUE"]


    return profile


# ======================================
# Fibonacci 50%
# ======================================

def calculate(
    monthly,
    weekly,
):


    result = {}


    # ==================================
    # Swing Data
    # ==================================

    month_high = float(
        monthly["LAST_SWING_HIGH"]
    )


    month_low = float(
        monthly["LAST_SWING_LOW"]
    )


    week_high = float(
        weekly["LAST_SWING_HIGH"]
    )


    week_low = float(
        weekly["LAST_SWING_LOW"]
    )



    # ==================================
    # Trend Judge
    # ==================================

    if week_high >= month_high:

        trend = "UP"


    else:

        trend = "DOWN"



    # ==================================
    # Fibonacci 50%
    # ==================================

    if trend == "UP":


        start_price = month_low

        end_price = week_high


        half_price = (

            start_price

            +

            (

                end_price

                -

                start_price

            )

            *

            0.5

        )


    else:


        start_price = month_high

        end_price = week_low


        half_price = (

            start_price

            -

            (

                start_price

                -

                end_price

            )

            *

            0.5

        )



    # ==================================
    # Result
    # ==================================

    result["TREND"] = trend


    result["START_PRICE"] = round(
        start_price,
        3
    )


    result["END_PRICE"] = round(
        end_price,
        3
    )


    result["HALF_PRICE"] = round(
        half_price,
        3
    )


    result["MONTH_HIGH"] = round(
        month_high,
        3
    )


    result["MONTH_LOW"] = round(
        month_low,
        3
    )


    result["WEEK_HIGH"] = round(
        week_high,
        3
    )


    result["WEEK_LOW"] = round(
        week_low,
        3
    )


    return result

# ======================================
# Process
# ======================================

def process(symbol):


    # ==================================
    # Load Monthly Swing
    # ==================================

    monthly = load_profile(
        symbol,
        "SWING",
        "1M",
    )


    if monthly is None:

        return



    # ==================================
    # Load Weekly Swing
    # ==================================

    weekly = load_profile(
        symbol,
        "SWING",
        "1W",
    )


    if weekly is None:

        return



    # ==================================
    # Calculate
    # ==================================

    fibonacci = calculate(
        monthly,
        weekly,
    )



    # ==================================
    # Save
    # ==================================

    output_dir = (

        DATA_PATH

        /

        symbol["Folder"]

        /

        "indicator"

        /

        "fibonacci"

    )


    output_dir.mkdir(

        parents=True,

        exist_ok=True,

    )



    output = (

        output_dir

        /

        "1D.csv"

    )



    df = pd.DataFrame(

        fibonacci.items(),

        columns=[

            "ITEM",

            "VALUE",

        ],

    )


    df.to_csv(

        output,

        index=False,

    )


    print(
        f"Saved -> {output}"
    )
    
# ======================================
# MAIN
# ======================================

if __name__ == "__main__":


    print()

    print("==============================")

    print("FIBONACCI START")

    print("==============================")



    symbols = load_symbols()



    for symbol in symbols:


        print()

        print("=" * 60)

        print(symbol["Name"])

        print("=" * 60)



        process(
            symbol
        )



    print()

    print("==============================")

    print("FIBONACCI Complete")

    print("==============================")