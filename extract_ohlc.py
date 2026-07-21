import re
import json
import pandas as pd
from datetime import datetime

with open("timescale_update.txt", "r", encoding="utf-8") as f:
    text = f.read()

# TradingViewメッセージを全部抽出
parts = re.findall(r'~m~\d+~m~({.*?})(?=~m~|$)', text, re.DOTALL)

target = None

for p in parts:
    try:
        obj = json.loads(p)

        if obj.get("m") == "timescale_update":
            target = obj
            break

    except Exception:
        pass

if target is None:
    print("timescale_update が見つかりません")
    exit()

bars = target["p"][1]["s1"]["s"]

rows = []

for b in bars:

    v = b["v"]

    rows.append({
        "Date": datetime.fromtimestamp(v[0]),
        "Open": v[1],
        "High": v[2],
        "Low": v[3],
        "Close": v[4],
        "Volume": v[5] if len(v) > 5 else 0
    })

df = pd.DataFrame(rows)

print(df.head())

df.to_csv("nikkei225.csv", index=False)

print()
print("="*40)
print("CSV保存完了")
print("件数:", len(df))
print("="*40)
