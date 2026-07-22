import pandas as pd
from pathlib import Path


# ===============================
# 入力ファイル
# ===============================

INPUT = Path(
    "data/WHSELFINVEST_JAPAN225CFD/raw/1D.csv"
)

OUTPUT = Path(
    "data/WHSELFINVEST_JAPAN225CFD/raw/1W.csv"
)


# ===============================
# 読み込み
# ===============================

df = pd.read_csv(INPUT)

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date")


# ===============================
# ISO週番号
# ===============================

iso = df["Date"].dt.isocalendar()

df["Year"] = iso.year

df["Week"] = iso.week


# ===============================
# 週足生成
# ===============================

weekly = (
    df.groupby(
        ["Year", "Week"],
        as_index=False,
    )
    .agg(
        Date=("Date", "first"),
        Open=("Open", "first"),
        High=("High", "max"),
        Low=("Low", "min"),
        Close=("Close", "last"),
        Volume=("Volume", "sum"),
    )
)


# ===============================
# 保存
# ===============================

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

weekly.to_csv(
    OUTPUT,
    index=False,
)

print("=" * 40)
print("週足生成完了")
print(weekly.tail())
print("=" * 40)