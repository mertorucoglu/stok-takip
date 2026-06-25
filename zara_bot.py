import json
from curl_cffi import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://www.zara.com/tr/tr/regular-fit-dokulu-polo-t-shirt-p00526447.html"
}

# Her beden için ayrı ayrı deneyelim
for size_id in [3, 4, 5]:
    url = f"https://www.zara.com/itxrest/1/catalog/store/11766/product/id/511360252/availability?sizeId={size_id}"
    r = requests.get(url, headers=headers, impersonate="chrome120", timeout=15)
    print(f"\nsizeId={size_id}:")
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))