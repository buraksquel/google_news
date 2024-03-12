import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import boto3
from datetime import datetime

def aciklama_cek(url):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    p_etiketi = soup.find("p")
    return p_etiketi.text if p_etiketi else "Kısa açıklama bulunamadı..."

def url_cek(site_url):
    response = requests.get(site_url, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    canonical_link = soup.find("link", rel="canonical")
    if canonical_link:
        orijinal_url = canonical_link.get("href")
        return orijinal_url
    else:
        return None

def aws_s3_kaydet(dosya_adi, icerik):
    with open("config.txt", "r", encoding="utf-8") as config_file:
        lines = config_file.readlines()
        aws_access_key_id = lines[0].strip().split('=')[1]
        aws_secret_access_key = lines[1].strip().split('=')[1]
        aws_region = lines[2].strip().split('=')[1]

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    icerik_utf8 = icerik.encode("utf-8")

    s3.put_object(Body=icerik_utf8, Bucket='casegooglenews', Key=dosya_adi)

def google_news(News):
    kategoriler = {
        "spor": {"kategori": "Spor", "base_url": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FuUnlHZ0pVVWlnQVAB?hl=tr&gl=TR&ceid=TR%3Atr"},
        "sağlık": {"kategori": "Sağlık", "base_url": "https://news.google.com/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FuUnlLQUFQAQ?hl=tr&gl=TR&ceid=TR%3Atr"},
        "iş": {"kategori": "İş", "base_url": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FuUnlHZ0pVVWlnQVAB?hl=tr&gl=TR&ceid=TR%3Atr"},
        "dünya": {"kategori": "Dünya", "base_url": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuUnlHZ0pVVWlnQVAB?hl=tr&gl=TR&ceid=TR%3Atr"}
    }

    if News.lower() not in kategoriler:
        print("Geçersiz kategori.")
        return

    kategori = kategoriler[News.lower()]["kategori"]
    base_url = kategoriler[News.lower()]["base_url"]

    response = requests.get(base_url)
    if response.status_code != 200:
        return
    html_icerigi = response.content
    soup = BeautifulSoup(html_icerigi, "html.parser")

    haberler = soup.find_all("div", class_="f9uzM")

    for siralama, haber_bilgisi in enumerate(haberler, start=1):
        kaynak = haber_bilgisi.find("div", {"class": "a7P8l"}).text.strip()
        baslik = haber_bilgisi.find("a", class_="gPFEn").text.strip()
        kisa_aciklama_url = haber_bilgisi.find("a", class_="gPFEn").get("href")
        tarih_zaman = haber_bilgisi.find("time", class_="hvbAAd").get("datetime")

        full_url = f"https://news.google.com{kisa_aciklama_url}"
        orijinal_url = url_cek(full_url)
        kisa_aciklama = aciklama_cek(full_url)

        dosya_adi = f"{kategori}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{siralama}.txt"
        icerik = f"{kategori} Verileri:\nSıralama: {siralama}\nKategori: {kategori}\nBaşlık: {baslik}\nKısa Açıklama: {kisa_aciklama}\nKaynak: {kaynak}\nTarih/Zaman: {tarih_zaman}\nURL: {orijinal_url}\n***********************************\n"

        aws_s3_kaydet(dosya_adi, icerik)

google_news("spor")
google_news("sağlık")
google_news("iş")
google_news("dünya")
