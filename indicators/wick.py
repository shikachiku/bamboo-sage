import pandas as pd


# ======================================
# Parameter
# ======================================

INDICATOR = "wick"



# ======================================
# Wick Calculation
# ======================================

def calculate(data):

    result = data


    # ======================================
    # Upper Wick
    # ======================================

    result["UPPER_WICK"] = (
        result["High"]
        -
        result[
            [
                "Open",
                "Close",
            ]
        ]
        .max(axis=1)
    )


    # ======================================
    # Lower Wick
    # ======================================

    result["LOWER_WICK"] = (
        result[
            [
                "Open",
                "Close",
            ]
        ]
        .min(axis=1)
        -
        result["Low"]
    )


    # ======================================
    # Body
    # ======================================

    result["BODY_SIZE"] = (
        result["Close"]
        -
        result["Open"]
    ).abs()



    # ======================================
    # Total Range
    # ======================================

    total_range = (
        result["High"]
        -
        result["Low"]
    )


    total_range = total_range.replace(
        0,
        float("nan")
    )



    # ======================================
    # Wick Ratio
    # ======================================

    result["UPPER_WICK_RATIO"] = (
        result["UPPER_WICK"]
        /
        total_range
    )


    result["LOWER_WICK_RATIO"] = (
        result["LOWER_WICK"]
        /
        total_range
    )


    result["WICK_RATIO"] = (
        result["UPPER_WICK"]
        +
        result["LOWER_WICK"]
    ) / total_range



    result[
        [
            "UPPER_WICK_RATIO",
            "LOWER_WICK_RATIO",
            "WICK_RATIO",
        ]
    ] = result[
        [
            "UPPER_WICK_RATIO",
            "LOWER_WICK_RATIO",
            "WICK_RATIO",
        ]
    ].fillna(0)



    # ======================================
    # Wick Type
    # Vectorized
    # ======================================

    result["WICK_TYPE"] = "NONE"


    result.loc[
        result["UPPER_WICK"]
        >
        result["LOWER_WICK"],
        "WICK_TYPE"
    ] = "UPPER"



    result.loc[
        result["LOWER_WICK"]
        >
        result["UPPER_WICK"],
        "WICK_TYPE"
    ] = "LOWER"



    result.loc[
        result["UPPER_WICK"]
        ==
        result["LOWER_WICK"],
        "WICK_TYPE"
    ] = "BOTH"



    return result