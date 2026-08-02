import requests
import pandas as pd
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

from settings import DATA_PATH


# ===================================
# Config
# ===================================

INVEST_SYMBOL_FILE = "invest_symbols.csv"

SAVE_DIR = DATA_PATH
# ===================================
# History Range
# ===================================

# timeframe別取得期間
# ここを変更するだけで取得期間を変更可能

HISTORY_DAYS = {


    # 日足
    # 例：50年
    "1D":
        365 * 10,


    # 1時間足
    # 例：10年
    "1H":
        200,


    # 週足
    "1W":
        365 * 30,


    # 月足
    "1M":
        365 * 30,

}

# ===================================
# Timezone
# ===================================

UTC_MINUS_4 = timezone(
    timedelta(hours=-4)
)


# ===================================
# Timeframe
# ===================================

TIMEFRAMES = {

    "1H": "60",

    "1D": "D",

    "1W": "W",

    "1M": "M",

}


# ===================================
# Investing API
# ===================================

BASE = "https://tvc4.investing.com"


HEADERS = {

    "User-Agent":
        "Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/150.0.0.0 Safari/537.36",

    "Origin":
        "https://tvc-invdn-cf-com.investing.com",

    "Referer":
        "https://tvc-invdn-cf-com.investing.com/",

    "X-Requested-With":
        "XMLHttpRequest",

}


# ===================================
# session token取得
# ===================================

def get_session():

    session = requests.Session()

    session.headers.update(HEADERS)

    return session



# ===================================
# symbol情報取得
# ===================================

def get_symbol_info(session, ticker):

    url = (
        BASE +
        "/691ff947cd653013b349943b50e12e94/"
        "1785478104/"
        "11/11/29/symbols"
    )


    params = {
        "symbol": ticker
    }


    r = session.get(
        url,
        params=params,
        timeout=10,
    )


    print("SYMBOL STATUS:", r.status_code)


    if r.status_code != 200:
        print(r.text)
        return None


    return r.json()



# ===================================
# candle取得
# ===================================

def get_history(
    session,
    ticker,
    timeframe
):


    now = int(time.time())


    url = (
        BASE +
        "/691ff947cd653013b349943b50e12e94/"
        "1785478104/"
        "11/11/29/history"
    )


    resolution_map = {

        "1H": "60",

        "1D": "D",

        "1W": "W",

        "1M": "M",

    }


    resolution = resolution_map[timeframe]


    print(
        "REQUEST RESOLUTION:",
        timeframe,
        resolution
    )


    history_days = HISTORY_DAYS[timeframe]


    print(
        "REQUEST DAYS:",
        history_days
    )


    params = {

        "symbol":
            ticker,

        "resolution":
            resolution,

        "from":
            now
            -
            history_days * 24 * 60 * 60,

        "to":
            now,

    }


    r = session.get(
        url,
        params=params,
        timeout=10,
    )


    print(
        "HISTORY STATUS:",
        r.status_code
    )


    if r.status_code != 200:

        print(r.text)

        return None


    data = r.json()


    if data["s"] != "ok":

        print(data)

        return None


    return data



# ===================================
# dataframe
# ===================================

def convert_dataframe(
    data,
    timeframe
):


    if timeframe == "1H":

        dates = [
            datetime.fromtimestamp(
                x,
                tz=UTC_MINUS_4
            )
            .strftime("%Y-%m-%d %H:00:00")
            for x in data["t"]
        ]

    else:

        dates = [
            datetime.fromtimestamp(
                x,
                tz=UTC_MINUS_4
            )
            .strftime("%Y-%m-%d")
            for x in data["t"]
        ]



    df = pd.DataFrame({

        "Date":
            dates,

        "Open":
            data["o"],

        "High":
            data["h"],

        "Low":
            data["l"],

        "Close":
            data["c"],

        "Volume":
            data["v"],

    })


    numeric_columns = [

        "Open",
        "High",
        "Low",
        "Close",
        "Volume",

    ]


    for col in numeric_columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


    df["Volume"] = (
        df["Volume"]
        .fillna(0)
    )


    return df



# ===================================
# download
# ===================================

def download(
    ticker,
    folder,
    timeframe
):


    print()

    print(
        "DOWNLOAD:",
        folder,
        ticker,
        timeframe
    )


    session = get_session()


    info = get_symbol_info(
        session,
        ticker
    )


    if info is None:

        print(
            "Symbol info failed"
        )

        return



    data = get_history(
        session,
        ticker,
        timeframe
    )


    if data is None:

        print(
            "History download failed"
        )

        return



    df = convert_dataframe(
        data,
        timeframe,
    )


    print()

    print(
        df.head()
    )


    # ===============================
    # Save Investing RAW
    # Merge mode
    # ===============================

    save_path = (
        SAVE_DIR /
        folder /
        "investraw"
    )


    save_path.mkdir(
        parents=True,
        exist_ok=True
    )


    file = (
        save_path /
        f"{timeframe}.csv"
    )


    # -------------------------------
    # Existing data merge
    # -------------------------------

    if file.exists():

        print()

        print(
            "MERGE EXISTING:",
            file
        )


        old_df = pd.read_csv(
            file
        )


        df = pd.concat(
            [
                old_df,
                df,
            ],
            ignore_index=True
        )


        df = (
            df
            .drop_duplicates(
                subset=["Date"],
                keep="last"
            )
        )


    # -------------------------------
    # Sort Date
    # -------------------------------

    df = (
        df
        .sort_values(
            "Date"
        )
        .reset_index(
            drop=True
        )
    )


    # -------------------------------
    # Save
    # -------------------------------

    df.to_csv(
        file,
        index=False,
        encoding="utf-8"
    )


    print()

    print(
        "SAVE:",
        file
    )

    print(
        "ROWS:",
        len(df)
    )



# ===================================
# main
# ===================================

def main():


    symbols = pd.read_csv(
        INVEST_SYMBOL_FILE
    )


    for _, row in symbols.iterrows():


        if row["Enable"] != 1:

            continue



        for timeframe in TIMEFRAMES:


            download(

                str(row["Investing"]),

                row["Folder"],

                timeframe

            )


            time.sleep(1)



if __name__ == "__main__":

    main()