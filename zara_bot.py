import os
import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import undetected_chromedriver as uc

# --- BİLGİLERİ GİTHUB SECRETS'TAN ÇEKİYORUZ ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
ZARA_URL = "https://www.zara.com/tr/tr/regular-fit-dokulu-polo-t-shirt-p00526447.html?v1=511360252&v2=2415619"
HEDEF_BEDEN = "L"

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


def driver_olustur():
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    
    # GitHub Actions'taki Chrome sürümünü otomatik buluyoruz
    try:
        c_version = subprocess.check_output(['google-chrome', '--version']).decode('utf-8')
        # Örn çıktı: "Google Chrome 149.0.7827.0" -> Buradan 149 sayısını çekiyoruz
        ana_surum = int(c_version.split()[2].split('.')[0])
        print(f"Sistemdeki Chrome Sürümü: {ana_surum} tespit edildi. Eşleşen sürücü indiriliyor...")
    except Exception as e:
        print("Chrome sürümü okunamadı, varsayılan 149 kullanılıyor.")
        ana_surum = 149

    # version_main parametresi ile birebir uyumlu sürümü zorluyoruz
    return uc.Chrome(options=options, version_main=ana_surum)

def l_bedeni_kontrol_et(driver):
    try:
        # Sayfada en az bir beden elemanı belirene kadar 20 saniye akıllı bekleme
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.size-selector-sizes-size"))
        )
        
        # Arkadaşının getirdiği o canavar CSS mantığı
        bedenler = driver.find_elements(By.CSS_SELECTOR, "li.size-selector-sizes-size")
        print(f"Toplam bulunan beden sayısı: {len(bedenler)}")
        
        for beden in bedenler:
            try:
                label = beden.find_element(By.CSS_SELECTOR, ".size-selector-sizes-size__label")
                metin = label.text.strip()
                
                if metin == HEDEF_BEDEN or metin.startswith(f"{HEDEF_BEDEN} "):
                    class_ozelligi = beden.get_attribute("class") or ""
                    print(f"{HEDEF_BEDEN} beden bulundu. Class: {class_ozelligi!r}")
                    
                    # Zara'nın o meşhur engelli sınıf etiketleri
                    if "--disabled" in class_ozelligi or "--unavailable" in class_ozelligi:
                        return False # Stokta yok
                    return True # Stok VAR!
            except Exception:
                continue
        
        print(f"{HEDEF_BEDEN} beden listede tam eşleşmedi.")
        return None
        
    except Exception as e:
        print(f"Beden tablosu sayfada yüklenemedi: {e}")
        return None

def botu_baslat():
    print("Undetected Tarayıcı başlatılıyor...")
    driver = driver_olustur()
    
    print("Zara gizli modda kontrol ediliyor...")
    try:
        driver.get(ZARA_URL)
        time.sleep(7) # Sayfanın oturması için biraz süre tanıyoruz

        sonuc = l_bedeni_kontrol_et(driver)

        if sonuc is True:
            print("🔥 STOK BULUNDU! 🔥")
            telegram_mesaj_gonder(f"📣 AGA KOŞ L BEDEN STOĞA GİRDİ! \nLink: {ZARA_URL}")
        elif sonuc is False:
            print("L beden hâlâ stokta yok.")
            telegram_mesaj_gonder("🚀 Zara Stok Kontrolü Yapıldı: L beden hâlâ stokta yok, nöbetteyim aga!")
        else:
            print("Sayfa yapısı tam yüklenemedi.")
            telegram_mesaj_gonder("⚠️ Zara sayfa yapısı yüklenemedi, bot sonraki turda tekrar deneyecek.")

    except Exception as e:
        print(f"Sistem Hatası: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    botu_baslat()