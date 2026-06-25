import json
from curl_cffi import requests

URL1 = "https://www.zara.com/tr/tr/product/id/511360252/extra-detail?ajax=true"
URL2 = "https://www.zara.com/itxrest/3/returns/store/11766/product/511360252/sizing-info?locale=tr_TR&clientId=c9e6663d-094e-48bf-af1e-905013bc942c"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "tr-TR,tr;q=0.9",
    "Referer": "https://www.zara.com/tr/tr/regular-fit-dokulu-polo-t-shirt-p00526447.html"
}

for isim, url in [("EXTRA-DETAIL", URL1), ("SIZING-INFO", URL2)]:
    print(f"\n{'='*50}")
    print(f"TEST: {isim}")
    print(f"{'='*50}")
    try:
        r = requests.get(url, headers=headers, impersonate="chrome120", timeout=15)
        print(f"HTTP: {r.status_code}")
        if r.status_code == 200:
            print(json.dumps(r.json(), indent=2, ensure_ascii=False)[:2000])
    except Exception as e:
        print(f"Hata: {e}")