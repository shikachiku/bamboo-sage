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

PROFILES = [
    "ADX",
    "HIGHLOW",
    "HIGHLOW5",
]

# ======================================
# Last Candle Date
# ======================================

def get_last_bar(tf):

    raw = pd.read_csv(
        f"{BASE}/{SYMBOL}/raw/{tf}.csv",
        index_col=0,
        parse_dates=True,
    )

    return str(raw.index[-1].date())

# ======================================
# Read Profile
# ======================================

def read_profile(profile_name, tf):

    profile_file = (
        f"{BASE}/{SYMBOL}/profile/"
        f"{profile_name}_PROFILE_{tf}.csv"
    )

    df = pd.read_csv(profile_file)

    values = {}

    for _, row in df.iterrows():

        values[row["ITEM"]] = row["VALUE"]

    return values

# ======================================
# Append History
# ======================================

def append_history(profile_name, tf):

    profile = read_profile(profile_name, tf)

    last_bar = get_last_bar(tf)

    history_dir = (
        f"{BASE}/{SYMBOL}/history"
    )

    os.makedirs(history_dir, exist_ok=True)

    history_file = (
        f"{history_dir}/"
        f"{profile_name}_HISTORY_{tf}.csv"
    )

    row = {
        "DATE": last_bar,
    }

    row.update(profile)

    new_df = pd.DataFrame([row])

    # --------------------------
    # 初回
    # --------------------------

    if not os.path.exists(history_file):

        new_df.to_csv(
            history_file,
            index=False,
        )

        print(f"Create -> {history_file}")

        return

    # --------------------------
    # 既存読込
    # --------------------------

    old = pd.read_csv(
        history_file,
        dtype=str,
    )

    # --------------------------
    # 同じ日付なら更新
    # --------------------------

    if (
        len(old) > 0
        and
        old.iloc[-1]["DATE"] == last_bar
    ):

        old = old.iloc[:-1]

    # --------------------------
    # 追加
    # --------------------------

    history = pd.concat(
        [
            old,
            new_df,
        ],
        ignore_index=True,
    )

    history.to_csv(
        history_file,
        index=False,
    )

    print(f"Saved -> {history_file}")

# ======================================
# Main
# ======================================

if __name__ == "__main__":

    for profile in PROFILES:

        for tf in TIMEFRAMES:

            append_history(
                profile,
                tf,
            )

    print()
    print("==============================")
    print("History Complete")
    print("==============================")