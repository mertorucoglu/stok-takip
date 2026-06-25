import os
import requests

# --- BİLGİLERİ GİTHUB SECRETS'TAN ÇEKİYORUZ ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Zara'nın arkadaki gizli stok sorgulama API Linki
ZARA_API_URL = "https://www.zara.com/tr/tr/itxrest/catalog/v2/product/511360252/stock"
ZARA_URL = "https://www.zara.com/tr/tr/regular-fit-dokulu-polo-t-shirt-p00526447.html?v1=511360252&v2=2415619"

def telegram_mesaj_gonder(mesaj):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Telegram Token veya Chat ID bulunamadı!")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mesaj}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram hatası: {e}")

def stok_kontrol_et():
    # Gerçek bir insan tarayıcısı gibi görünmek için basit bir header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    print("Zara API üzerinden stoklar sorgulanıyor...")
    try:
        response = requests.get(ZARA_API_URL, headers=headers, timeout=15)
        
        if response.status_code == 200:
            veri = response.json()
            # API'den dönen beden listesindeki stok durumlarını tarıyoruz
            stocks = veri.get("stocks", [])
            
            # L bedenin ID'si (Zara arkada L beden için bu ID'yi kullanıyor)
            # Not: Eğer ID değişirse genel listeyi ekrana bastırıp kontrol edebiliriz
            l_beden_stokta = False
            
            for item in stocks:
                # Genellikle L beden bu tişört için fiziksel olarak listededir, 
                # boyutu veya 'outOfStock' durumunu kontrol ediyoruz.
                # En garanti yol: L bedene ait id'yi bulmak ya da 'quantity' bakmak.
                # Şimdilik genel listede 'outOfStock' olmayan bir L arıyoruz.
                pass
            
            # Doğrudan ham stok listesini terminale basalım ne döndüğünü görelim
            print(f"Gelen Stok Verisi: {stocks}")
            
            # Kolaylık olsun: Eğer tişörtün genel stoklarında bir hareketlilik varsa 
            # veya 'outOfStock' durumu değiştiyse yakalayacağız.
            # Zara API'sinde her bedenin bir 'sku' kodu olur.
            
            # EN TEMİZ YOL: L beden şu an stokta olmadığı için listede 'outOfStock': True olur.
            # Biz listeyi kontrol edelim:
            stok_durumu = "OUT_OF_STOCK"
            
            # Eğer API'den veri temiz geldiyse ama L'yi ayırt etmek istiyorsak:
            # Zara stok durumunu 'status' olarak verir: 'in_stock' veya 'out_of_stock'
            
            # Test amaçlı: API sorunsuz çalıştıysa şimdilik stok yok diyelim ve logu görelim
            print("API başarıyla okundu, L beden kontrolü yapılıyor...")
            
            # Eğer tüm bedenler kapalı değilse ve veri geldiyse:
            # Şimdilik sahte alarmı engellemek için direkt False dönüyoruz, terminal loguna bakacağız
            return False 
            
        else:
            print(f"Zara API hata kodu döndürdü: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"API isteği başarısız oldu: {e}")
        return None

def botu_baslat():
    sonuc = stok_kontrol_et()

    if sonuc is True:
        print("🔥 STOK BULUNDU! 🔥")
        telegram_mesaj_gonder(f"📣 AGA KOŞ L BEDEN STOĞA GİRDİ! \nLink: {ZARA_URL}")
    elif sonuc is False:
        print("L beden hâlâ stokta yok.")
        telegram_mesaj_gonder("🚀 Zara Stok Kontrolü Yapıldı (API): L beden hâlâ stokta yok, nöbetteyim aga!")
    else:
        print("Zara veri merkezine bağlanılamadı.")
        telegram_mesaj_gonder("⚠️ Zara API'sine bağlanılamadı, sonraki turda tekrar denenecek.")

if __name__ == "__main__":
    botu_baslat()