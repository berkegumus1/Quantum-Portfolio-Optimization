# Quantum-Portfolio-Optimization
Cryptography and NLP-supported quantum portfolio optimization (Mathematics Bachelor's Thesis).




## Kurulum ve Çalıştırma Notu
**Önemli:** Proje içerisindeki Python scriptlerinde (örneğin `nlp_motoru.py` vb.) dosya okuma yolları yerel bilgisayar dizinine (örn: `C:\Users\Berke\Desktop\Tez_Final\...`) göre ayarlanmıştır. 

Projeyi kendi bilgisayarınızda veya sunucunuzda çalıştırırken "Dosya Bulunamadı" hatası almamak için, lütfen kod içerisindeki `dosya_yolu` değişkenlerini projenin bulunduğu yeni dizine göre güncelleyiniz. İhtiyaç duyulan tüm veriler proje klasörlerinde mevcuttur.







## Gereksinimler (Requirements)
Projedeki simülasyonların, API sunucusunun ve optimizasyon algoritmalarının eksiksiz çalışabilmesi için aşağıdaki Python kütüphanelerinin sisteminizde yüklü olması gerekmektedir:

**Veri İşleme ve Görselleştirme:**
* `pandas`
* `numpy`
* `matplotlib`
* `seaborn`

**API ve Güvenlik:**
* `fastapi` (API sunucusu altyapısı)
* `pydantic` (Veri doğrulama modelleri)
* `passlib[argon2]` (Kullanıcı şifreleme/hashleme)
* `PyJWT` (Token tabanlı kimlik doğrulama - kod içinde `jwt` olarak çağrılır)

**Kuantum Optimizasyonu ve NLP:**
* `dimod` (D-Wave QUBO modelleme)
* `neal` (Simulated Annealing çözücüsü)
* `transformers` (FinBERT duygu analizi motoru)

*(Not: `sqlite3`, `hashlib`, `os`, `re` gibi kütüphaneler Python standart kütüphanesine dahil olduğundan harici kuruluma ihtiyaç duymaz.)*

Tüm dış bağımlılıkları tek seferde kurmak için terminalinizde aşağıdaki komutu çalıştırabilirsiniz:
```bash
pip install pandas numpy matplotlib seaborn fastapi pydantic "passlib[argon2]" PyJWT dimod neal transformers




# Web Sitesi Arayüzü

## Web sitesinin ara yüzü
API uç noktaları ve JWT tabanlı kimlik doğrulama yönetimini gösteren web arayüzü.
![Web Sitesinin Ara Yüzü](kuantum_api_arayuz.jpeg)

### Simülasyon Çıktısı (Örnek JSON)
Portföy optimizasyonu sonucunda API tarafından döndürülen örnek JSON çıktısı:
```json
{
  "islem_durumu": "Tünelleme tamamlandı. Kuantum motoru optimum portföyü kilitledi.",
  "yatirim_vadesi": "Uzun Vadeli Yatırım (2 Yıl)",
  "fon_dagilimi": {
    "JNJ": "166666.67 TL",
    "PG": "166666.67 TL",
    "WMT": "166666.67 TL",
    "MCD": "166666.67 TL",
    "KO": "166666.67 TL",
    "UNH": "166666.67 TL"
  },
  "ilk_yatirilan_tutar": "1000000.00 TL",
  "tunelleme_sonrasi_guncel_para": "2500000.00 TL",
  "net_kazanc": "1500000.00 TL"
}
