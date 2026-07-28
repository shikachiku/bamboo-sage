from pathlib import Path
import sys


# ======================================
# Project Root
# ======================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )



import os
import pandas as pd


from settings import DATA_PATH
from symbol_loader import load_symbols



# ======================================
# Parameter
# ======================================

BASE = DATA_PATH


TIMEFRAMES = [

    "1D",

]



# ======================================
# Load Fibonacci Indicator
# ======================================

def load_fibonacci(
    symbol,
    tf,
):


    file = (

        BASE

        /

        symbol["Folder"]

        /

        "indicator"

        /

        "fibonacci"

        /

        f"{tf}.csv"

    )


    if not file.exists():

        print(
            f"FIBONACCI Not Found : {file}"
        )

        return None



    df = pd.read_csv(
        file,
    )


    data = {}


    for _, row in df.iterrows():

        data[row["ITEM"]] = row["VALUE"]



    return data

# ======================================
# Create Profile
# ======================================

def create_profile(
    fibonacci,
    close,
):


    profile = {}



    # ==================================
    # Basic
    # ==================================

    trend = fibonacci.get(
        "TREND"
    )


    start_price = float(
        fibonacci.get(
            "START_PRICE"
        )
    )


    end_price = float(
        fibonacci.get(
            "END_PRICE"
        )
    )


    half_price = float(
        fibonacci.get(
            "HALF_PRICE"
        )
    )



    current_close = float(
        close
    )



    # ==================================
    # Distance
    # ==================================

    distance = (

        current_close

        -

        half_price

    )



    distance_rate = (

        distance

        /

        half_price

        *

        100

    )



    # ==================================
    # Zone
    # ==================================

    zone = "UNKNOWN"

    state = "UNKNOWN"



    # ------------------------------
    # UP Trend
    # ------------------------------

    if trend == "UP":


        if current_close >= half_price * 1.03:


            zone = "ABOVE_HALF"

            state = "WAIT_PULLBACK"



        elif current_close >= half_price * 0.97:


            zone = "HALF_ZONE"

            state = "BUY_WATCH"



        else:


            zone = "BELOW_HALF"

            state = "CAUTION"



    # ------------------------------
    # DOWN Trend
    # ------------------------------

    elif trend == "DOWN":


        if current_close <= half_price * 0.97:


            zone = "BELOW_HALF"

            state = "WAIT_REBOUND"



        elif current_close <= half_price * 1.03:


            zone = "HALF_ZONE"

            state = "SELL_WATCH"



        else:


            zone = "ABOVE_HALF"

            state = "CAUTION"



    # ==================================
    # Save
    # ==================================

    profile["TREND"] = trend


    profile["START_PRICE"] = round(
        start_price,
        3
    )


    profile["END_PRICE"] = round(
        end_price,
        3
    )


    profile["HALF_PRICE"] = round(
        half_price,
        3
    )


    profile["CURRENT_CLOSE"] = round(
        current_close,
        3
    )


    profile["DIST_TO_HALF"] = round(
        distance,
        3
    )


    profile["DIST_RATE"] = round(
        distance_rate,
        3
    )


    profile["ZONE"] = zone


    profile["STATE"] = state



    return profile


# ======================================
# Process
# ======================================

def process(
    symbol,
    tf,
):


    # ==================================
    # Load Fibonacci
    # ==================================

    fibonacci = load_fibonacci(
        symbol,
        tf,
    )


    if fibonacci is None:

        return



    # ==================================
    # Load RAW
    # ==================================

    raw_file = (

        BASE

        /

        symbol["Folder"]

        /

        "raw"

        /

        f"{tf}.csv"

    )


    if not raw_file.exists():

        print(
            f"RAW Not Found : {raw_file}"
        )

        return



    raw = pd.read_csv(

        raw_file,

        index_col=0,

        parse_dates=True,

    )



    current_close = raw["Close"].iloc[-1]



    # ==================================
    # Create Profile
    # ==================================

    profile = create_profile(

        fibonacci,

        current_close,

    )



    # ==================================
    # Save
    # ==================================

    output_csv = (

        BASE

        /

        symbol["Folder"]

        /

        "profile"

        /

        f"FIBONACCI_PROFILE_{tf}.csv"

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
    
    # ======================================
# MAIN
# ======================================

if __name__ == "__main__":


    print()

    print("==============================")

    print("FIBONACCI PROFILE START")

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

    print("FIBONACCI PROFILE Complete")

    print("==============================")