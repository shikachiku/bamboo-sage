from pathlib import Path
import sys

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# =====================================
# Path
# =====================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_ROOT = Path(
    "/mnt/chromeos/shared/GoogleDrive/MyDrive/BambooSage/data"
)

OUTPUT_DIR = Path(
    "/mnt/chromeos/shared/GoogleDrive/MyDrive/BambooSage/chart/output"
)


# =====================================
# Parameter
# =====================================

SYMBOL = "TSE_JP225"
TIMEFRAME = "1M"

LOOKBACK = 120


# =====================================
# Load CSV
# =====================================

def load_data():

    path = (
        DATA_ROOT
        / SYMBOL
        / "analysis"
        / f"{TIMEFRAME}.csv"
    )

    print(path)

    df = pd.read_csv(path)

    df["Date"] = pd.to_datetime(df["Date"])

    df = df.sort_values("Date")

    df = df.tail(LOOKBACK)

    return df


# =====================================
# Chart
# =====================================

def create_chart(df):

    fig = make_subplots(
        rows=5,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[
            0.40,
            0.15,
            0.15,
            0.18,
            0.12
        ]
    )


    # -----------------------------
    # 1. Heikin Ashi
    # -----------------------------

    fig.add_trace(
        go.Candlestick(
            x=df["Date"],
            open=df["HA_Open"],
            high=df["HA_High"],
            low=df["HA_Low"],
            close=df["HA_Close"],
            name="HA"
        ),
        row=1,
        col=1
    )


    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["High5MA"],
            name="High5"
        ),
        row=1,
        col=1
    )


    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Low5MA"],
            name="Low5"
        ),
        row=1,
        col=1
    )


    # -----------------------------
    # 2. ADX_LEVEL
    # -----------------------------

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["ADX_LEVEL"],
            name="ADX_LEVEL"
        ),
        row=2,
        col=1
    )


    # -----------------------------
    # 3. DI
    # -----------------------------

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["+DI"],
            name="+DI"
        ),
        row=3,
        col=1
    )


    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["-DI"],
            name="-DI"
        ),
        row=3,
        col=1
    )


    # -----------------------------
    # 4. MACD
    # -----------------------------

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["MACD"],
            name="MACD"
        ),
        row=4,
        col=1
    )


    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["MACD_SIGNAL"],
            name="Signal"
        ),
        row=4,
        col=1
    )


    fig.add_trace(
        go.Bar(
            x=df["Date"],
            y=df["MACD_HIST"],
            name="Histogram"
        ),
        row=4,
        col=1
    )


    # -----------------------------
    # 5. Stochastic
    # -----------------------------

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["STOCH_K"],
            name="K"
        ),
        row=5,
        col=1
    )


    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["STOCH_D"],
            name="D"
        ),
        row=5,
        col=1
    )


    fig.add_hline(
        y=80,
        row=5,
        col=1
    )


    fig.add_hline(
        y=20,
        row=5,
        col=1
    )


    # -----------------------------
    # Layout
    # -----------------------------

    fig.update_layout(
        title=f"{SYMBOL} {TIMEFRAME}",
        height=1200,
        xaxis_rangeslider_visible=False
    )


    return fig



# =====================================
# Main
# =====================================

if __name__ == "__main__":

    df = load_data()

    fig = create_chart(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output = (
        OUTPUT_DIR
        / f"{SYMBOL}_{TIMEFRAME}.html"
    )

    fig.write_html(
        output,
        include_plotlyjs="cdn"
    )

    print("created:")
    print(output)

