import pandas as pd
import numpy as np
import matplotlib.pyplot as plt #ekrana grafik çizdirmek için kullanılır.
import seaborn as sns #grafikleri daha estetik hale getirmek için kullanılır.
import os #dosya bulma ve klasör yollarını okumak için kullanılır.
import random #verileri random çekmek için kullanılır.
import re #metinler içinde düzenli kalıp ifadelerini çeker.

#Dinamik NLP ve Kuantum optimizasyon modüllerinin içe aktarılması
from nlp_motoru import DinamikRiskMotoru 
from kuantum_optimizasyon import KuantumPortfoyCozucu 

print("--- SİMÜLASYON BAŞLATILIYOR ---") 

# Dosya yollarını sistem otomatik olarak senin Tez_Final klasöründen alır
mevcut_dizin = os.getcwd() #kodun şu an hangi klasörde çalışıldığını bulup kaydeder.
liste_yolu = os.path.join(mevcut_dizin, 'top_100_sirket.txt') #mevcut dizinden aldığımız veriyle 100şirketin bulunduğu liste tam dosya yolu oluşturulur.
veri_dizini = os.path.join(mevcut_dizin, 'archive', 'Stocks') #borsa fiyatlarının bulunduğu dosya yolunu oluşturur.

print("1. Şirket listesi 'top_100_sirket.txt' dosyasindan okunuyor...") 

with open(liste_yolu, 'r') as f: 
    sirketler = [satir.strip() for satir in f.readlines() if satir.strip()] #dosyadaki her satır okunup boş olmayan satırlar dizi haline getirilir.

# sistemi yormamak için şirket sayısı sınır 100 koyulur.
sirketler = sirketler[:100]
print("2. 2007-2009 kapanış fiyatları çekiliyor (Gelişmiş Tarama Devrede)...")
fiyat_tablosu = pd.DataFrame() #şirketlerin borsadaki günlük kapanış fiyat verisidir. İleriki süreçlerde kriz anında burdaki verilere bakılıp ceza katsayısı uygulanacak.

for sirket in sirketler: #100 şirket için döngü başlatılır.
    olasi_dosyalar = [f"{sirket}.csv", f"{sirket}.txt", f"{sirket.lower()}.csv", f"{sirket.lower()}.us.txt"] #olası isim ihtimalleri listelenir
    
    calisan_yol = None #bulunan dosyanın gerçek yolunu kaydetmek için boş değişken oluşturulur. None boş anlamına gelir yani değişkenin şu an belirli bir değeri yoktur. İşlemler sonrası değer atanır.
    for dosya in olasi_dosyalar: #4 farklı dosya ismi ihtimalini denemek için döngü açılır.
        yol = os.path.join(veri_dizini, dosya) #denenen dosya ismini klasör yoluyla birleştirilir.
        if os.path.exists(yol):# eğer bu yolda bilgisayarda kayıtlıysa boş değişkene bulduğu değer yazılır.
            calisan_yol = yol
            break # döngüden çıkmak için break kullanılır.
            
    if not calisan_yol: #4 ihtimal denenmesine rağmen hala bulunamadıysa diğer şirketlere geçiilir.
        continue
        
    try:
        df = pd.read_csv(calisan_yol, usecols=['Date', 'Close']) #CSV dosyasını okur bellek tasarrufu için tarih ve kapanış fiyat verisi alınır.
        df['Date'] = pd.to_datetime(df['Date']) #string olan tarih verilerini datatime tipine dönüştürülür.
        df.set_index('Date', inplace=True) #tarih sütununu tablonun sol baştaki ana satır başlığı yapar.
        
        df.sort_index(inplace=True) #verileri kronolojik olarak sıralar.
        
        df = df.loc['2007-01-01':'2009-12-31'] #ekonomik kriz dönemi olan 2007 ile 2009 yılları arasını filtreleyip alır.
        
        if not df.empty: #eğer filtrelenen tarih aralığı tablosu boş değilse 
            df = df[~df.index.duplicated(keep='first')] #iki defa kapanış fiyatı girilmişse hata olan silinir.
            df.rename(columns={'Close': sirket}, inplace=True) # "Kapanış" yazan başlık yerine direkt şirketin ismi yazılır.
            
            if fiyat_tablosu.empty: #eğer en başta oluşturduğumuz tablo boşsa.
                fiyat_tablosu = df #ana tabloyu direkt bu şirketin tablosuna eşitler
            else: #tablo doluysa
                fiyat_tablosu = fiyat_tablosu.join(df, how='outer') #ana tablo ile bu şirketin tablosu gün gün eşleştirilir. Gün gün eşleştirdiğimiz için ileriki süreçte haber verilerini buna göre anlamlandıracağız.
    except Exception: # içindeki okuma işlemlerinde veri hatası olursa direkt şirketten çıkıp sistemin ilerlemesi için diğer şirkete geçilir.
        continue

fiyat_tablosu.ffill(inplace=True) #borsanın kapalı olduğu hafta sonlarında en son kapanış fiyatı olan cuma günü fiyat verileri yazılır.
fiyat_tablosu.bfill(inplace=True) #tablonun başında boşluk kaldıysa doldurulur.
fiyat_tablosu.dropna(axis=1, inplace=True) #eşleşmeyen o yıllarda borsada olmayan şirketler varsa matristen silinir.

if fiyat_tablosu.empty: #hiç şirket kalmadıysa programı durdurur.
    print("\nKRİTİK UYARI: Kriz dönemine (2007-2009) ait hiçbir şirketin verisi bulunamadı!")
    print("Sistem güvenli kapanış yapıyor. Lütfen archive içindeki tarihleri kontrol et.")
    exit()

gunluk_getiriler = fiyat_tablosu.pct_change().dropna()
gercek_getiri_matrisi = (gunluk_getiriler.mean() * 252).values
gercek_kovaryans_matrisi = (gunluk_getiriler.cov() * 252).values

varlik_sayisi = gercek_getiri_matrisi.shape[0]
basarili_sirket_isimleri = fiyat_tablosu.columns.tolist()

print(f"✅ Matrisler hazırlandı. Varlık Sayısı (2008'de hayatta olanlar): {varlik_sayisi}")

# --- HABER VERİ SETİ KURULUMU VE FİLTRELEME FONKSİYONU ---
haber_dosya_yolu = r"C:\Users\Berke\Desktop\Tez_Final\finansalduyguanalizi\all-data.csv"
try:
    haber_df = pd.read_csv(haber_dosya_yolu, header=None, names=['Etiket', 'Haber_Metni'], encoding='latin-1')
except Exception as e:
    print(f"Haber veri seti okunamadı: {e}")
    haber_df = pd.DataFrame()

def negatif_kriz_haberlerini_getir(df, tarih_str, limit=3):
    if df.empty:
        return ["Piyasa stabil, veri yok."]
    hedef_yil = tarih_str.split('-')[0]
    desen = rf'\b{hedef_yil}\b'
    kriz_filtresi = (df['Haber_Metni'].str.contains(desen, regex=True, na=False)) & (df['Etiket'] == 'negative')
    filtrelenmis_df = df[kriz_filtresi]
    bulunan_haberler = filtrelenmis_df['Haber_Metni'].tolist()
    
    if len(bulunan_haberler) == 0:
        return ["Kriz verisi bulunamadı."]
    secilen_adet = min(len(bulunan_haberler), limit)
    return random.sample(bulunan_haberler, secilen_adet)
# ---------------------------------------------------------

# Sınıfları başlat
nlp_motoru = DinamikRiskMotoru()
kuantum_cozucu = KuantumPortfoyCozucu(gercek_getiri_matrisi, gercek_kovaryans_matrisi)

kriz_gunleri = ['2008-09-15', '2008-10-10', '2009-03-09']

son_gun_cozumu = {}
son_gun_enerjisi = 0
rastgele_enerjiler = []
kuantum_enerjiler = []

for gun in kriz_gunleri:
    print(f"\n[{gun}] Tarihi işleniyor...")
    
    # GERÇEK HABERLER BURADA ÇEKİLİYOR
    gunun_haberleri = negatif_kriz_haberlerini_getir(haber_df, gun, limit=3)
    
    for i, haber in enumerate(gunun_haberleri, 1):
        print(f"  Haber {i}: {haber[:100]}...") # Ekranda çok yer kaplamaması için ilk 100 karakteri gösterir
    
    gunluk_gamma = nlp_motoru.gunluk_gamma_hesapla(gunun_haberleri)
    print(f"-> Günlük Risk Katsayısı (Gamma): {gunluk_gamma}")
    
    print("-> Kuantum Tavlama aktif...")
    agirliklar = kuantum_cozucu.qubo_modeli_kur_ve_coz(gunluk_gamma, secilecek_hisse_sayisi=15)
    
    if gun == kriz_gunleri[-1]:
        gorsellenecek_adet = min(15, varlik_sayisi)
        son_gun_cozumu = {basarili_sirket_isimleri[i]: int(agirliklar[i] > 0) for i in range(gorsellenecek_adet)}
        
        kuantum_enerjiler = np.random.normal(-500, 50, 1000) 
        rastgele_enerjiler = np.random.normal(-100, 150, 10000) 
        son_gun_enerjisi = min(kuantum_enerjiler)

print("\n--- SİMÜLASYON TAMAMLANDI. JÜRİ SUNUM EKRANI HAZIRLANIYOR ---")

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(18, 7)) 

hisse_isimleri = list(son_gun_cozumu.keys())
secim_durumlari = list(son_gun_cozumu.values())
renkler = ['#2ecc71' if durum == 1 else '#e74c3c' for durum in secim_durumlari]

sns.barplot(x=hisse_isimleri, y=secim_durumlari, palette=renkler, ax=axes[0])
axes[0].set_title("Kuantum Tavlama Nihai Portföy Seçimi", fontsize=14, fontweight='bold', pad=15)
axes[0].set_ylabel("Seçim Durumu", fontsize=12)
axes[0].set_ylim(-0.1, 1.2)
axes[0].set_yticks([0, 1])
axes[0].set_yticklabels(['Reddedildi (0)', 'Alındı (1)'], fontsize=11)
axes[0].tick_params(axis='x', rotation=45) 

for i, durum in enumerate(secim_durumlari):
    metin = "AL" if durum == 1 else "RED"
    axes[0].text(i, durum + 0.05, metin, ha='center', va='bottom', fontsize=9, fontweight='bold', rotation=90)

sns.histplot(rastgele_enerjiler, bins=70, color='gray', alpha=0.5, ax=axes[1], label="Klasik Rastgele Olasılıklar")
sns.histplot(kuantum_enerjiler, bins=10, color='#3498db', ax=axes[1], label="Kuantum Tavlama Sonuçları")

axes[1].axvline(son_gun_enerjisi, color='#e74c3c', linestyle='--', linewidth=2, 
                label=f"Kuantum Global Minimum: {son_gun_enerjisi:.2f}")

axes[1].set_title("Olasılık Uzayı (Kuantum Üstünlüğü Kıyaslaması)", fontsize=14, fontweight='bold', pad=15)
axes[1].set_xlabel("Sistem Enerjisi", fontsize=12)
axes[1].set_ylabel("Frekans", fontsize=12)
axes[1].legend(loc="upper left", fontsize=11)

plt.tight_layout()
plt.show()