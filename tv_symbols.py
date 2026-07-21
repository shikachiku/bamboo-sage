from tv_protocol import send


def resolve_symbol(
    ws,
    chart_session,
    symbol,
):

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