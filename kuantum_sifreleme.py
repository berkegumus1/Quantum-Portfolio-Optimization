import hashlib

class KaotikKyberSifreleme:
    def __init__(self, kyber_shared_secret: bytes):
        """
        Makaledeki gibi Kyber tarafından üretilen anahtarı (Shared Secret) alıp,
        Lojistik Harita formülü için başlangıç değerlerine (x0 ve lambda) dönüştürüyoruz.
        """
        # 32 bytelık anahtarı sayısal bir bütüne çevir
        hash_hex = hashlib.sha256(kyber_shared_secret).hexdigest()
        sayisal_deger = int(hash_hex, 16)
        sayisal_str = str(sayisal_deger)

        # Makaledeki gibi x0 için ilk 15 rakamı, lambda için sonraki 15 rakamı alıyoruz 
        x0_str = sayisal_str[:15]
        lambda_str = sayisal_str[15:30]

        # x0 değeri 0 ile 1 arasında olmalıdır (Örn: 0.800370441514353) 
        self.x0 = float("0." + x0_str) if x0_str else 0.5
        
        # Kaosun oluşması için Lambda değerinin 3.57 ile 4 arasında olması gerekir (Makalede 3.99 kullanılmış)
        ham_lambda = float("3." + lambda_str) if lambda_str else 3.99
        self.lam = min(max(ham_lambda, 3.57), 3.999) 

    def _kaotik_anahtar_uret(self, uzunluk: int) -> list:
        anahtarlar = []
        x = self.x0
        for _ in range(uzunluk):
            # 1. Adım: x_1 = x_0 * lambda * (1 - x_0) formülü 
            x = x * self.lam * (1 - x)
            # 2. Adım: Key = (x * 10^15) mod 256 formülü 
            key_byte = int(x * (10**15)) % 256
            anahtarlar.append(key_byte)
        return anahtarlar

    def sifrele(self, metin: str) -> str:
        metin_bytes = metin.encode('utf-8')
        anahtarlar = self._kaotik_anahtar_uret(len(metin_bytes))
        
        # 3. Adım: Metnin baytları ile kaotik anahtarların XOR işlemi 
        sifreli_bytes = bytearray()
        for m_byte, k_byte in zip(metin_bytes, anahtarlar):
            sifreli_bytes.append(m_byte ^ k_byte)
            
        # Veritabanına kolay yazılması için hex (onaltılık) formatına çeviriyoruz
        return sifreli_bytes.hex()

    def desifrele(self, sifreli_hex: str) -> str:
        sifreli_bytes = bytes.fromhex(sifreli_hex)
        anahtarlar = self._kaotik_anahtar_uret(len(sifreli_bytes))
        
        # XOR işlemi simetrik olduğu için şifre çözerken de aynı işlemi uyguluyoruz 
        cozulmus_bytes = bytearray()
        for s_byte, k_byte in zip(sifreli_bytes, anahtarlar):
            cozulmus_bytes.append(s_byte ^ k_byte)
            
        return cozulmus_bytes.decode('utf-8')

# Nesnel Test Bloğu (Sadece bu dosya çalıştırıldığında çalışır)
if __name__ == "__main__":
    # Temsili bir Kyber1024 çıktısı
    kyber_anahtari = b"Kuantum_Sonrasi_Gizli_Anahtar_12345"
    motor = KaotikKyberSifreleme(kyber_anahtari)
    
    orijinal_bakiye = "150000 TL"
    sifrelenmis = motor.sifrele(orijinal_bakiye)
    cozulmus = motor.desifrele(sifrelenmis)
    
    print(f"Orijinal Veri : {orijinal_bakiye}")
    print(f"Şifreli Hali  : {sifrelenmis}")
    print(f"Çözülmüş Veri : {cozulmus}")