###symbols.csv   ファイルを編集

import csv
from websocket import create_connection

from tv_protocol import (
    new_sessions,
    send_auth,
    create_chart_session,
    create_quote_session,
    add_symbol,
    send,
    receive,
    close,
)

URL = "wss://data.tradingview.com/socket.io/websocket"


def resolve_symbol(ws, chart_session, symbol):

    payload = (
        '{"symbol":"'
        + symbol +
        '","adjustment":"splits"}'
    )

    send(
        ws,
        "resolve_symbol",
        [
            chart_session,
            "symbol_1",
            "=" + payload,
        ],
    )


def check_symbol(tv_symbol):

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

        send_auth(ws)

        create_chart_session(ws, chart_session)
        create_quote_session(ws, quote_session)

        add_symbol(
            ws,
            quote_session,
            tv_symbol,
        )

        resolve_symbol(
            ws,
            chart_session,
            tv_symbol,
        )

        buffer = ""

        while True:

            msg = receive(ws)

            if not msg:
                continue

            if "~h~" in msg:
                ws.send(msg)
                continue

            buffer += msg

            if "symbol_resolved" in buffer:
                return True

            if (
                "symbol_error" in buffer
                or
                "no_such_symbol" in buffer
            ):
                return False

    except Exception:
        return False

    finally:

        if ws:
            close(ws)


def main():

    ok = 0
    ng = 0

    print()
    print("=" * 60)
    print("CHECK symbols.csv")
    print("=" * 60)

    with open("symbols.csv", newline="", encoding="utf-8-sig") as f:

        reader = csv.DictReader(f)

        for row in reader:

            symbol = row["TradingView"].strip()

            print(f"{symbol:<40}", end="")

            if check_symbol(symbol):
                print("TRUE")
                ok += 1
            else:
                print("ERROR")
                ng += 1

    print()
    print("=" * 60)
    print(f"TRUE  : {ok}")
    print(f"ERROR : {ng}")
    print("=" * 60)


if __name__ == "__main__":
    main()
