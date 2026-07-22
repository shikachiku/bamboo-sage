import json
import random
import string

# =========================================
# TradingView Session
# =========================================

# =========================================
# Session Generator
# =========================================

def new_sessions():

    chart_session = "cs_" + "".join(
        random.choice(string.ascii_lowercase)
        for _ in range(12)
    )

    quote_session = "qs_" + "".join(
        random.choice(string.ascii_lowercase)
        for _ in range(12)
    )

    return chart_session, quote_session

# =========================================
# Message Utility
# =========================================

def wrap_message(message):

    txt = json.dumps(message, separators=(",", ":"))

    return f"~m~{len(txt)}~m~{txt}"


def make_message(method, params):

    return wrap_message(
        {
            "m": method,
            "p": params,
        }
    )


def send(ws, method, params):

    ws.send(
        make_message(
            method,
            params,
        )
    )

# =========================================
# Protocol Commands
# =========================================

def send_auth(ws):

    send(
        ws,
        "set_auth_token",
        ["unauthorized_user_token"],
    )


def create_chart_session(ws, chart_session):

    send(
        ws,
        "chart_create_session",
        [chart_session, ""],
    )


def create_quote_session(ws, quote_session):

    send(
        ws,
        "quote_create_session",
        [quote_session],
    )


def add_symbol(
    ws,
    quote_session,
    symbol,
):

    send(
        ws,
        "quote_add_symbols",
        [
            quote_session,
            symbol,
        ],
    )

def create_series(
    ws,
    chart_session,
    timeframe,
    bars,
):

    interval = {
        "4H": "240",
        "1D": "1D",
        "1W": "1W",
        "1M": "1M",
    }.get(
        timeframe,
        timeframe,
    )

    send(
        ws,
        "create_series",
        [
            chart_session,
            "s1",
            "s1",
            "symbol_1",
            interval,
            bars,
            "",
        ],
    )


# =========================================
# Receive
# =========================================

def receive(ws):

    return ws.recv()


# =========================================
# Close
# =========================================

def close(ws):

    try:
        ws.close()

    except Exception:
        pass