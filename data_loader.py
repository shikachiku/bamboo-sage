

import yfinance as yf


def load_nikkei(period, interval):

    nikkei = yf.Ticker("^N225")

    data = nikkei.history(
        period=period,
        interval=interval
    )

    return data
