from tvDatafeed import TvDatafeed, Interval

print("TradingViewへ接続中...")

tv = TvDatafeed()

print("データ取得中...")

data = tv.get_hist(
    symbol="NIKKEI",
    exchange="TVC",
    interval=Interval.in_daily,
    n_bars=5
)

print(data)
