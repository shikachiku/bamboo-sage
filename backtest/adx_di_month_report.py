from pathlib import Path
from datetime import datetime
import pandas as pd
import sys


# ======================================
# Project Path
# ======================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )


from settings import DATA_PATH


# ======================================
# Parameter
# ======================================

SYMBOL = "WHSELFINVEST_JAPAN225CFD"

STRATEGY_NAME = "adx_di_month"

BACKTEST_DIR = (
    DATA_PATH
    /
    SYMBOL
    /
    "backtest"
)



# ======================================
# Load
# ======================================

def load_result():

    files = sorted(
        BACKTEST_DIR.glob(
            f"{STRATEGY_NAME}_result_*.csv"
        )
    )


    if not files:

        raise FileNotFoundError(
            "Backtest result file not found"
        )


    latest_file = files[-1]


    print()
    print("LOAD RESULT")
    print(latest_file)


    return pd.read_csv(
        latest_file,
        parse_dates=[
            "ENTRY_DATE",
            "EXIT_DATE",
        ]
    )



# ======================================
# Basic Statistics
# ======================================

def basic_report(df):

    total = len(df)

    win = df[
        df["PROFIT"] > 0
    ]

    loss = df[
        df["PROFIT"] <= 0
    ]


    gross_profit = (
        win["PROFIT"]
        .sum()
    )


    gross_loss = (
        abs(
            loss["PROFIT"]
            .sum()
        )
    )


    pf = (
        gross_profit
        /
        gross_loss
        if gross_loss != 0
        else 0
    )


    print()
    print("="*50)
    print("BASIC REPORT")
    print("="*50)


    print(
        f"TOTAL TRADE : {total}"
    )

    print(
        f"WIN         : {len(win)}"
    )

    print(
        f"LOSS        : {len(loss)}"
    )

    print(
        f"WIN RATE    : {len(win)/total*100:.2f}%"
    )


    print(
        f"TOTAL PROFIT: {df['PROFIT'].sum():.1f}"
    )


    print(
        f"AVG PROFIT  : {df['PROFIT'].mean():.1f}"
    )


    print(
        f"MAX PROFIT  : {df['PROFIT'].max():.1f}"
    )


    print(
        f"MAX LOSS    : {df['PROFIT'].min():.1f}"
    )


    print(
        f"PF          : {pf:.2f}"
    )



# ======================================
# Exit Reason
# ======================================

def exit_report(df):

    print()
    print("="*50)
    print("EXIT REASON")
    print("="*50)


    report = (
        df
        .groupby(
            "EXIT_REASON"
        )
        .agg(
            COUNT=(
                "PROFIT",
                "count"
            ),

            AVG_PROFIT=(
                "PROFIT",
                "mean"
            ),

            TOTAL_PROFIT=(
                "PROFIT",
                "sum"
            )
        )
    )


    print(report)



# ======================================
# Year Report
# ======================================

def yearly_report(df):

    df["YEAR"] = (
        df["ENTRY_DATE"]
        .dt.year
    )


    report = (
        df
        .groupby(
            "YEAR"
        )
        .agg(

            TRADE=(
                "PROFIT",
                "count"
            ),

            PROFIT=(
                "PROFIT",
                "sum"
            ),

            WIN_RATE=(
                "PROFIT",
                lambda x:
                (
                    x > 0
                )
                .mean()
                *
                100
            )
        )
    )


    print()
    print("="*50)
    print("YEAR REPORT")
    print("="*50)

    print(report)



# ======================================
# ADX LEVEL Analysis
# ======================================

def adx_level_report(df):

    print()
    print("="*50)
    print("ADX LEVEL")
    print("="*50)


    df["ADX_LEVEL_ZONE"] = pd.cut(
        df["ENTRY_ADX_LEVEL"],
        bins=[
            -0.01,
            0.2,
            0.5,
            0.8,
            1.0
        ],
        labels=[
            "LOW",
            "MID_LOW",
            "MID",
            "HIGH"
        ]
    )


    report = (
        df
        .groupby(
            "ADX_LEVEL_ZONE",
            observed=False
        )
        .agg(

            COUNT=(
                "PROFIT",
                "count"
            ),

            AVG_PROFIT=(
                "PROFIT",
                "mean"
            ),

            WIN_RATE=(
                "PROFIT",
                lambda x:
                (
                    x > 0
                )
                .mean()
                *
                100
            )
        )
    )


    print(report)



# ======================================
# Main
# ======================================

def main():

    df = load_result()


    basic_report(df)

    exit_report(df)

    yearly_report(df)

    adx_level_report(df)


    run_id = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


    report_file = (
        BACKTEST_DIR
        /
        f"{STRATEGY_NAME}_report_{run_id}.csv"
    )


    df.to_csv(
        report_file,
        index=False
    )


    print()
    print("="*50)
    print("REPORT SAVED")
    print(report_file)
    print("="*50)



if __name__ == "__main__":

    main()