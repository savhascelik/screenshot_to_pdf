import os
import time
import random
import pandas as pd
from datetime import datetime
from playwright.sync_api import sync_playwright
import img2pdf
from PIL import Image

def human_like_delay():
    """İnsan benzeri rastgele bekleme süreleri"""
    time.sleep(random.uniform(1, 3))

def setup_stealth_page(context):
    """Bot benzeri davranışları gizlemek için sayfa ayarları"""
    page = context.new_page()
    
    # User-Agent ve diğer tarayıcı özelliklerini ayarla
    page.set_extra_http_headers({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    })
    
    # WebDriver özelliğini gizle
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
    """)
    
    return page

def take_screenshot(url, output_dir, brand_name, url_index):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_brand_name = "".join(x for x in brand_name if x.isalnum() or x in " -_")
    safe_url = "".join(x for x in url.split("//")[-1] if x.isalnum() or x in ".-_")
    safe_url = safe_url[:50]
    
    brand_dir = os.path.join(output_dir, safe_brand_name)
    os.makedirs(brand_dir, exist_ok=True)
    
    filename = f"{timestamp}_{url_index}_{safe_url}.png"
    filepath = os.path.join(brand_dir, filename)
    
    try:
        with sync_playwright() as p:
            # Tarayıcı başlatma ayarları
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage'
                ]
            )
            
            context = browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                locale='en-US'
            )
            
            page = setup_stealth_page(context)
            
            # Rastgele scroll hareketleri
            def random_scroll():
                for _ in range(random.randint(2, 5)):
                    page.evaluate(f"() => window.scrollBy(0, {random.randint(200, 800)})")
                    human_like_delay()
            
            # Sayfayı yükle
            page.goto(url, timeout=60000, wait_until='domcontentloaded')
            human_like_delay()
            
            # CAPTCHA kontrolü
            if "robot" in page.title().lower() or "captcha" in page.content().lower():
                raise Exception("CAPTCHA algılandı")
            
            # İnsan benzeri etkileşimler
            random_scroll()
            
            # Ekran görüntüsü al
            page.screenshot(path=filepath, full_page=True)
            human_like_delay()
            
            browser.close()
        
        # PDF dönüştürme
        pdf_filename = filename.replace('.png', '.pdf')
        pdf_path = os.path.join(brand_dir, pdf_filename)
        
        with open(pdf_path, "wb") as f:
            img = Image.open(filepath)
            pdf_bytes = img2pdf.convert(img.filename)
            f.write(pdf_bytes)
        
        os.remove(filepath)
        return True, pdf_path
    
    except Exception as e:
        print(f"Hata oluştu ({url}): {str(e)}")
        return False, str(e)

def process_urls(excel_path, output_dir, max_retries=2):
    df = pd.read_excel(excel_path)
    urls = df.iloc[:, 2].tolist()
    brands = df.iloc[:, 4].tolist()
    
    report = {
        'success': 0,
        'fail': 0,
        'failed_urls': []
    }
    
    for i, (url, brand) in enumerate(zip(urls, brands)):
        if pd.isna(url) or str(url).strip() == '':
            continue
            
        print(f"İşleniyor {i+1}/{len(urls)}: {url}")
        
        retry_count = 0
        success = False
        
        while retry_count < max_retries and not success:
            success, result = take_screenshot(url, output_dir, brand, i)
            
            if not success and "CAPTCHA" in str(result):
                retry_count += 1
                print(f"CAPTCHA algılandı, {max_retries-retry_count} deneme hakkı kaldı")
                time.sleep(random.randint(10, 30))  # Uzun bekleme
            else:
                break
        
        if success:
            report['success'] += 1
        else:
            report['fail'] += 1
            report['failed_urls'].append({
                'url': url,
                'brand': brand,
                'error': result
            })
    
    report_path = os.path.join(output_dir, "process_report.txt")
    with open(report_path, 'w') as f:
        f.write(f"Toplam URL: {len(urls)}\n")
        f.write(f"Başarılı: {report['success']}\n")
        f.write(f"Başarısız: {report['fail']}\n\n")
        f.write("Başarısız URL'ler:\n")
        for item in report['failed_urls']:
            f.write(f"URL: {item['url']}\n")
            f.write(f"Marka: {item['brand']}\n")
            f.write(f"Hata: {item['error']}\n\n")
    
    return report

if __name__ == "__main__":
    excel_file = "input.xlsx"
    output_directory = "screenshots_pdfs"
    os.makedirs(output_directory, exist_ok=True)
    
    print("İşlem başlıyor...")
    start_time = time.time()
    
    result = process_urls(excel_file, output_directory)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("\nİşlem tamamlandı!")
    print(f"Toplam süre: {duration:.2f} saniye")
    print(f"Toplam URL: {result['success'] + result['fail']}")
    print(f"Başarılı: {result['success']}")
    print(f"Başarısız: {result['fail']}")
    print(f"Rapor dosyası: {os.path.join(output_directory, 'process_report.txt')}")