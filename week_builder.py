import pandas as pd
from pathlib import Path

# ===============================
# 入力ファイル
# ===============================

INPUT = Path("data/live/JAPAN225CFD/1D_live.csv")
OUTPUT = Path("data/live/JAPAN225CFD/1W_live.csv")


# ===============================
# 読み込み
# ===============================

df = pd.read_csv(INPUT)

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date")


# ===============================
# 週番号作成
# （月曜始まり）
# ===============================

df["Year"] = df["Date"].dt.isocalendar().year
df["Week"] = df["Date"].dt.isocalendar().week


# ===============================
# 集約
# ===============================

weekly = (
    df.groupby(["Year", "Week"])
      .agg(
          Date=("Date", "first"),
          Open=("Open", "first"),
          High=("High", "max"),
          Low=("Low", "min"),
          Close=("Close", "last"),
          Volume=("Volume", "sum"),
      )
      .reset_index(drop=True)
)


# ===============================
# 保存
# ===============================

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

weekly.to_csv(
    OUTPUT,
    index=False,
)

print("=" * 40)
print("週足生成完了")
print(weekly.tail())
print("=" * 40)
