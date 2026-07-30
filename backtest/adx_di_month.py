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
from symbol_loader import load_symbols



# ======================================
# Parameter
# ======================================

STRATEGY_NAME = "adx_di_month"



# ======================================
# Load
# ======================================

def load_analysis(
    symbol,
    timeframe
):

    file = (
        DATA_PATH
        / symbol["Folder"]
        / "analysis"
        / f"{timeframe}.csv"
    )


    return pd.read_csv(
        file,
        parse_dates=[
            "Date"
        ]
    )


# ======================================
# Monthly Entry Signal
# ======================================

def make_entry_signal(df):

    df["DI_GC"] = False


    for i in range(1, len(df)):

        if (

            df["+DI"].iloc[i-1]
            <=
            df["-DI"].iloc[i-1]

            and

            df["+DI"].iloc[i]
            >
            df["-DI"].iloc[i]

        ):

            df.loc[
                i,
                "DI_GC"
            ] = True


    return df



# ======================================
# Weekly Exit Signal
# ======================================

def check_weekly_exit(
    weekly,
    date
):

    target = weekly[
        weekly["Date"] > date
    ]


    red_count = 0


    for _, row in target.iterrows():

        if row["HA_COLOR"] == "RED":

            red_count += 1

        else:

            red_count = 0


        if red_count >= 2:

            return row["Date"]


    return None



# ======================================
# Monthly Stop
# ======================================

def check_month_stop(
    monthly,
    index
):

    for i in range(
        index + 1,
        len(monthly)
    ):

        row = monthly.iloc[i]


        if (

            row["HA_Close"]
            <
            row["Low5MA"]

        ):

            return row["Date"]


    return None

# ======================================
# Trade Risk Calculation
# Maximum Profit / Drawdown
# ======================================

def calculate_trade_risk(
    monthly,
    weekly,
    entry_date,
    exit_date,
    entry_price
):


    prices = []


    # ------------------------------
    # Monthly High / Low
    # ------------------------------

    target_month = monthly[
        (monthly["Date"] >= entry_date)
        &
        (monthly["Date"] <= exit_date)
    ]


    for _, row in target_month.iterrows():

        prices.append(
            {
                "High": row["High"],
                "Low": row["Low"]
            }
        )


    # ------------------------------
    # Weekly High / Low
    # ------------------------------

    target_week = weekly[
        (weekly["Date"] >= entry_date)
        &
        (weekly["Date"] <= exit_date)
    ]


    for _, row in target_week.iterrows():

        prices.append(
            {
                "High": row["High"],
                "Low": row["Low"]
            }
        )


    if len(prices) == 0:

        return 0, 0



    highs = [
        x["High"]
        for x in prices
    ]


    lows = [
        x["Low"]
        for x in prices
    ]



    max_price = max(highs)

    min_price = min(lows)



    max_profit = (
        max_price
        -
        entry_price
    )



    max_drawdown = (
        min_price
        -
        entry_price
    )



    return (
        max_profit,
        max_drawdown
    )

# ======================================
# Backtest
# ======================================


# ======================================
# Backtest
# ======================================

def backtest(symbol):


    monthly = load_analysis(
        symbol,
        "1M"
    )

    weekly = load_analysis(
        symbol,
        "1W"
    )


    monthly = make_entry_signal(
        monthly
    )


    results = []


    for i in range(
        len(monthly)-1
    ):


        row = monthly.iloc[i]


        if row["DI_GC"]:


            entry_row = monthly.iloc[i+1]


            entry_date = entry_row["Date"]

            entry_price = entry_row["Open"]



            exit_week = check_weekly_exit(
                weekly,
                entry_date
            )


            exit_stop = check_month_stop(
                monthly,
                i+1
            )



            exits = []



            if exit_stop is not None:

                exits.append(
                    (
                        exit_stop,
                        "STOP_LOSS"
                    )
                )



            if exit_week is not None:

                exits.append(
                    (
                        exit_week,
                        "WEEKLY_RED"
                    )
                )



            if exits:

                exit_date, reason = sorted(
                    exits,
                    key=lambda x: x[0]
                )[0]


            else:

                exit_date = monthly.iloc[-1]["Date"]

                reason = "HOLD"



            if reason == "WEEKLY_RED":

                exit_price = weekly[
                    weekly["Date"] == exit_date
                ]["Open"].iloc[0]


            else:

                exit_price = monthly[
                    monthly["Date"] == exit_date
                ]["Open"].iloc[0]



            profit = (
                exit_price
                -
                entry_price
            )


            profit_rate = (
                profit
                /
                entry_price
                *
                100
            )



            hold_months = (
                exit_date.year
                -
                entry_date.year
            ) * 12 + (
                exit_date.month
                -
                entry_date.month
            )



            max_profit, max_drawdown = calculate_trade_risk(
                monthly,
                weekly,
                entry_date,
                exit_date,
                entry_price
            )



            results.append({

                "ENTRY_DATE": entry_date,

                "ENTRY_PRICE": entry_price,

                "EXIT_DATE": exit_date,

                "EXIT_PRICE": exit_price,

                "EXIT_REASON": reason,

                "PROFIT": profit,

                "PROFIT_RATE": profit_rate,

                "HOLD_MONTHS": hold_months,

                "MAX_PROFIT": max_profit,

                "MAX_DRAWDOWN": max_drawdown,

                "ENTRY_ADX": row["ADX"],

                "ENTRY_ADX_LEVEL":
                    row["ADX_LEVEL"]
                    if "ADX_LEVEL" in row
                    else None,

                "ENTRY_PLUS_DI": row["+DI"],

                "ENTRY_MINUS_DI": row["-DI"],

            })


    return pd.DataFrame(results)# ======================================
# Save
# ======================================

def save_result(
    symbol,
    result
):

    folder = (
        DATA_PATH
        /
        symbol["Folder"]
        /
        "backtest"
    )


    folder.mkdir(
        parents=True,
        exist_ok=True
    )


    run_id = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


    file = (
        folder
        /
        f"{STRATEGY_NAME}_result_{run_id}.csv"
    )


    result.to_csv(
        file,
        index=False
    )


    print()
    print("="*50)
    print("BACKTEST COMPLETE")
    print(symbol["Name"])
    print(file)
    print("="*50)



# ======================================
# Main
# ======================================

# ======================================
# Save
# ======================================

def save_result(
    symbol,
    result
):

    folder = (
        DATA_PATH
        /
        symbol["Folder"]
        /
        "backtest"
    )


    folder.mkdir(
        parents=True,
        exist_ok=True
    )


    run_id = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


    file = (
        folder
        /
        f"{STRATEGY_NAME}_result_{run_id}.csv"
    )


    result.to_csv(
        file,
        index=False
    )


    print()
    print("="*50)
    print("BACKTEST COMPLETE")
    print(symbol["Name"])
    print(file)
    print("="*50)



# ======================================
# Main
# ======================================

def main():


    symbols = load_symbols()


    for symbol in symbols:


        print()
        print("="*50)
        print(
            f"BACKTEST : {symbol['Name']}"
        )
        print("="*50)



        result = backtest(
            symbol
        )


        save_result(
            symbol,
            result
        )



if __name__ == "__main__":

    main()