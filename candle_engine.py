from pathlib import Path

import pandas as pd

from folder_manager import (
    RAW_DIR,
    LIVE_DIR,
)

from color import title


RAW_60 = RAW_DIR / "60.csv"

RAW_1D = RAW_DIR / "1D.csv"
RAW_1W = RAW_DIR / "1W.csv"
RAW_1M = RAW_DIR / "1M.csv"

LIVE_240 = LIVE_DIR / "240.csv"

LIVE_1D = LIVE_DIR / "1D.csv"
LIVE_1W = LIVE_DIR / "1W.csv"
LIVE_1M = LIVE_DIR / "1M.csv"


def load_csv(path):

    return pd.read_csv(
        path,
        index_col=0,
        parse_dates=True,
    )


def save(df, path):

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(path)

    print(f"Saved : {path}")


def build_240():

    title("Build 240min")

    df = load_csv(RAW_60)

    agg = {
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
    }

    if "Volume" in df.columns:

        agg["Volume"] = "sum"

    df240 = (
        df
        .resample("240min")
        .agg(agg)
        .dropna()
    )

    save(
        df240,
        LIVE_240,
    )
def build_live_daily():

    title("Build Live Daily")

    df = load_csv(RAW_1D)

    save(
        df,
        LIVE_1D,
    )


def build_live_weekly():

    title("Build Live Weekly")

    df = load_csv(RAW_1W)

    save(
        df,
        LIVE_1W,
    )


def build_live_monthly():

    title("Build Live Monthly")

    df = load_csv(RAW_1M)

    save(
        df,
        LIVE_1M,
    )
if __name__ == "__main__":

    print()

    print("=" * 60)
    print("CANDLE ENGINE START")
    print("=" * 60)

    build_240()

    build_live_daily()

    build_live_weekly()

    build_live_monthly()

    print()

    title(
        "CANDLE ENGINE COMPLETED"
    )