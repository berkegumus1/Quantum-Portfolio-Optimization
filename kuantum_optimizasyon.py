import numpy as np
import dimod
import neal

class KuantumPortfoyCozucu:
    def __init__(self, beklenen_getiri, kovaryans):
        self.mu = np.array(beklenen_getiri)
        self.sigma = np.array(kovaryans)
        self.varlik_sayisi = self.mu.shape[0] 
        self.cozucu = neal.SimulatedAnnealingSampler()

    def qubo_modeli_kur_ve_coz(self, gamma, secilecek_hisse_sayisi=15):
        ceza_katsayisi = 10.0
        Q = {}

        for i in range(self.varlik_sayisi):
            getiri_etkisi = -1 * self.mu[i]
            ceza_etkisi = ceza_katsayisi * (1 - 2 * secilecek_hisse_sayisi)
            Q[(i, i)] = getiri_etkisi + ceza_etkisi

        for i in range(self.varlik_sayisi):
            for j in range(i + 1, self.varlik_sayisi):
                risk_etkisi = 2 * gamma * self.sigma[i, j]
                ikili_ceza = 2 * ceza_katsayisi
                Q[(i, j)] = risk_etkisi + ikili_ceza

        bqm = dimod.BinaryQuadraticModel.from_qubo(Q)
        sonuclar = self.cozucu.sample(bqm, num_reads=100)
        en_iyi_cozum = sonuclar.first.sample
        
        agirliklar = np.zeros(self.varlik_sayisi)
        secilen_indeksler = [i for i in range(self.varlik_sayisi) if en_iyi_cozum[i] == 1]
        
        if len(secilen_indeksler) > 0:
            esit_agirlik = 1.0 / len(secilen_indeksler)
            for idx in secilen_indeksler:
                agirliklar[idx] = esit_agirlik
                
        return agirliklar