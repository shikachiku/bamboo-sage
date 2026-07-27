from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import os
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


# ======================================
# Read Profile
# ======================================

def load_profile(
    symbol,
    name,
    tf,
):

    file = (
        DATA_PATH
        / symbol["Folder"]
        / "profile"
        / f"{name}_PROFILE_{tf}.csv"
    )


    if not file.exists():

        return {}


    df = pd.read_csv(file)


    values = {}


    for _, row in df.iterrows():

        values[row["ITEM"]] = row["VALUE"]


    return values



# ======================================
# Convert Stars
# ======================================

def stars_to_score(stars):

    table = {

        "★★★★★": 5,
        "★★★★☆": 4,
        "★★★☆☆": 3,
        "★★☆☆☆": 2,
        "★☆☆☆☆": 1,

    }


    return table.get(
        stars,
        0,
    )



# ======================================
# Build Master
# ======================================

def build_master(
    symbol,
    tf,
):

    adx = load_profile(
        symbol,
        "ADX",
        tf,
    )


    highlow = load_profile(
        symbol,
        "HIGHLOW",
        tf,
    )


    highlow5 = load_profile(
        symbol,
        "HIGHLOW5",
        tf,
    )


    trend = load_profile(
        symbol,
        "TREND",
        tf,
    )


    master = {}


    # =====================================
    # Basic
    # =====================================

    master["SYMBOL"] = symbol["Name"]

    master["TIMEFRAME"] = tf



    # =====================================
    # ADX
    # =====================================

    master["ADX_ZONE"] = adx.get(
        "ZONE"
    )


    master["ADX_STATE"] = adx.get(
        "STATE"
    )


    master["ADX_TREND"] = adx.get(
        "TREND_STRENGTH"
    )



    # =====================================
    # HIGHLOW
    # =====================================

    master["HIGHLOW_SCORE"] = highlow.get(
        "BREAK_SCORE"
    )


    master["HIGHLOW_ZONE"] = highlow.get(
        "BUY_ZONE"
    )


    master["HIGHLOW_STATE"] = highlow.get(
        "STATE"
    )



    # =====================================
    # HIGHLOW5
    # =====================================

    master["HIGHLOW5_SCORE"] = highlow5.get(
        "BREAK_SCORE"
    )


    master["HIGHLOW5_ZONE"] = highlow5.get(
        "BUY_ZONE"
    )


    master["HIGHLOW5_STATE"] = highlow5.get(
        "STATE"
    )



    # =====================================
    # TREND
    # =====================================

    master["TREND_STATE"] = trend.get(
        "STATE"
    )


    master["TREND_DIRECTION"] = trend.get(
        "TREND"
    )


    master["TREND_ZONE"] = trend.get(
        "BUY_ZONE"
    )



    # =====================================
    # AI SCORE
    # =====================================

    score = 0


    score += stars_to_score(
        highlow.get(
            "BUY_ZONE"
        )
    )


    score += stars_to_score(
        highlow5.get(
            "BUY_ZONE"
        )
    )


    score += stars_to_score(
        "★★★★★"
        if adx.get("STATE") == "READY"
        else
        "★★★☆☆"
    )


    score += stars_to_score(
        trend.get(
            "BUY_ZONE"
        )
    )



    master["AI_SCORE"] = score



    # =====================================
    # AI ZONE
    # =====================================

    if score >= 17:

        ai = "★★★★★"


    elif score >= 13:

        ai = "★★★★☆"


    elif score >= 9:

        ai = "★★★☆☆"


    elif score >= 5:

        ai = "★★☆☆☆"


    else:

        ai = "★☆☆☆☆"



    master["AI_ZONE"] = ai



    return master



# ======================================
# Save
# ======================================

def process(
    symbol,
    tf,
):

    master = build_master(
        symbol,
        tf,
    )


    output_dir = (
        DATA_PATH
        /
        symbol["Folder"]
        /
        "master"
    )


    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )


    output = (
        output_dir
        /
        f"{tf}.csv"
    )



    df = pd.DataFrame(
        master.items(),
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
        f"Saved : {output}"
    )



# ======================================
# MAIN
# ======================================

def main():

    print("=" * 40)
    print("MASTER START")
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
    print("MASTER COMPLETE")
    print("=" * 40)



if __name__ == "__main__":

    main()