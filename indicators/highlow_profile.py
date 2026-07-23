import os
import pandas as pd

# ======================================
# Parameter
# ======================================

BASE = "data"

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

    score = 0

    # ----------------------------
    # Break Score
    # ----------------------------

    if data["BREAK_HIGH5"].iloc[-1]:
        score += 1

    if data["BREAK_HIGH10"].iloc[-1]:
        score += 2

    if data["BREAK_HIGH20"].iloc[-1]:
        score += 3

    if data["BREAK_HIGH60"].iloc[-1]:
        score += 4

    profile["BREAK_SCORE"] = score

    # ----------------------------
    # BUY ZONE
    # ----------------------------

    if score == 10:

        stars = "★★★★★"

    elif score >= 7:

        stars = "★★★★☆"

    elif score >= 4:

        stars = "★★★☆☆"

    elif score >= 1:

        stars = "★★☆☆☆"

    else:

        stars = "★☆☆☆☆"

    profile["BUY_ZONE"] = stars

    # ----------------------------
    # STATE
    # ----------------------------

    if score == 10:

        state = "SUPER_BREAK"

    elif score >= 7:

        state = "STRONG_BREAK"

    elif score >= 4:

        state = "BREAK"

    elif score >= 1:

        state = "EARLY_BREAK"

    else:

        state = "WAIT"

    profile["STATE"] = state

    # ----------------------------
    # Last Values
    # ----------------------------

    for length in [5, 10, 20, 60]:

        profile[f"High{length}MA"] = round(
            data[f"High{length}MA"].iloc[-1],
            3,
        )

        profile[f"Low{length}MA"] = round(
            data[f"Low{length}MA"].iloc[-1],
            3,
        )

        profile[f"DIST_TO_HIGH{length}"] = round(
            data[f"DIST_TO_HIGH{length}"].iloc[-1],
            3,
        )

        profile[f"DIST_TO_LOW{length}"] = round(
            data[f"DIST_TO_LOW{length}"].iloc[-1],
            3,
        )

        profile[f"BREAK_HIGH{length}"] = (
            data[f"BREAK_HIGH{length}"].iloc[-1]
        )

        profile[f"BREAK_LOW{length}"] = (
            data[f"BREAK_LOW{length}"].iloc[-1]
        )

        profile[f"STOP_PRICE_{length}"] = round(
            data[f"STOP_PRICE_{length}"].iloc[-1],
            3,
        )

        profile[f"RISK_{length}"] = round(
            data[f"RISK_{length}"].iloc[-1],
            3,
        )

    return profile


# ======================================
# Process
# ======================================

def process(tf):

    input_csv = (
        f"{BASE}/{SYMBOL}/live/highlow/{tf}.csv"
    )

    output_csv = (
        f"{BASE}/{SYMBOL}/profile/HIGHLOW_PROFILE_{tf}.csv"
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

    print(f"Saved -> {output_csv}")


# ======================================
# MAIN
# ======================================

if __name__ == "__main__":

    for tf in TIMEFRAMES:

        process(tf)

    print()
    print("==============================")
    print("HIGHLOW PROFILE Complete")
    print("==============================")