import os
import requests as standart_requests
from curl_cffi import requests

# --- BİLGİLERİ GİTHUB SECRETS'TAN ÇEKİYORUZ ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
ZARA_URL = "https://www.zara.com/tr/tr/regular-fit-dokulu-polo-t-shirt-p00526447.html?v1=511360252&v2=2415619"
ZARA_API_URL = "https://www.zara.com/tr/tr/itxrest/catalog/v2/product/511360252/stock"

def telegram_mesaj_gonder(mesaj):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mesaj}
    try:
        standart_requests.post(url, json=payload, timeout=10)
    except Exception as e:
        pass

def botu_baslat():
    print("Siber hayalet modu aktif: TLS Fingerprint ile Zara API'sine sızılıyor...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": ZARA_URL
    }
    
    try:
        # impersonate="chrome120" parametresi sistemin tam bir Chrome gibi davranmasını sağlar
        response = requests.get(ZARA_API_URL, headers=headers, impersonate="chrome120", timeout=15)
        
        if response.status_code == 200:
            print("🔥 GÜVENLİK DUVARI AŞILDI! Veriler içeride:")
            veri = response.json()
            
            # Zara'nın L beden için hangi ID'yi kullandığını görmek için şimdilik tüm veriyi ekrana basıyoruz
            print(f"GELEN API VERİSİ: {veri}")
            telegram_mesaj_gonder("🚀 API duvarı aşıldı aga! Logları kontrol et, şifreyi çözüyoruz.")
        else:
            print(f"Kapı duvar aga. Hata Kodu: {response.status_code}")
            telegram_mesaj_gonder(f"⚠️ API hala engelliyor. Hata Kodu: {response.status_code}")
            
    except Exception as e:
        print(f"Sistem Hatası: {e}")

if __name__ == "__main__":
    botu_baslat()