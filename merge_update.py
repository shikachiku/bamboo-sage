from datetime import datetime

import pandas as pd


UPDATE_BARS = 300


def load_existing(path):

    if path.exists():

        return pd.read_csv(
            path,
            index_col=0,
            parse_dates=True,
        )

    return None


def save(df, path):

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(path)

    print(f"Saved : {path}")


def get_last_datetime(df):

    if df is None:

        return None

    if len(df) == 0:

        return None

    return df.index.max()


def calculate_missing_bars(
    timeframe,
    last_datetime,
):

    if last_datetime is None:

        return UPDATE_BARS

    now = datetime.now()

    seconds_map = {
        "60": 60 * 60,
        "1D": 60 * 60 * 24,
        "1W": 60 * 60 * 24 * 7,
        "1M": 60 * 60 * 24 * 30,
    }

    seconds = seconds_map.get(timeframe)

    if seconds is None:

        return UPDATE_BARS

    diff = (
        now - last_datetime.to_pydatetime()
    ).total_seconds()

    bars = max(
        0,
        int(diff / seconds),
    )

    return bars + 20


def merge_data(
    old_df,
    new_df,
):

    if old_df is None:

        return new_df

    merged = pd.concat(
        [
            old_df,
            new_df,
        ]
    )

    merged = merged[
        ~merged.index.duplicated(
            keep="last"
        )
    ]

    merged = merged.sort_index()

    return merged


from datetime import datetime

def history_too_old(timeframe, last_datetime):
    """
    履歴が古すぎる場合 True を返す
    """

    if last_datetime is None:
        return True

    now = datetime.now()

    diff_days = (now - last_datetime.to_pydatetime()).days

    limits = {
        "60": 7,
        "1D": 30,
        "1W": 90,
        "1M": 365,
    }

    return diff_days > limits[timeframe]



def history_too_old(timeframe, last_datetime):
    """
    履歴が古すぎる場合 True を返す
    """

    if last_datetime is None:
        return True

    now = datetime.now()

    diff_days = (now - last_datetime.to_pydatetime()).days

    limits = {
        "60": 7,     # 1週間以上空いたらフル取得
        "1D": 30,    # 1か月
        "1W": 90,    # 3か月
        "1M": 365,   # 1年
    }

    return diff_days > limits[timeframe]

def has_new_data(old_df, new_df):

    if old_df is None:
        return True

    if len(new_df) == 0:
        return False

    last_old = old_df.index.max()

    last_new = new_df.index.max()

    return last_new > last_old