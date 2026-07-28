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


# ======================================
# Profile
# ======================================

def create_profile(data):

    profile = {}

    swing_high = data[
        data["SWING_HIGH"]
    ]

    swing_low = data[
        data["SWING_LOW"]
    ]


    # -----------------------------
    # Last Swing High
    # -----------------------------

    if len(swing_high):

        last = swing_high.iloc[-1]

        profile["LAST_SWING_HIGH"] = round(
            last["High"],
            3,
        )

        profile["LAST_SWING_HIGH_DATE"] = str(
            last.name.date()
        )

    else:

        profile["LAST_SWING_HIGH"] = ""

        profile["LAST_SWING_HIGH_DATE"] = ""


    # -----------------------------
    # Last Swing Low
    # -----------------------------

    if len(swing_low):

        last = swing_low.iloc[-1]

        profile["LAST_SWING_LOW"] = round(
            last["Low"],
            3,
        )

        profile["LAST_SWING_LOW_DATE"] = str(
            last.name.date()
        )

    else:

        profile["LAST_SWING_LOW"] = ""

        profile["LAST_SWING_LOW_DATE"] = ""


    # -----------------------------
    # Count
    # -----------------------------

    profile["SWING_HIGH_COUNT"] = len(
        swing_high
    )

    profile["SWING_LOW_COUNT"] = len(
        swing_low
    )


    # -----------------------------
    # Current Close
    # -----------------------------

    profile["CURRENT_CLOSE"] = round(
        data["Close"].iloc[-1],
        3,
    )


    return profile

# ======================================
# Process
# ======================================

def process(
    symbol,
    tf,
):

    input_csv = (
        DATA_PATH
        / symbol["Folder"]
        / "indicator"
        / "swing"
        / f"{tf}.csv"
    )

    if not input_csv.exists():

        print(
            f"SWING Not Found : {input_csv}"
        )

        return


    output_csv = (
        DATA_PATH
        / symbol["Folder"]
        / "profile"
        / f"SWING_PROFILE_{tf}.csv"
    )


    data = pd.read_csv(
        input_csv,
        index_col=0,
        parse_dates=True,
    )


    profile = create_profile(
        data
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
    print("SWING PROFILE Complete")
    print("==============================")