import requests


URL = (
    "https://tvc4.investing.com/"
    "ca5913e37d843ada7cc0e85b673032e5/"
    "1785446588/11/11/29/search"
)


PARAMS = {
    "limit": 30,
    "query": "1570",
    "type": "",
    "exchange": "",
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

    "Cookie":
        "_cf_bm="
        "ここに取得した_cf_bm値を入れる",
}


def main():

    session = requests.Session()

    response = session.get(
        URL,
        params=PARAMS,
        headers=HEADERS,
        timeout=10,
    )


    print("STATUS:", response.status_code)

    print()


    if response.status_code == 200:

        data = response.json()

        for item in data:

            print(
                item["full_name"],
                item["ticker"],
                item["type"],
            )

    else:

        print(response.text)



if __name__ == "__main__":

    main()