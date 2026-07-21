
import pandas as pd


def calculate_high5ma(data):
    return data["High"].rolling(5).mean()


def calculate_low5ma(data):
    return data["Low"].rolling(5).mean()
