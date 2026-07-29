import pandas as pd


# ======================================
# Parameter
# ======================================

INDICATOR = "wick"



# ======================================
# Wick Calculation
# ======================================

def calculate(data):

    result = data.copy()


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
    # ======================================

    def wick_type(row):

        upper = row["UPPER_WICK"]
        lower = row["LOWER_WICK"]


        if upper == 0 and lower == 0:

            return "NONE"


        elif upper > lower:

            return "UPPER"


        elif lower > upper:

            return "LOWER"


        else:

            return "BOTH"



    result["WICK_TYPE"] = (
        result.apply(
            wick_type,
            axis=1
        )
    )


    return result