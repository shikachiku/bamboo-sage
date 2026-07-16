
from data_loader import load_nikkei
from heikin_ashi import calculate_heikin_ashi

print("竹林の賢人 Version 0.7")

data = load_nikkei()

ha = calculate_heikin_ashi(data)

print(
    ha[
        ["HA_Open", "HA_High", "HA_Low", "HA_Close"]
    ].head()
)
