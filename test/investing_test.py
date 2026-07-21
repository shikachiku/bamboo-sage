

url = "https://tvc4.investing.com/522241f0a1507b88a2307b1e7db76eb3/1784279091/11/11/29/history?symbol=178&resolution=M&from=851159820&to=1784279880"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://tvc-invdn-cf-com.investing.com/",
    "Origin": "https://tvc-invdn-cf-com.investing.com",
    "Accept": "*/*"
}

r = requests.get(url, headers=headers)

print("Status:", r.status_code)
print(r.text[:500])



















