from pathlib import Path
from websocket import create_connection

from config import SYMBOL

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

TIMEFRAME = "60"


def download():

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

        title("60min Download Start")

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
            SYMBOL,
        )

        resolve_symbol(
            ws,
            chart_session,
            SYMBOL,
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
                    TIMEFRAME,
                    BAR_COUNT,
                )

                print("60min Series request sent")

                series_sent = True
            if "timescale_update" in buffer:

                try:

                    df = tv_to_dataframe(
                        buffer
                    )

                    filename = (
                        RAW_DIR /
                        "60.csv"
                    )

                    save_csv(
                        df,
                        filename,
                    )

                    title(
                        "60min Download Finished"
                    )

                    print(
                        f"Saved : {filename}"
                    )

                    break

                except Exception as e:

                    print(
                        "DataFrame ERROR"
                    )

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
            "60min Disconnected"
        )
if __name__ == "__main__":

    create_data_folders()

    print()
    title("60min History Download")

    print("=" * 60)
    print("60min History Download")
    print("=" * 60)

    download()

    print()

    title(
        "60min DOWNLOAD COMPLETED"
    )