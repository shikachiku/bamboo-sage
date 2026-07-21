

import pandas as pd


def calculate_heikin_ashi(data):

    ha = pd.DataFrame(index=data.index)

    # 平均足終値
    ha["HA_Close"] = (
        data["Open"]
        + data["High"]
        + data["Low"]
        + data["Close"]
    ) / 4

    # 平均足始値
    ha["HA_Open"] = 0.0

    # 最初の1本
    ha.iloc[0, ha.columns.get_loc("HA_Open")] = (
        data["Open"].iloc[0]
        + data["Close"].iloc[0]
    ) / 2

    # 2本目以降
    for i in range(1, len(data)):
        ha.iloc[i, ha.columns.get_loc("HA_Open")] = (
            ha["HA_Open"].iloc[i-1]
            + ha["HA_Close"].iloc[i-1]
        ) / 2

    # 高値
    ha["HA_High"] = pd.concat(
        [data["High"], ha["HA_Open"], ha["HA_Close"]],
        axis=1
    ).max(axis=1)

    # 安値
    ha["HA_Low"] = pd.concat(
        [data["Low"], ha["HA_Open"], ha["HA_Close"]],
        axis=1
    ).min(axis=1)

    return ha




