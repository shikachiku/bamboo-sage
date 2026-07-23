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

LENGTH = 5

# ======================================
# High Low 5
# ======================================

def calculate_highlow5(data):

    result = pd.DataFrame(index=data.index)

    result["Close"] = data["Close"]

    # ----------------------------
    # High5MA
    # ----------------------------

    result["High5MA"] = (
        data["High"]
        .rolling(LENGTH)
        .mean()
    )

    # ----------------------------
    # Low5MA
    # ----------------------------

    result["Low5MA"] = (
        data["Low"]
        .rolling(LENGTH)
        .mean()
    )

    # ----------------------------
    # Distance
    # ----------------------------

    result["DIST_TO_HIGH5"] = (
        result["High5MA"]
        - result["Close"]
    )

    result["DIST_TO_LOW5"] = (
        result["Close"]
        - result["Low5MA"]
    )

    # ----------------------------
    # Break
    # ----------------------------

    result["BREAK_HIGH5"] = (
        result["Close"]
        >
        result["High5MA"]
    )

    result["BREAK_LOW5"] = (
        result["Close"]
        <
        result["Low5MA"]
    )

    # ----------------------------
    # Stop
    # ----------------------------

    result["STOP_PRICE_5"] = (
        result["Low5MA"]
    )

    result["RISK_5"] = (
        result["Close"]
        -
        result["STOP_PRICE_5"]
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
        f"{BASE}/{SYMBOL}/live/hl5/{tf}.csv"
    )

    data = pd.read_csv(
        input_csv,
        index_col=0,
        parse_dates=True,
    )

    hl = calculate_highlow5(data)

    os.makedirs(
        os.path.dirname(output_csv),
        exist_ok=True,
    )

    hl.to_csv(output_csv)

    print(f"Saved -> {output_csv}")

# ======================================
# Main
# ======================================

if __name__ == "__main__":

    for tf in TIMEFRAMES:

        process(tf)

    print()
    print("==============================")
    print("HighLow5 Complete")
    print("==============================")