import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- BİLGİLERİ GİTHUB SECRETS'TAN ÇEKİYORUZ ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
ZARA_URL = "https://www.zara.com/tr/tr/regular-fit-dokulu-polo-t-shirt-p00526447.html?v1=511360252&v2=2415619"
HEDEF_BEDEN = "L" 

def telegram_mesaj_gonder(mesaj):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Telegram Token veya Chat ID bulunamadı, mesaj gönderilemiyor!")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mesaj}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram mesajı gönderilemedi: {e}")

def driver_olustur():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    # Bot korumasını (anti-bot) aşmak için ekstra gizlilik argümanları ekledik
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def popup_kapat(driver):
    try:
        popup_button = driver.find_elements(
            By.XPATH, "//button[contains(text(), 'DEVAM ET') or contains(., 'TÜRKİYE')]"
        )
        if popup_button:
            popup_button[0].click()
            print("Pop-up yakalandı ve kapatıldı.")
            time.sleep(2)
    except Exception:
        pass

def l_bedeni_kontrol_et(driver):
    try:
        # Sayfada beden listesi belirene kadar en fazla 15 saniye AKILLI BEKLEME yapıyoruz
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.size-selector-sizes-size"))
        )
        
        # Beden elemanlarını topluyoruz
        bedenler = driver.find_elements(By.CSS_SELECTOR, "li.size-selector-sizes-size")
        print(f"Toplam bulunan beden elementi sayısı: {len(bedenler)}")
        
        for beden in bedenler:
            try:
                label = beden.find_element(By.CSS_SELECTOR, ".size-selector-sizes-size__label")
                metin = label.text.strip()
                
                if metin == HEDEF_BEDEN or metin.startswith(f"{HEDEF_BEDEN} "):
                    class_ozelligi = beden.get_attribute("class") or ""
                    print(f"{HEDEF_BEDEN} beden bulundu. Class: {class_ozelligi!r}")
                    
                    if "--disabled" in class_ozelligi or "--unavailable" in class_ozelligi:
                        return False
                    return True
            except Exception:
                continue
        
        print(f"{HEDEF_BEDEN} beden liste içinde eşleşmedi.")
        return None
        
    except Exception as e:
        print(f"Beden elementi sayfada yüklenemedi: {e}")
        return None

def botu_baslat():
    driver = driver_olustur()
    # Selenium'un bot olduğunu gizleyen ufak bir script çakıyoruz araya
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    
    print("Zara kontrol ediliyor...")
    try:
        driver.get(ZARA_URL)
        time.sleep(5)
        popup_kapat(driver)

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
        print(f"Hata: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    botu_baslat()