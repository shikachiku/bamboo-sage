from websocket import create_connection

url = "wss://data.tradingview.com/socket.io/websocket"

print("Connecting...")

try:
    ws = create_connection(
        url,
        timeout=10,
        header=[
            "Origin: https://www.tradingview.com",
            "User-Agent: Mozilla/5.0"
        ]
    )

    print("===================================")
    print("CONNECTED!")
    print("===================================")

    ws.close()

except Exception as e:
    print("ERROR")
    print(e)
