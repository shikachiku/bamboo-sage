from websocket import create_connection

from symbol_loader import load_symbols

from tv_protocol import (
    new_sessions,
    send_auth,
    create_chart_session,
    create_quote_session,
    add_symbol,
    receive,
    close,
)

from tv_symbols import resolve_symbol

URL = "wss://data.tradingview.com/socket.io/websocket"


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

            if "~h~" in msg:

                ws.send(msg)

                continue

            buffer += msg

            if "symbol_resolved" in buffer:

                return True

            if "symbol_error" in buffer:

                return False

    except Exception:

        return False

    finally:

        if ws:

            close(ws)


def main():

    symbols = load_symbols()

    ok = []
    ng = []

    print()
    print("=" * 60)
    print("SYMBOL CHECK")
    print("=" * 60)

    for symbol in symbols:

        tv = symbol["TradingView"]

        result = check_symbol(tv)

        if result:

            print(f"{tv:<40} TRUE")

            ok.append(tv)

        else:

            print(f"{tv:<40} ERROR")

            ng.append(tv)

    print()
    print("=" * 60)
    print(f"OK     : {len(ok)}")
    print(f"ERROR  : {len(ng)}")
    print("=" * 60)

    if ng:

        print()
        print("ERROR SYMBOLS")
        print("-" * 60)

        for s in ng:

            print(s)


if __name__ == "__main__":

    main()