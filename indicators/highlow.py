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

LENGTHS = [
    5,
    10,
    20,
    60,
]

# ======================================
# High Low Engine
# ======================================

def calculate_highlow(data):

    result = pd.DataFrame(index=data.index)

    result["Close"] = data["Close"]

    for length in LENGTHS:

        # --------------------------
        # High MA
        # --------------------------

        high_name = f"High{length}MA"

        result[high_name] = (
            data["High"]
            .rolling(length)
            .mean()
        )

        # --------------------------
        # Low MA
        # --------------------------

        low_name = f"Low{length}MA"

        result[low_name] = (
            data["Low"]
            .rolling(length)
            .mean()
        )

        # --------------------------
        # Distance
        # --------------------------

        result[f"DIST_TO_HIGH{length}"] = (
            result[high_name]
            - result["Close"]
        )

        result[f"DIST_TO_LOW{length}"] = (
            result["Close"]
            - result[low_name]
        )

        # --------------------------
        # Break
        # --------------------------

        result[f"BREAK_HIGH{length}"] = (
            result["Close"]
            >
            result[high_name]
        )

        result[f"BREAK_LOW{length}"] = (
            result["Close"]
            <
            result[low_name]
        )

        # --------------------------
        # Stop
        # --------------------------

        result[f"STOP_PRICE_{length}"] = (
            result[low_name]
        )

        result[f"RISK_{length}"] = (
            result["Close"]
            -
            result[f"STOP_PRICE_{length}"]
        )

    return result

# ======================================
# Process
# ======================================

def process(tf):

    input_csv = (
        f"{BASE}/{SYMBOL}/raw/{tf}.csv"
    )

    output_csv = (
        f"{BASE}/{SYMBOL}/live/highlow/{tf}.csv"
    )

    data = pd.read_csv(
        input_csv,
        index_col=0,
        parse_dates=True,
    )

    hl = calculate_highlow(data)

    os.makedirs(
        os.path.dirname(output_csv),
        exist_ok=True,
    )

    hl.to_csv(output_csv)

    print(
        f"Saved -> {output_csv}"
    )

# ======================================
# Main
# ======================================

if __name__ == "__main__":

    for tf in TIMEFRAMES:

        process(tf)

    print()
    print("==============================")
    print("HIGH LOW Complete")
    print("==============================")