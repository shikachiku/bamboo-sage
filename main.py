
from adx import calculate_adx
from strategy import judge_strategy
from trend import judge_trend
from data_loader import load_nikkei
from heikin_ashi import calculate_heikin_ashi
from color import judge_color
from highlow import calculate_high5ma, calculate_low5ma
import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)




print("竹林の賢人 Version 1.6   開発版")

# =================
# 日経225データ取得
# =================

month_data = load_nikkei("5y", "1mo")
week_data = load_nikkei("5y", "1wk")
day_data = load_nikkei("6mo", "1d")

# ==========
# 平均足計算
# ==========
#ha = calculate_heikin_ashi(data)

# ======
# 色判定
# ======

#colors = judge_color(ha)

# =============
# トレンド判定
# =============

#trends = judge_trend(colors)

#ha["Trend"] = trends

# =============
# Color列を追加
# =============

#ha["Color"] = colors

# ====
# 表示
# ====

#print(
#    ha[
#        ["HA_Open", "HA_Close", "Color", "Trend"]
#    ].head()
#)



#print("月足データ")
#print(month_data.head())

#print("週足データ")
#print(week_data.head())

#print("日足データ")
#print(day_data.head())


month_ha = calculate_heikin_ashi(month_data)
week_ha = calculate_heikin_ashi(week_data)
day_ha = calculate_heikin_ashi(day_data)

month_adx = calculate_adx(month_data)


month_colors = judge_color(month_ha)
week_colors = judge_color(week_ha)
day_colors = judge_color(day_ha)


month_trends = judge_trend(month_colors)
week_trends = judge_trend(week_colors)
day_trends = judge_trend(day_colors)


month_ha["Color"] = month_colors
month_ha["Trend"] = month_trends

week_ha["Color"] = week_colors
week_ha["Trend"] = week_trends

day_ha["Color"] = day_colors
day_ha["Trend"] = day_trends


month_ha["High5MA"] = calculate_high5ma(month_data)
month_ha["Low5MA"] = calculate_low5ma(month_data)

week_ha["High5MA"] = calculate_high5ma(week_data)
week_ha["Low5MA"] = calculate_low5ma(week_data)

day_ha["High5MA"] = calculate_high5ma(day_data)
day_ha["Low5MA"] = calculate_low5ma(day_data)


print("【月足】")

print(month_ha[
    ["HA_Open", "HA_Close", "High5MA", "Low5MA", "Color", "Trend"]
].tail(3))

print()

print("【週足】")

print(week_ha[
    ["HA_Open", "HA_Close", "High5MA", "Low5MA", "Color", "Trend"]
].tail(3))

print()

print("【日足】")

print(day_ha[
    ["HA_Open", "HA_Close", "High5MA", "Low5MA", "Color", "Trend"]
].tail(3))


print()
print("=" * 40)
print("竹林の賢人 相場サマリー")
print("=" * 40)

print(f"月足 : {month_trends[-1]}")
print(f"週足 : {week_trends[-1]}")
print(f"日足 : {day_trends[-1]}")

print()

today = day_ha.iloc[-1]

print(f"現在HA終値 : {today['HA_Close']:.0f}")
print(f"High5MA    : {today['High5MA']:.0f}")
print(f"Low5MA     : {today['Low5MA']:.0f}")

print()

high_diff = today["High5MA"] - today["HA_Close"]
low_diff = today["HA_Close"] - today["Low5MA"]


if high_diff >= 0:
    print(f"↑ あと {high_diff:.0f} 円")
else:
    print(f"↑ {abs(high_diff):.0f} 円 上")

print()


if low_diff >= 0:
    print(f"↑ {low_diff:.0f} 円 上")
else:
    print(f"↓ {abs(low_diff):.0f} 円 下")


print()

if today["HA_Close"] > today["High5MA"]:
    print("現在位置 : High5MAより上")
elif today["HA_Close"] < today["Low5MA"]:
    print("現在位置 : Low5MAより下")
else:
    print("現在位置 : High5MAとLow5MAの間")


position = "MID"

if today["HA_Close"] > today["High5MA"]:
    position = "HIGH"

elif today["HA_Close"] < today["Low5MA"]:
    position = "LOW"

strategy, reasons = judge_strategy(
    month_trends[-1],
    week_trends[-1],
    day_trends[-1],
    position
)



print("判定")
print()
print(strategy)

print()
print("理由")

for r in reasons:
    print(r)


print()

print("【月足 ADX】")

print(
    month_adx[
        ["ADX", "+DI", "-DI"]
    ].tail(3)
)




