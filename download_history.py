from pathlib import Path
from websocket import create_connection

from symbol_loader import load_symbols

from folder_manager import (
    create_data_folders,
    RAW_DIR,
)

from tv_protocol import (
    new_sessions,
    send_auth,
    create_chart_session,
    create_quote_session,
    add_symbol,
    create_series,
    receive,
    close,
)

from tv_symbols import (
    resolve_symbol,
)

from tv_dataframe import (
    tv_to_dataframe,
    save_csv,
)

from color import title


URL = "wss://data.tradingview.com/socket.io/websocket"

BAR_COUNT = 10000

TIMEFRAMES = [
    "1D",
    "1W",
    "1M",
]


def download_one(symbol, timeframe):

    ws = None

    try:

        chart_session, quote_session = new_sessions()

        ws = create_connection(
            URL,
            header=[
                "Origin: https://www.tradingview.com",
                "User-Agent: Mozilla/5.0",
            ],
        )

        title(f"{symbol['Name']} {timeframe} Download Start")

        send_auth(ws)

        create_chart_session(
            ws,
            chart_session,
        )

        create_quote_session(
            ws,
            quote_session,
        )

        add_symbol(
            ws,
            quote_session,
            symbol["TradingView"],
        )

        resolve_symbol(
            ws,
            chart_session,
            symbol["TradingView"],
        )

        print("Symbol request sent")

        series_sent = False

        buffer = ""

        while True:

            msg = receive(ws)

            if not msg:
                continue

            if "~h~" in msg:

                ws.send(msg)

                continue

            buffer += msg

            if (
                "symbol_resolved" in buffer
                and
                not series_sent
            ):

                create_series(
                    ws,
                    chart_session,
                    timeframe,
                    BAR_COUNT,
                )

                print(
                    f"{timeframe} Series request sent"
                )

                series_sent = True

            if "timescale_update" in buffer:

                try:

                    df = tv_to_dataframe(
                        buffer
                    )

                    folder = Path(
                        "data"
                    ) / symbol["Folder"] / "raw"

                    folder.mkdir(
                        parents=True,
                        exist_ok=True,
                    )

                    filename = folder / f"{timeframe}.csv"

                    save_csv(
                        df,
                        filename,
                    )

                    title(
                        f"{symbol['Name']} {timeframe} Download Finished"
                    )

                    print(
                        f"Saved : {filename}"
                    )

                    break

                except Exception as e:

                    print("DataFrame ERROR")
                    print(e)

                    break

    except KeyboardInterrupt:

        print()
        print("Ctrl+C")

    except Exception as e:

        print()
        print("ERROR :", e)

    finally:

        if ws is not None:

            close(ws)

        title(
            f"{symbol['Name']} {timeframe} Disconnected"
        )
        
        
        
def main():

    create_data_folders()

    print()
    print("=" * 60)
    print("History Download")
    print("=" * 60)

    symbols = load_symbols()

    for symbol in symbols:

        print()
        print("=" * 60)
        print(symbol["Name"])
        print("=" * 60)

        for tf in TIMEFRAMES:

            print()
            print("-" * 60)
            print(f"{tf} Download")
            print("-" * 60)

            download_one(
                symbol,
                tf,
            )

    print()

    title(
        "ALL HISTORY DOWNLOAD COMPLETED"
    )


if __name__ == "__main__":

    main()