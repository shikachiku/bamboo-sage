from pathlib import Path
import sys

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
    "1M",
    "1W",
    "1D",
    "4H",
]

# ======================================
# Strategy
# ======================================

def decide(master):

    score = int(master["AI_SCORE"])

    adx = str(master["ADX_STATE"])

    hl = str(master["HIGHLOW_ZONE"])

    hl5 = str(master["HIGHLOW5_ZONE"])

    signal = "WAIT"

    confidence = 0

    # ==================================
    # BUY STRONG
    # ==================================

    if (
        adx == "READY"
        and
        hl == "★★★★★"
        and
        hl5 == "★★★★★"
    ):

        signal = "BUY_STRONG"

        confidence = 100

    # ==================================

    elif (
        adx == "READY"
        and
        score >= 11
    ):

        signal = "BUY"

        confidence = 80

    # ==================================

    elif score >= 9:

        signal = "WATCH"

        confidence = 60

    # ==================================

    elif score >= 6:

        signal = "HOLD"

        confidence = 50

    # ==================================

    elif adx == "EXTREME":

        signal = "REDUCE"

        confidence = 40

    # ==================================

    else:

        signal = "SELL"

        confidence = 20

    return {

        "SIGNAL": signal,

        "CONFIDENCE": confidence,

    }

# ======================================
# Process
# ======================================

def process(
    symbol,
    tf,
):

    master_file = (
        BASE
        / symbol["Folder"]
        / "master"
        / f"{tf}.csv"
    )

    if not master_file.exists():

        print(
            f"MASTER Not Found : {master_file}"
        )

        return

    df = pd.read_csv(master_file)

    master = {}

    for _, row in df.iterrows():

        master[row["ITEM"]] = row["VALUE"]

    result = decide(master)

    out = (
        BASE
        / symbol["Folder"]
        / "strategy"
    )

    out.mkdir(
        parents=True,
        exist_ok=True,
    )

    output = (
        out
        / f"{tf}.csv"
    )

    strategy = {

        **master,

        **result,

    }

    save = pd.DataFrame(

        strategy.items(),

        columns=[
            "ITEM",
            "VALUE",
        ],

    )

    save.to_csv(

        output,

        index=False,

    )

    print(
        f"Saved -> {output}"
    )

# ======================================
# Main
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
    print("STRATEGY Complete")
    print("==============================")