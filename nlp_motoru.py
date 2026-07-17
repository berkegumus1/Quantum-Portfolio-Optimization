from transformers import pipeline
import numpy as np

class DinamikRiskMotoru:
    def __init__(self):
        print("NLP Motoru (FinBERT) belleğe yükleniyor. Lütfen bekleyin...")
        self.analizor = pipeline("sentiment-analysis", model="ProsusAI/finbert")
        self.temel_gamma = 0.5
        print("NLP Motoru başarıyla aktifleştirildi.")

    def gunluk_gamma_hesapla(self, haberler_listesi):
        if not haberler_listesi or len(haberler_listesi) == 0:
            return self.temel_gamma

        hesaplanan_gammalar = []
        for haber in haberler_listesi:
            kisa_haber = str(haber)[:500] 
            sonuc = self.analizor(kisa_haber)[0]
            
            duygu = sonuc['label']
            skor = sonuc['score']

            if duygu == 'negative':
                dinamik_gamma = self.temel_gamma * (1 + skor)
            elif duygu == 'positive':
                dinamik_gamma = self.temel_gamma * (1 - (skor / 2))
            else:
                dinamik_gamma = self.temel_gamma

            hesaplanan_gammalar.append(dinamik_gamma)

        gunluk_net_gamma = np.mean(hesaplanan_gammalar)
        return round(float(gunluk_net_gamma), 4)