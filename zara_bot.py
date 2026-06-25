import os
import requests as standart_requests
from curl_cffi import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
ZARA_URL = "https://www.zara.com/tr/tr/regular-fit-dokulu-polo-t-shirt-p00526447.html?v1=511360252&v2=2415619"
API_URL = "https://www.zara.com/itxrest/1/catalog/store/11766/product/id/511360252/availability"

S_SKU = "450244943"  # String olarak tut

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
    print("Zara stok botu aktif...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": ZARA_URL
    }

    try:
        r = requests.get(API_URL, headers=headers, impersonate="chrome120", timeout=15)

        if r.status_code == 200:
            data = r.json()

            for item in data["skusAvailability"]:
                sku = str(item["sku"])  # Her zaman string'e çevir
                durum = item["availability"]

                if sku == S_SKU:
                    continue

                print(f"SKU: {sku} → {durum}")

                if durum in ("in_stock", "low_on_stock"):
                    print(f"🔥 STOK BULUNDU! SKU: {sku}")
                    telegram_mesaj_gonder(
                        f"📣 AGA KOŞ! ZARA'DA STOK GİRDİ!\n"
                        f"SKU: {sku} ({durum})\n"
                        f"Link: {ZARA_URL}"
                    )
                else:
                    print("Stok yok, beklemeye devam...")  # Sadece log, mesaj yok

        else:
            print(f"HTTP Hatası: {r.status_code}")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    botu_baslat()