import os
import re
from curl_cffi import requests
from bs4 import BeautifulSoup

ZARA_URL = "https://www.zara.com/tr/tr/regular-fit-dokulu-polo-t-shirt-p00526447.html?v1=511360252&v2=2415619"
URUN_ID = "511360252" # Senin tişörtün Zara sistemindeki kimliği

def botu_baslat():
    print("Siber radar aktif: Tüm JavaScript dosyalarının içi deşiliyor...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    try:
        response = requests.get(ZARA_URL, headers=headers, impersonate="chrome120", timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            scripts = soup.find_all("script")
            print(f"Toplam {len(scripts)} adet JavaScript dosyası bulundu. Taranıyor...\n")
            
            bulundu = False
            for i, script in enumerate(scripts):
                icerik = script.text
                
                # Eğer bu scriptin içinde bizim ürünün ID'si veya "stock" kelimesi geçiyorsa yakala!
                if URUN_ID in icerik or "stock" in icerik.lower():
                    print(f"🚨 DİKKAT! {i}. SCRIPT İÇİNDE GİZLİ VERİ BULUNDU! 🚨")
                    # Tamamını basarsak terminal çöker, sadece ilk 1000 karakterini görelim
                    print(icerik[:1000])
                    print("-" * 50 + "\n")
                    bulundu = True
            
            if not bulundu:
                print("Aga hiçbir scriptin içinde veri yok! Zara bu veriyi başka bir API'den canlı çekiyor demektir.")
                
        else:
            print(f"Sayfaya erişilemedi. HTTP Kodu: {response.status_code}")
            
    except Exception as e:
        print(f"Sistem Hatası: {e}")

if __name__ == "__main__":
    botu_baslat()