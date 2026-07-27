from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import pandas as pd

from settings import DATA_PATH
from symbol_loader import load_symbols


# ======================================
# Parameter
# ======================================

TIMEFRAMES = [
    "1M",
    "1W",
    "1D",
    "4H",
]


INDICATOR = "trend"


# ======================================
# Trend Profile
# ======================================

def create_profile(data):

    latest = data.iloc[-1]

    status = latest["TREND_STATUS"]


    profile = {}


    profile["STATE"] = status


    # --------------------------
    # Trend Direction
    # --------------------------

    if status in [
        "BLUE_CHANGE",
        "BLUE_CONTINUE",
    ]:

        profile["TREND"] = "UP"


    elif status in [
        "RED_CHANGE",
        "RED_CONTINUE",
    ]:

        profile["TREND"] = "DOWN"


    else:

        profile["TREND"] = "NONE"



    # --------------------------
    # BUY ZONE
    # --------------------------

    if status == "BLUE_CHANGE":

        profile["BUY_ZONE"] = "★★★★★"


    elif status == "BLUE_CONTINUE":

        profile["BUY_ZONE"] = "★★★★☆"


    elif status == "RED_CHANGE":

        profile["BUY_ZONE"] = "★★☆☆☆"


    else:

        profile["BUY_ZONE"] = "★☆☆☆☆"



    return profile



# ======================================
# Process
# ======================================

def process(symbol, tf):


    input_file = (
        DATA_PATH
        / symbol["Folder"]
        / "indicator"
        / "trend"
        / f"{tf}.csv"
    )


    if not input_file.exists():

        print(
            f"Skip : {input_file}"
        )

        return



    data = pd.read_csv(
        input_file,
        index_col=0,
        parse_dates=True,
    )


    profile = create_profile(
        data
    )


    output_dir = (
        DATA_PATH
        / symbol["Folder"]
        / "profile"
    )


    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )


    output_file = (
        output_dir
        /
        f"TREND_PROFILE_{tf}.csv"
    )


    df = pd.DataFrame(
        profile.items(),
        columns=[
            "ITEM",
            "VALUE",
        ],
    )


    df.to_csv(
        output_file,
        index=False,
    )


    print(
        f"Saved : {output_file}"
    )



# ======================================
# MAIN
# ======================================

def main():

    print("=" * 40)
    print("TREND PROFILE START")
    print("=" * 40)


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
    print("=" * 40)
    print("TREND PROFILE COMPLETE")
    print("=" * 40)



if __name__ == "__main__":

    main()