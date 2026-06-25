import os
import json
import requests as standart_requests
from curl_cffi import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
HEDEF_BEDEN = "L"
ZARA_URL = "https://www.zara.com/tr/tr/regular-fit-dokulu-polo-t-shirt-p00526447.html?v1=511360252&v2=2415619"

API_URL = "https://www.zara.com/itxrest/1/catalog/store/11766/product/id/511360252/availability"

def telegram_mesaj_gonder(mesaj):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mesaj}
    try:
        standart_requests.post(url, json=payload, timeout=10)
    except Exception:
        pass

def botu_baslat():
    print("API modu aktif: Zara stok verisi direkt çekiliyor...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "tr-TR,tr;q=0.9",
        "Referer": ZARA_URL
    }

    try:
        response = requests.get(API_URL, headers=headers, impersonate="chrome120", timeout=15)

        print(f"HTTP Kodu: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("Ham veri:")
            print(json.dumps(data, indent=2, ensure_ascii=False))

        else:
            print(f"Erişilemedi: {response.status_code}")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    botu_baslat()