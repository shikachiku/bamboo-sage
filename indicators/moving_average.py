import pandas as pd


# ======================================
# Parameter
# ======================================

INDICATOR = "moving_average"


# 移動平均期間
MA_LIST = [
    20,
    50,
    200,
]


# ======================================
# Moving Average
# ======================================

def calculate(data):

    result = data.copy()


    # ----------------------------
    # SMA
    # ----------------------------

    for length in MA_LIST:

        result[f"SMA_{length}"] = (
            data["Close"]
            .rolling(length)
            .mean()
        )


    # ----------------------------
    # SMA200 Position
    # ----------------------------

    result["ABOVE_SMA200"] = (
        result["Close"]
        >
        result["SMA_200"]
    )


    # ----------------------------
    # Distance
    # ----------------------------

    result["DIST_TO_SMA200"] = (
        result["Close"]
        -
        result["SMA_200"]
    )


    # ----------------------------
    # Trend
    # ----------------------------

    result["SMA200_TREND"] = ""


    for i in range(1, len(result)):


        current = result["SMA_200"].iloc[i]

        previous = result["SMA_200"].iloc[i-1]


        if pd.isna(current) or pd.isna(previous):

            continue


        if current > previous:

            result.iloc[
                i,
                result.columns.get_loc(
                    "SMA200_TREND"
                )
            ] = "UP"


        elif current < previous:

            result.iloc[
                i,
                result.columns.get_loc(
                    "SMA200_TREND"
                )
            ] = "DOWN"



    return result



# ======================================
# MAIN
# ======================================

if __name__ == "__main__":

    from indicator_base import run_indicator

    run_indicator(
        INDICATOR,
        calculate,
    )