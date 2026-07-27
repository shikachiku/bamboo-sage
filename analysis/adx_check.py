from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import pandas as pd

from settings import DATA_PATH


# ======================================
# Parameter
# ======================================

SYMBOL = "WHSELFINVEST_JAPAN225CFD"


TIMEFRAMES = [
    "1M",
    "1W",
    "1D",
    "4H",
]


REMOVE_FIRST = 30



# ======================================
# ADX Check
# ======================================

def check_adx(tf):

    file = (
        DATA_PATH
        /
        SYMBOL
        /
        "indicator"
        /
        "adx"
        /
        f"{tf}.csv"
    )


    if not file.exists():

        print(
            f"Missing : {file}"
        )

        return



    # ==================================
    # Load
    # ==================================

    adx = pd.read_csv(
        file,
        index_col=0,
        parse_dates=True,
    )


    print()
    print("=" * 60)
    print(f"TIMEFRAME : {tf}")
    print("=" * 60)



    # ==================================
    # Basic
    # ==================================

    print(
        f"DATA COUNT : {len(adx)}"
    )

    print(
        f"START DATE : {adx.index[0]}"
    )

    print(
        f"END DATE   : {adx.index[-1]}"
    )


    print()



    # ==================================
    # ADX Statistics
    # ==================================

    print("ALL DATA")

    print(
        f"MAX ADX : {adx['ADX'].max():.2f}"
    )

    print(
        f"MIN ADX : {adx['ADX'].min():.2f}"
    )

    print(
        f"AVG ADX : {adx['ADX'].mean():.2f}"
    )



    print()



    # ==================================
    # First 30 bars check
    # ==================================

    first30 = adx.head(30)


    print("FIRST 30 BARS")

    print(
        f"MAX ADX : {first30['ADX'].max():.2f}"
    )

    print(
        f"AVG ADX : {first30['ADX'].mean():.2f}"
    )



    print()



    # ==================================
    # After 30 bars
    # ==================================

    normal = adx.iloc[30:]


    print("AFTER 30 BARS")

    print(
        f"COUNT : {len(normal)}"
    )

    print(
        f"MAX ADX : {normal['ADX'].max():.2f}"
    )

    print(
        f"MIN ADX : {normal['ADX'].min():.2f}"
    )

    print(
        f"AVG ADX : {normal['ADX'].mean():.2f}"
    )



    print()



    # ==================================
    # TOP 10 ADX
    # ==================================

    print("TOP 10 ADX")


    top10 = (
        normal["ADX"]
        .sort_values(
            ascending=False
        )
        .head(10)
    )


    print(top10)



    print()



    # ==================================
    # Current
    # ==================================

    current = adx.iloc[-1]


    print("CURRENT")

    print(
        f"DATE : {adx.index[-1]}"
    )

    print(
        f"ADX  : {current['ADX']:.2f}"
    )

    print(
        f"+DI  : {current['+DI']:.2f}"
    )

    print(
        f"-DI  : {current['-DI']:.2f}"
    )



# ======================================
# MAIN
# ======================================


def main():

    print()
    print("=" * 40)
    print("ADX CHECK START")
    print("=" * 40)



    for tf in TIMEFRAMES:

        check_adx(tf)



    print()
    print("=" * 40)
    print("ADX CHECK COMPLETE")
    print("=" * 40)



if __name__ == "__main__":

    main()