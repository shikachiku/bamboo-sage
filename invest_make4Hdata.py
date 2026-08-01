import pandas as pd
from pathlib import Path

from settings import DATA_PATH


# ===================================
# Config
# ===================================

INVEST_SYMBOL_FILE = "invest_symbols.csv"

SAVE_DIR = DATA_PATH


# ===================================
# 4H conversion
# ===================================

def make_4h_data(
    input_file,
    output_file,
):


    df = pd.read_csv(
        input_file
    )


    print(
        "READ:",
        input_file
    )


    # -----------------------------
    # Date
    # -----------------------------

    df["Date"] = pd.to_datetime(
        df["Date"]
    )


    df = df.sort_values(
        "Date"
    )


    df = df.set_index(
        "Date"
    )


    # -----------------------------
    # 4H aggregation
    # -----------------------------

    df_4h = df.resample(
        "4h",
        origin="start"
    ).agg(

        {
            "Open": "first",

            "High": "max",

            "Low": "min",

            "Close": "last",

            "Volume": "sum",

        }

    )


    # 欠損足削除

    df_4h = df_4h.dropna()


    # -----------------------------
    # Date restore
    # -----------------------------

    df_4h = df_4h.reset_index()


    df_4h["Date"] = (
        df_4h["Date"]
        .dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )


    # -----------------------------
    # Save
    # -----------------------------

    df_4h.to_csv(
        output_file,
        index=False,
        encoding="utf-8"
    )


    print(
        "SAVE:",
        output_file
    )



# ===================================
# symbol process
# ===================================

def process_symbol(
    folder
):


    input_file = (
        SAVE_DIR /
        folder /
        "investraw" /
        "1H.csv"
    )


    output_file = (
        SAVE_DIR /
        folder /
        "investraw" /
        "4H.csv"
    )


    if not input_file.exists():

        print(
            "NOT FOUND:",
            input_file
        )

        return



    make_4h_data(

        input_file,

        output_file

    )



# ===================================
# main
# ===================================

def main():


    symbols = pd.read_csv(
        INVEST_SYMBOL_FILE
    )


    for _, row in symbols.iterrows():


        if row["Enable"] != 1:

            continue


        print()

        print(
            "PROCESS:",
            row["Folder"]
        )


        process_symbol(
            row["Folder"]
        )



if __name__ == "__main__":

    main()
