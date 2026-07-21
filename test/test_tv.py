
from tvDatafeed import TvDatafeed, Interval

tv = TvDatafeed()

print("接続OK")

try:
    data = tv.get_hist(
        symbol="JP225",
        exchange="TVC",
        interval=Interval.in_daily,
        n_bars=5
    )

    print(data)

except Exception as e:
    print(e)
