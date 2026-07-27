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

BASE = DATA_PATH

SYMBOL = "WHSELFINVEST_JAPAN225CFD"

TIMEFRAMES = [
    "1M",
    "1W",
    "1D",
    "4H",
]


# ==========================================
# ZONE
# ==========================================

ZONE_LOW = 0.20
ZONE_LOW_NORMAL = 0.40
ZONE_NORMAL = 0.60
ZONE_HIGH_NORMAL = 0.80


# ==========================================
# PROFILE
# ==========================================

def create_profile(adx):

    current = adx["ADX"].iloc[-1]

    minimum = adx["ADX"].min()

    maximum = adx["ADX"].max()

    average = adx["ADX"].mean()

    median = adx["ADX"].median()

    std = adx["ADX"].std()


    # ----------------------------
    # Position
    # ----------------------------

    if maximum != minimum:

        position = (
            current - minimum
        ) / (
            maximum - minimum
        )

    else:

        position = 0


    # ----------------------------
    # Zone
    # ----------------------------

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


    # ----------------------------
    # Trend Strength
    # ----------------------------

    if current < 20:

        trend_strength = "NONE"

    elif current < 30:

        trend_strength = "WEAK"

    elif current < 40:

        trend_strength = "NORMAL"

    elif current < 50:

        trend_strength = "STRONG"

    elif current < 60:

        trend_strength = "VERY_STRONG"

    else:

        trend_strength = "EXTREME"


    # ----------------------------
    # State
    # ----------------------------

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


    # ----------------------------
    # Profile
    # ----------------------------

    profile = {

        "CURRENT": round(current, 3),

        "MIN": round(minimum, 3),

        "MAX": round(maximum, 3),

        "AVERAGE": round(average, 3),

        "MEDIAN": round(median, 3),

        "STD": round(std, 3),

        "RANGE": round(maximum - minimum, 3),

        "POSITION": round(position, 3),

        "ZONE": zone,

        "TREND_STRENGTH": trend_strength,

        "STATE": state,

        "TO_MIN": round(current - minimum, 3),

        "TO_MAX": round(maximum - current, 3),

        "DISTANCE_TO_LOW": round(position * 100, 1),

        "DISTANCE_TO_HIGH": round((1 - position) * 100, 1),

    }


    return profile



# ==========================================
# PROCESS
# ==========================================

def process(tf):


    input_csv = (
        BASE
        / SYMBOL
        / "indicator"
        / "adx"
        / f"{tf}.csv"
    )


    output_csv = (
        BASE
        / SYMBOL
        / "profile"
        / f"ADX_PROFILE_{tf}.csv"
    )


    adx = pd.read_csv(
        input_csv,
        index_col=0,
        parse_dates=True,
    )


    profile = create_profile(adx)


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