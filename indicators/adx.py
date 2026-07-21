

import pandas as pd


def calculate_adx(data, period=14):

    high = data["High"]
    low = data["Low"]
    close = data["Close"]

    plus_dm = high.diff()
    minus_dm = -low.diff()

    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm < 0] = 0

    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(period).mean()

    plus_di = 100 * (
        plus_dm.rolling(period).mean() / atr
    )

    minus_di = 100 * (
        minus_dm.rolling(period).mean() / atr
    )

    dx = (
        (plus_di - minus_di).abs()
        / (plus_di + minus_di)
    ) * 100

    adx = dx.rolling(period).mean()

    result = pd.DataFrame()

    result["ADX"] = adx
    result["+DI"] = plus_di
    result["-DI"] = minus_di

    return result
