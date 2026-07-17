import pandas as pd
import os

def tez_haber_raporu_olustur():
    print("--- NLP VERİ SETİ ZAMAN ÇİZELGESİ VE DUYGU ANALİZİ ---")
    
    # Dosya yolunu kendi arşiv klasörüne göre ayarla
    mevcut_dizin = os.getcwd()
    dosya_yolu = os.path.join(mevcut_dizin, 'archive', 'haber_veriseti.csv')
    
    if not os.path.exists(dosya_yolu):
        print(f"HATA: {dosya_yolu} bulunamadı. Lütfen dosya adını kontrol et.")
        return

    try:
        # Veriyi okutuyoruz. Kendi veri setindeki sütun isimlerine göre 'Tarih' ve 'Duygu' kısımlarını güncellemelisin.
        df = pd.read_csv(dosya_yolu)
        
        # Sütun adının 'Date' veya 'Tarih' olduğunu varsayarak zaman formatına çeviriyoruz
        zaman_sutunu = 'Date' if 'Date' in df.columns else 'Tarih'
        df[zaman_sutunu] = pd.to_datetime(df[zaman_sutunu], errors='coerce')
        
        # Tarih formatı bozuk olan satırları temizle
        df = df.dropna(subset=[zaman_sutunu])
        
        # 2007 - 2009 Yılları arasını filtrele
        hedef_yillar = df[(df[zaman_sutunu].dt.year >= 2007) & (df[zaman_sutunu].dt.year <= 2009)]
        toplam_haber = len(hedef_yillar)
        
        if toplam_haber == 0:
            print("Belirtilen tarih aralığında (2007-2009) haber bulunamadı.")
            return

        baslangic = hedef_yillar[zaman_sutunu].min().strftime('%d.%m.%Y')
        bitis = hedef_yillar[zaman_sutunu].max().strftime('%d.%m.%Y')

        print("=" * 60)
        print(f"Sistem Başlangıç Tarihi : {baslangic}")
        print(f"Sistem Bitiş Tarihi     : {bitis}")
        print(f"Toplam İşlenen Haber    : {toplam_haber}")
        print("=" * 60)
        
        # Yıllara göre haber sayılarının dağılımı
        yillik_dagilim = hedef_yillar[zaman_sutunu].dt.year.value_counts().sort_index()
        print("\nYıllara Göre Haber Dağılımı:")
        for yil, sayi in yillik_dagilim.items():
            print(f" -> {yil} Yılı: {sayi} adet haber")
            
        print("-" * 60)
        
        # Duygu durumuna (Olumlu, Olumsuz, Nötr) göre dağılım
        duygu_sutunu = 'Sentiment' if 'Sentiment' in df.columns else 'Duygu'
        
        if duygu_sutunu in df.columns:
            duygu_dagilimi = hedef_yillar[duygu_sutunu].value_counts()
            print("\n2007-2009 Dönemi Duygu (Sentiment) Dağılımı:")
            for duygu, sayi in duygu_dagilimi.items():
                yuzde = (sayi / toplam_haber) * 100
                print(f" -> {str(duygu).capitalize()}: {sayi} adet (%{yuzde:.1f})")
        else:
            print(f"\nUyarı: '{duygu_sutunu}' isimli bir sütun bulunamadı. Duygu dağılımı hesaplanamıyor.")
            print("Lütfen CSV dosyasındaki duygu sütununun adını kontrol edip koda ekle.")
            
        print("=" * 60)
        print("Rapor başarıyla oluşturuldu. Bu verileri tezin 'Bulgular' veya 'Veri Seti' bölümüne ekleyebilirsin.")
        
    except Exception as e:
        print(f"Kod çalışırken beklenmeyen bir hata oluştu: {e}")

if __name__ == "__main__":
    tez_haber_raporu_olustur()