import json
import pandas as pd
from datetime import datetime
from config import CSV_FILE

def tv_to_dataframe(msg):

    start = msg.find('"m":"timescale_update"')

    if start == -1:
        raise Exception("timescale_update が見つかりません")

    msg = msg[start - 1:]

    end = msg.find('~m~')

    if end != -1:
        msg = msg[:end]

    obj = json.loads(msg)

    bars = obj["p"][1]["s1"]["s"]

    rows = []

    for b in bars:

        v = b["v"]

        rows.append(
            {
                "Date": pd.to_datetime(v[0], unit="s"),
                "Open": float(v[1]),
                "High": float(v[2]),
                "Low": float(v[3]),
                "Close": float(v[4]),
                "Volume": float(v[5]) if len(v) > 5 else 0,
            }
        )

    df = pd.DataFrame(rows)

    df = df.set_index("Date")

    df = df.sort_index()

    return df


def save_csv(df, filename):

    df.to_csv(filename)

    print("=" * 40)
    print(f"{filename} 保存完了")
    print(f"件数 : {len(df)}")
    print("=" * 40)