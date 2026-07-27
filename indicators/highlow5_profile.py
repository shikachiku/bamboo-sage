from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import os
import pandas as pd

from settings import DATA_PATH


# ======================================
# Parameter
# ======================================

BASE = DATA_PATH

SYMBOL = "WHSELFINVEST_JAPAN225CFD"

TIMEFRAMES = [
    "1M",
    "1W",
    "1D",
    "4H",
]


# ======================================
# Profile
# ======================================

def create_profile(data):

    profile = {}

    profile["CURRENT_CLOSE"] = round(
        data["Close"].iloc[-1],
        3,
    )


    # -----------------------------
    # BREAK SCORE
    # -----------------------------

    score = 0

    if data["BREAK_HIGH5"].iloc[-1]:

        score = 5


    profile["BREAK_SCORE"] = score


    # -----------------------------
    # BUY ZONE
    # -----------------------------

    if score == 5:

        stars = "★★★★★"

    elif score >= 4:

        stars = "★★★★☆"

    elif score >= 3:

        stars = "★★★☆☆"

    elif score >= 2:

        stars = "★★☆☆☆"

    else:

        stars = "★☆☆☆☆"


    profile["BUY_ZONE"] = stars


    # -----------------------------
    # STATE
    # -----------------------------

    if score == 5:

        state = "BREAK"

    elif score >= 3:

        state = "READY"

    else:

        state = "WAIT"


    profile["STATE"] = state


    # -----------------------------
    # HIGH LOW 5 DATA
    # -----------------------------

    profile["High5MA"] = round(
        data["High5MA"].iloc[-1],
        3,
    )


    profile["Low5MA"] = round(
        data["Low5MA"].iloc[-1],
        3,
    )


    profile["DIST_TO_HIGH5"] = round(
        data["DIST_TO_HIGH5"].iloc[-1],
        3,
    )


    profile["DIST_TO_LOW5"] = round(
        data["DIST_TO_LOW5"].iloc[-1],
        3,
    )


    profile["BREAK_HIGH5"] = (
        data["BREAK_HIGH5"].iloc[-1]
    )


    profile["BREAK_LOW5"] = (
        data["BREAK_LOW5"].iloc[-1]
    )


    # -----------------------------
    # STOP
    # -----------------------------

    profile["STOP_PRICE"] = round(
        data["STOP_PRICE_5"].iloc[-1],
        3,
    )


    profile["RISK"] = round(
        data["RISK_5"].iloc[-1],
        3,
    )


    return profile



# ======================================
# Process
# ======================================

def process(tf):


    # 修正済み
    # indicator/highlow5 を読む

    input_csv = (
        f"{BASE}/{SYMBOL}/indicator/highlow5/{tf}.csv"
    )


    output_csv = (
        f"{BASE}/{SYMBOL}/profile/HIGHLOW5_PROFILE_{tf}.csv"
    )


    data = pd.read_csv(
        input_csv,
        index_col=0,
        parse_dates=True,
    )


    profile = create_profile(data)


    os.makedirs(
        os.path.dirname(output_csv),
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


    for tf in TIMEFRAMES:

        process(tf)


    print()

    print("==============================")

    print("HIGHLOW5 PROFILE Complete")

    print("==============================")