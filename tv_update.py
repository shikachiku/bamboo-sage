import time
from websocket import create_connection


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

from tv_symbols import resolve_symbol

URL = "wss://data.tradingview.com/socket.io/websocket"


def download_from_tv(
    symbol,
    timeframe,
    bars,
):

    chart_session, quote_session = new_sessions()

    ws = create_connection(
        URL,
        header=[
            "Origin: https://www.tradingview.com",
            "User-Agent: Mozilla/5.0",
        ],
    )

    try:

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
            symbol,
        )

        resolve_symbol(
            ws,
            chart_session,
            symbol,
        )

        print("Symbol request sent")

        series_sent = False

        buffer = ""

        timeout = time.time() + 15

        while True:

            if time.time() > timeout:

                raise TimeoutError(
                    "TradingView Timeout"
                )

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
                    bars,
                )

                print(
                    f"{timeframe} Series request sent"
                )

                series_sent = True

            if "timescale_update" in buffer:

                return buffer

    finally:

        close(ws)