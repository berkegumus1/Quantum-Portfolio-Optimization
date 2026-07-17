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
