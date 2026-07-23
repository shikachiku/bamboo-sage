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
# Read Profile
# ======================================

def load_profile(name, tf):

    file = (
        f"{BASE}/{SYMBOL}/profile/"
        f"{name}_PROFILE_{tf}.csv"
    )

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

    return table.get(stars, 0)

# ======================================
# Build Master
# ======================================

def build_master(tf):

    adx = load_profile("ADX", tf)

    highlow = load_profile("HIGHLOW", tf)

    highlow5 = load_profile("HIGHLOW5", tf)

    master = {}

    # ---------------------------------

    master["TIMEFRAME"] = tf

    master["ADX_ZONE"] = adx.get("ZONE")

    master["ADX_STATE"] = adx.get("STATE")

    master["ADX_TREND"] = adx.get("TREND_STRENGTH")

    # ---------------------------------

    master["HIGHLOW_SCORE"] = highlow.get(
        "BREAK_SCORE"
    )

    master["HIGHLOW_ZONE"] = highlow.get(
        "BUY_ZONE"
    )

    master["HIGHLOW_STATE"] = highlow.get(
        "STATE"
    )

    # ---------------------------------

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
    # AI SCORE
    # =====================================

    score = 0

    score += stars_to_score(
        highlow.get("BUY_ZONE")
    )

    score += stars_to_score(
        highlow5.get("BUY_ZONE")
    )

    score += stars_to_score(
        "★★★★★"
        if adx.get("STATE") == "READY"
        else
        "★★★☆☆"
    )

    master["AI_SCORE"] = score

    # =====================================
    # AI ZONE
    # =====================================

    if score >= 14:

        ai = "★★★★★"

    elif score >= 11:

        ai = "★★★★☆"

    elif score >= 8:

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

def process(tf):

    master = build_master(tf)

    out = (
        f"{BASE}/{SYMBOL}/master"
    )

    os.makedirs(out, exist_ok=True)

    output = (
        f"{out}/{tf}.csv"
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
        f"Saved -> {output}"
    )

# ======================================
# MAIN
# ======================================

if __name__ == "__main__":

    for tf in TIMEFRAMES:

        process(tf)

    print()
    print("==============================")
    print("MASTER Complete")
    print("==============================")