import os
import pandas as pd


def append_history(
    symbol,
    timeframe,
    profile,
    bar_date,
):

    history_dir = f"data/{symbol}/history"

    os.makedirs(
        history_dir,
        exist_ok=True,
    )

    history_file = (
        f"{history_dir}/ADX_HISTORY_{timeframe}.csv"
    )

    row = {
        "DATE": bar_date,

        "CURRENT": profile["CURRENT"],

        "POSITION": profile["POSITION"],

        "ZONE": profile["ZONE"],

        "TREND": profile["TREND_STRENGTH"],

        "STATE": profile["STATE"],
    }

    df = pd.DataFrame([row])

    if os.path.exists(history_file):

        df.to_csv(
            history_file,
            mode="a",
            header=False,
            index=False,
        )

    else:

        df.to_csv(
            history_file,
            index=False,
        )

    print(
        f"History -> {history_file}"
    )