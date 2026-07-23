from history_writer import append_history

# ======================================================
# Profile Parameter
# ======================================================

ZONE_LOW = 0.20
ZONE_LOW_NORMAL = 0.40
ZONE_NORMAL = 0.60
ZONE_HIGH_NORMAL = 0.80

import os
import pandas as pd

# ==========================
# Parameter
# ==========================

BASE = "data"

SYMBOL = "WHSELFINVEST_JAPAN225CFD"

TIMEFRAMES = [
    "1M",
    "1W",
    "1D",
    "4H",
]

# ==========================
# PROFILE
# ==========================

def create_profile(adx):

    current = adx["ADX"].iloc[-1]

    minimum = adx["ADX"].min()

    maximum = adx["ADX"].max()

    average = adx["ADX"].mean()

    median = adx["ADX"].median()

    std = adx["ADX"].std()

    profile = {}

    profile["CURRENT"] = current
    profile["MIN"] = minimum
    profile["MAX"] = maximum
    profile["AVERAGE"] = average
    profile["MEDIAN"] = median
    profile["STD"] = std

    profile["RANGE"] = maximum - minimum

    profile["TO_MIN"] = current - minimum
    profile["TO_MAX"] = maximum - current

    profile["ABOVE_AVG"] = current - average

    # -------------------------
    # POSITION
    # -------------------------

    if maximum != minimum:
        position = (
            current - minimum
        ) / (
            maximum - minimum
        )
    else:
        position = 0

    profile["POSITION"] = round(position, 3)

    # -------------------------
    # ZONE
    # -------------------------

    if position < ZONE_LOW:

        zone = "LOW"

    elif position < ZONE_LOW_NORMAL:

        zone = "LOW_NORMAL"

    elif position < ZONE_NORMAL:

        zone = "NORMAL"

    elif position < ZONE_HIGH_NORMAL:

        zone = "HIGH_NORMAL"

    else:

        zone = "HIGH"

    profile["ZONE"] = zone

    # -------------------------
    # TREND
    # -------------------------

    if current < 20:

        strength = "NONE"

    elif current < 30:

        strength = "WEAK"

    elif current < 40:

        strength = "NORMAL"

    elif current < 50:

        strength = "STRONG"

    elif current < 60:

        strength = "VERY_STRONG"

    else:

        strength = "EXTREME"

    profile["TREND_STRENGTH"] = strength

    # -------------------------
    # STATE
    # -------------------------

    if zone == "LOW":

        state = "READY"

    elif zone == "LOW_NORMAL":

        state = "ACCUMULATION"

    elif zone == "NORMAL":

        state = "RUNNING"

    elif zone == "HIGH_NORMAL":

        state = "CAUTION"

    else:

        state = "OVERHEATED"

    profile["STATE"] = state

    return profile


# ==========================
# SAVE
# ==========================

def process(tf):

    input_csv = (
        f"{BASE}/{SYMBOL}/live/ADX_{tf}.csv"
    )

    output_csv = (
        f"{BASE}/{SYMBOL}/profile/ADX_PROFILE_{tf}.csv"
    )

    adx = pd.read_csv(
        input_csv,
        index_col=0,
        parse_dates=True,
    )
    last_bar = adx.index[-1].strftime("%Y-%m-%d")

    profile = create_profile(adx)
    
    append_history(
        SYMBOL,
        tf,
        profile,
        last_bar,
    )

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


# ==========================
# MAIN
# ==========================

if __name__ == "__main__":

    for tf in TIMEFRAMES:

        process(tf)

    print()
    print("==============================")
    print("ADX PROFILE Complete")
    print("==============================")