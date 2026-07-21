import os
import pandas as pd
from config import CSV_FILE


def load_data():

    """
    TradingViewで保存したCSVを読み込む
    """

    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(
            f"{CSV_FILE} が見つかりません。\n"
            "先に tv_download.py を実行してください。"
        )

    df = pd.read_csv(CSV_FILE)

    # 日付をdatetime型へ
    df["Date"] = pd.to_datetime(df["Date"])

    # 日付をインデックスにする
    df.set_index("Date", inplace=True)

    # 数値型へ変換
    numeric = ["Open", "High", "Low", "Close"]

    for col in numeric:
        df[col] = pd.to_numeric(df[col])

    return df