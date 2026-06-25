import os
import requests as standart_requests
from curl_cffi import requests
from bs4 import BeautifulSoup

# --- BİLGİLERİ GİTHUB SECRETS'TAN ÇEKİYORUZ ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
ZARA_URL = "https://www.zara.com/tr/tr/regular-fit-dokulu-polo-t-shirt-p00526447.html?v1=511360252&v2=2415619"
HEDEF_BEDEN = "L"

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
    print("Siber hayalet modu aktif: Zara ana sayfasına sızılıyor...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    
    try:
        # impersonate="chrome120" ile bot korumasını ezip normal sayfayı indiriyoruz
        response = requests.get(ZARA_URL, headers=headers, impersonate="chrome120", timeout=15)
        
        if response.status_code == 200:
            print("🔥 Güvenlik duvarı aşıldı! HTML okunuyor...")
            
            # HTML'i BeautifulSoup ile parçalıyoruz
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Arkadaşının mantığı: CSS class'ı "size-selector-sizes-size" olan tüm <li> elementlerini bul
            bedenler = soup.find_all("li", class_=lambda c: c and "size-selector-sizes-size" in c)
            print(f"Toplam bulunan beden elementi sayısı: {len(bedenler)}")
            
            for beden in bedenler:
                # Bedenin içindeki yazıyı (etiketi) buluyoruz
                label = beden.find(class_=lambda c: c and "size-selector-sizes-size__label" in c)
                if label:
                    metin = label.text.strip()
                    
                    if metin == HEDEF_BEDEN or metin.startswith(f"{HEDEF_BEDEN} "):
                        # Elementin üzerindeki tüm CSS class'larını metin haline getiriyoruz
                        class_listesi = beden.get("class", [])
                        class_str = " ".join(class_listesi)
                        print(f"{HEDEF_BEDEN} beden bulundu. Class: {class_str!r}")
                        
                        if "--disabled" in class_str or "--unavailable" in class_str:
                            print("L beden hâlâ stokta yok.")
                            telegram_mesaj_gonder("🚀 Zara Stok Kontrolü: L beden hâlâ stokta yok, nöbetteyim aga!")
                            return
                        else:
                            print("🔥 STOK BULUNDU! 🔥")
                            telegram_mesaj_gonder(f"📣 AGA KOŞ L BEDEN STOĞA GİRDİ! \nLink: {ZARA_URL}")
                            return
            
            print("L beden listede bulunamadı veya sayfa yapısı farklı yüklendi.")
        else:
            print(f"Sayfaya erişilemedi. HTTP Kodu: {response.status_code}")
            
    except Exception as e:
        print(f"Sistem Hatası: {e}")

if __name__ == "__main__":
    botu_baslat()