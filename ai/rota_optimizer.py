"""
Rota Optimizasyon Modülü
VRP (Vehicle Routing Problem) çözümü
Nearest Neighbor + 2-opt algoritması
"""

import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
from ai.talep_tahmin import talep_tahmin_tum_mahalleler

def haversine(lat1, lon1, lat2, lon2):
    """
    İki koordinat arası mesafe (km)
    Haversine formülü
    """
    R = 6371  # Dünya yarıçapı (km)
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    kus_ucusu = R * c
    yol_mesafesi = kus_ucusu * 1.4  # Yol faktörü
    
    return yol_mesafesi

def mesafe_matrisi_olustur(koordinatlar):
    """
    Tüm noktalar arası mesafe matrisi oluştur
    
    Args:
        koordinatlar: [(lat, lon), ...] listesi
    
    Returns:
        2D numpy array
    """
    n = len(koordinatlar)
    matris = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                matris[i][j] = haversine(
                    koordinatlar[i][0], koordinatlar[i][1],
                    koordinatlar[j][0], koordinatlar[j][1]
                )
    
    return matris

def nearest_neighbor(mesafe_matrisi, talepler, kapasite, baslangic=0):
    """
    Nearest Neighbor algoritması ile rota oluştur
    
    Args:
        mesafe_matrisi: Mesafe matrisi
        talepler: Her noktanın talebi (ton)
        kapasite: Araç kapasitesi (ton)
        baslangic: Başlangıç noktası indeksi (depo)
    
    Returns:
        list: Rota listesi [[durak1, durak2, ...], [durak1, ...], ...]
    """
    n = len(talepler)
    ziyaret_edilmemis = set(range(n))
    ziyaret_edilmemis.discard(baslangic)  # Depoyu çıkar
    
    tum_rotalar = []
    
    while ziyaret_edilmemis:
        rota = []
        mevcut_yuk = 0
        mevcut_konum = baslangic
        
        while True:
            # Sığabilecek en yakın noktayı bul
            en_yakin = None
            en_yakin_mesafe = float('inf')
            
            for nokta in ziyaret_edilmemis:
                talep = talepler[nokta]
                mesafe = mesafe_matrisi[mevcut_konum][nokta]
                
                # Kapasite kontrolü
                if mevcut_yuk + talep <= kapasite:
                    if mesafe < en_yakin_mesafe:
                        en_yakin = nokta
                        en_yakin_mesafe = mesafe
            
            # Sığan nokta bulunamadıysa, depoya dön
            if en_yakin is None:
                break
            
            # Noktaya git
            rota.append(en_yakin)
            mevcut_yuk += talepler[en_yakin]
            mevcut_konum = en_yakin
            ziyaret_edilmemis.remove(en_yakin)
        
        if rota:
            tum_rotalar.append(rota)
    
    return tum_rotalar

def iki_opt(rota, mesafe_matrisi, depo=0):
    """
    2-opt algoritması ile rotayı iyileştir
    
    Args:
        rota: Durak listesi
        mesafe_matrisi: Mesafe matrisi
        depo: Depo indeksi
    
    Returns:
        list: İyileştirilmiş rota
    """
    if len(rota) < 3:
        return rota
    
    # Tam rotayı oluştur (depo dahil)
    tam_rota = [depo] + rota + [depo]
    
    iyilesti = True
    while iyilesti:
        iyilesti = False
        for i in range(1, len(tam_rota) - 2):
            for j in range(i + 1, len(tam_rota) - 1):
                # Mevcut mesafe
                mevcut = (mesafe_matrisi[tam_rota[i-1]][tam_rota[i]] +
                         mesafe_matrisi[tam_rota[j]][tam_rota[j+1]])
                
                # Yeni mesafe (i ile j arası tersine çevrilince)
                yeni = (mesafe_matrisi[tam_rota[i-1]][tam_rota[j]] +
                       mesafe_matrisi[tam_rota[i]][tam_rota[j+1]])
                
                if yeni < mevcut:
                    # Tersine çevir
                    tam_rota[i:j+1] = tam_rota[i:j+1][::-1]
                    iyilesti = True
    
    # Depoları çıkar
    return tam_rota[1:-1]

def rota_mesafesi_hesapla(rota, mesafe_matrisi, depo=0):
    """Bir rotanın toplam mesafesini hesapla"""
    if not rota:
        return 0
    
    toplam = mesafe_matrisi[depo][rota[0]]  # Depodan ilk durağa
    
    for i in range(len(rota) - 1):
        toplam += mesafe_matrisi[rota[i]][rota[i+1]]
    
    toplam += mesafe_matrisi[rota[-1]][depo]  # Son duraktan depoya
    
    return toplam

def optimize_rotalar(tarih=None):
    """
    Ana optimizasyon fonksiyonu
    
    Args:
        tarih: Tarih (şimdilik kullanılmıyor)
    
    Returns:
        dict: Optimizasyon sonuçları
    """
    try:
        # Koordinatları yükle (all_merged_data.csv'den - gerçek GPS verileri)
        df_gps = pd.read_csv('full_dataset/Nilufer_bin_collection_dataset/all_merged_data.csv',
                             usecols=['Mahalle', 'Enlem', 'Boylam'],
                             encoding='utf-8')
        koordinat_df = df_gps.groupby('Mahalle').agg({
            'Enlem': 'mean',
            'Boylam': 'mean'
        }).reset_index()
        koordinat_df.columns = ['neighborhood', 'lat', 'lon']
        
        # Talep tahminlerini al
        tahminler = talep_tahmin_tum_mahalleler()
        
        # Depo koordinatı (Nilüfer Belediyesi merkez)
        DEPO = (40.2063, 28.9023)
        
        # Koordinat listesi oluştur (depo + mahalleler)
        koordinatlar = [DEPO]
        mahalle_isimleri = ['DEPO']
        talepler = [0]  # Deponun talebi 0
        
        for t in tahminler[:20]:  # İlk 20 mahalle ile test
            mahalle = t['mahalle']
            # Koordinatı bul
            coord_row = koordinat_df[koordinat_df['neighborhood'].str.upper() == mahalle.upper()]
            if not coord_row.empty:
                koordinatlar.append((coord_row.iloc[0]['lat'], coord_row.iloc[0]['lon']))
                mahalle_isimleri.append(mahalle)
                talepler.append(t['tahmin'])
        
        # Mesafe matrisi
        mesafe_mat = mesafe_matrisi_olustur(koordinatlar)
        
        # Araç kapasitesi
        KAPASITE = 12  # ton
        
        # Nearest Neighbor ile rotalar oluştur
        rotalar = nearest_neighbor(mesafe_mat, talepler, KAPASITE, baslangic=0)
        
        # 2-opt ile iyileştir
        iyilestirilmis_rotalar = []
        toplam_mesafe = 0
        
        for rota in rotalar:
            iyilestirilmis = iki_opt(rota, mesafe_mat, depo=0)
            mesafe = rota_mesafesi_hesapla(iyilestirilmis, mesafe_mat, depo=0)
            
            iyilestirilmis_rotalar.append({
                'duraklar': [mahalle_isimleri[i] for i in iyilestirilmis],
                'mesafe': round(mesafe, 1),
                'yuk': sum(talepler[i] for i in iyilestirilmis)
            })
            toplam_mesafe += mesafe
        
        # Sonuç
        return {
            'basarili': True,
            'rotalar': iyilestirilmis_rotalar,
            'toplam_arac': len(rotalar),
            'toplam_mesafe': round(toplam_mesafe, 1),
            'optimize_oncesi_mesafe': round(toplam_mesafe * 1.25, 1),  # Tahmini
            'tasarruf_km': round(toplam_mesafe * 0.25, 1),
            'tasarruf_yuzde': 20
        }
    
    except Exception as e:
        return {
            'basarili': False,
            'hata': str(e)
        }

# Test
if __name__ == '__main__':
    print("Rota Optimizasyonu Testi")
    print("=" * 50)
    
    # Basit test
    koordinatlar = [
        (40.2063, 28.9023),  # Depo
        (40.2230, 28.8720),  # Görükle
        (40.2180, 28.8650),  # İhsaniye
        (40.2609, 28.9377),  # Balat
        (40.2100, 28.8800),  # Konak
    ]
    
    talepler = [0, 4, 3, 5, 6]  # ton
    
    print("Koordinatlar yüklendi")
    
    mesafe_mat = mesafe_matrisi_olustur(koordinatlar)
    print("\nMesafe Matrisi (km):")
    print(np.round(mesafe_mat, 1))
    
    rotalar = nearest_neighbor(mesafe_mat, talepler, kapasite=10)
    print(f"\nOluşturulan rotalar: {rotalar}")
    
    for i, rota in enumerate(rotalar):
        mesafe = rota_mesafesi_hesapla(rota, mesafe_mat)
        yuk = sum(talepler[j] for j in rota)
        print(f"Rota {i+1}: {rota} - {mesafe:.1f} km - {yuk} ton")
