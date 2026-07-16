
from data_loader import load_nikkei
from heikin_ashi import calculate_heikin_ashi
from color import judge_color

print("竹林の賢人 Version 0.8")

# 日経225データ取得
data = load_nikkei()

# 平均足計算
ha = calculate_heikin_ashi(data)

# 色判定
colors = judge_color(ha)

# Color列を追加
ha["Color"] = colors

# 表示
print(ha[["HA_Open", "HA_Close", "Color"]].head())
