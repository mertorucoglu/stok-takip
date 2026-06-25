import os
from curl_cffi import requests
from bs4 import BeautifulSoup

ZARA_URL = "https://www.zara.com/tr/tr/regular-fit-dokulu-polo-t-shirt-p00526447.html?v1=511360252&v2=2415619"

def botu_baslat():
    print("Siber hayalet modu aktif: Zara'nın SEO verisi röntgenleniyor...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    try:
        response = requests.get(ZARA_URL, headers=headers, impersonate="chrome120", timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            scripts = soup.find_all("script", type="application/ld+json")
            
            print(f"\nToplam {len(scripts)} adet SEO (ld+json) bloğu bulundu.\n")
            
            # Arkadaşının dediği testi yapıyoruz: İçinde ne var ekrana bas!
            for i, script in enumerate(scripts, 1):
                print(f"--- {i}. JSON BLOĞU (İLK 1000 KARAKTER) ---")
                print(script.text.strip()[:1000])
                print("------------------------------------------\n")
                
        else:
            print(f"Sayfaya erişilemedi. HTTP Kodu: {response.status_code}")
            
    except Exception as e:
        print(f"Sistem Hatası: {e}")

if __name__ == "__main__":
    botu_baslat()