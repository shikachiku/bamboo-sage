import requests
import time


URL = (
    "https://tvc4.investing.com/"
    "35c34c28e1d5995be8cd9b0fae7e67c2/"
    "1785452513/11/11/29/history"
)


PARAMS = {
    "symbol": "953291",
    "resolution": "D",
    "from": int(time.time()) - 365 * 24 * 60 * 60,
    "to": int(time.time()),
}


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
}


def main():

    response = requests.get(
        URL,
        params=PARAMS,
        headers=HEADERS,
        timeout=10,
    )


    print("STATUS:", response.status_code)

    print()


    if response.status_code != 200:

        print(response.text)

        return


    data = response.json()


    print("STATUS DATA:", data["s"])

    print()


    for i in range(5):

        print(
            data["t"][i],
            data["o"][i],
            data["h"][i],
            data["l"][i],
            data["c"][i],
            data["v"][i],
        )


if __name__ == "__main__":

    main()