

import yfinance as yf


def load_nikkei():

    ticker = yf.Ticker("^N225")

    data = ticker.history(period="3mo")

    return data
