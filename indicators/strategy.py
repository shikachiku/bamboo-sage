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

def process(tf):

    master_file = (
        f"{BASE}/{SYMBOL}/master/{tf}.csv"
    )

    df = pd.read_csv(master_file)

    master = {}

    for _, row in df.iterrows():

        master[row["ITEM"]] = row["VALUE"]

    result = decide(master)

    out = (
        f"{BASE}/{SYMBOL}/strategy"
    )

    os.makedirs(out, exist_ok=True)

    output = (
        f"{out}/{tf}.csv"
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

    print(f"Saved -> {output}")

# ======================================
# Main
# ======================================

if __name__ == "__main__":

    for tf in TIMEFRAMES:

        process(tf)

    print()
    print("==============================")
    print("STRATEGY Complete")
    print("==============================")