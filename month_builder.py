import pandas as pd
from pathlib import Path

# ===============================
# 入力・出力
# ===============================

INPUT = Path("data/live/JAPAN225CFD/1D_live.csv")
OUTPUT = Path("data/live/JAPAN225CFD/1M_live.csv")

# ===============================
# 読み込み
# ===============================

df = pd.read_csv(INPUT)

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date")

# ===============================
# 年・月
# ===============================

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month

# ===============================
# 月足生成
# ===============================

monthly = (
    df.groupby(["Year", "Month"])
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

monthly.to_csv(
    OUTPUT,
    index=False,
)

print("=" * 40)
print("月足生成完了")
print(monthly.tail())
print("=" * 40)
