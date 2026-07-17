import pandas as pd
import random
import re
from nlp_motoru import DinamikRiskMotoru

def negatif_kriz_haberlerini_getir(df, tarih_str, limit=3):
    """
    Belirtilen tarihin yılına ait sadece 'negative' etiketli haberleri bulur
    ve kriz simülasyonu için içlerinden rastgele seçim yapar.
    """
    hedef_yil = tarih_str.split('-')[0]
    desen = rf'\b{hedef_yil}\b'
    
    # 1. Filtre: Yılı içersin
    # 2. Filtre: Etiketi kesinlikle 'negative' olsun
    kriz_filtresi = (df['Haber_Metni'].str.contains(desen, regex=True, na=False)) & (df['Etiket'] == 'negative')
    
    filtrelenmis_df = df[kriz_filtresi]
    bulunan_haberler = filtrelenmis_df['Haber_Metni'].tolist()
    
    if len(bulunan_haberler) == 0:
        return ["Kriz verisi bulunamadı, piyasa kapalı."]
        
    # Yeterli haber varsa limit kadar rastgele seç, yoksa eldekilerin hepsini al
    secilen_adet = min(len(bulunan_haberler), limit)
    return random.sample(bulunan_haberler, secilen_adet)

print("--- NEGATİF HABER (KRİZ) FİLTRESİ BAŞLATILIYOR ---")

dosya_yolu = r"C:\Users\Berke\Desktop\Tez_Final\finansalduyguanalizi\all-data.csv"

try:
    df = pd.read_csv(dosya_yolu, header=None, names=['Etiket', 'Haber_Metni'], encoding='latin-1')
    
    kriz_gunleri = ['2008-09-15', '2008-10-10', '2009-03-09']
    nlp_motoru = DinamikRiskMotoru()
    
    for gun in kriz_gunleri:
        print(f"\n[{gun}] Tarihi için sadece NEGATİF haberler taranıyor...")
        
        gunun_haberleri = negatif_kriz_haberlerini_getir(df, gun, limit=3)
        
        for i, haber in enumerate(gunun_haberleri, 1):
            print(f"  {i}. [NEGATİF] {haber}")
            
        gunluk_gamma = nlp_motoru.gunluk_gamma_hesapla(gunun_haberleri)
        print(f"-> Kriz Durumu Gamma Katsayısı: {gunluk_gamma}")

except Exception as hata:
    print(f"Sistem Hatası: {hata}")