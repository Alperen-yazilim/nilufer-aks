"""
Talep Tahmini Modülü
Mahalle bazlı günlük çöp miktarı tahmini
"""

import pandas as pd
from datetime import datetime

# Sabitler
GUNLUK_TOPLAM = 572  # ton (ortalama)
TOPLAM_KONTEYNER = 196420

# Mevsim faktörleri
MEVSIM_FAKTORLERI = {
    1: 0.94,   # Ocak
    2: 0.85,   # Şubat
    3: 0.94,   # Mart
    4: 0.87,   # Nisan
    5: 1.02,   # Mayıs
    6: 1.07,   # Haziran
    7: 1.08,   # Temmuz
    8: 1.11,   # Ağustos
    9: 1.05,   # Eylül
    10: 1.04,  # Ekim
    11: 0.99,  # Kasım
    12: 1.00   # Aralık
}

def talep_tahmin(mahalle_konteyner, ay=None):
    """
    Bir mahalle için günlük çöp tahmini hesapla
    
    Args:
        mahalle_konteyner: Mahalledeki konteyner sayısı
        ay: Ay numarası (1-12), None ise şu anki ay
    
    Returns:
        float: Tahmini ton miktarı
    """
    if ay is None:
        ay = datetime.now().month
    
    oran = mahalle_konteyner / TOPLAM_KONTEYNER
    temel_tahmin = oran * GUNLUK_TOPLAM
    mevsimsel_tahmin = temel_tahmin * MEVSIM_FAKTORLERI[ay]
    
    return round(mevsimsel_tahmin, 2)

def talep_tahmin_tum_mahalleler(csv_path='full_dataset/container_counts.csv', ay=None):
    """
    Tüm mahalleler için talep tahmini
    
    Args:
        csv_path: Konteyner sayıları CSV dosyası
        ay: Ay numarası
    
    Returns:
        list: Mahalle bazlı tahminler
    """
    try:
        df = pd.read_csv(csv_path, sep=';')
        df.columns = df.columns.str.strip()
        
        # TOPLAM sütununu temizle
        df['TOPLAM'] = df['TOPLAM'].astype(str).str.replace('.', '').str.replace(',', '')
        df['TOPLAM'] = pd.to_numeric(df['TOPLAM'], errors='coerce').fillna(0).astype(int)
        
        tahminler = []
        for _, row in df.iterrows():
            tahmin = talep_tahmin(row['TOPLAM'], ay)
            tahminler.append({
                'mahalle': row['MAHALLE'],
                'konteyner': row['TOPLAM'],
                'tahmin': tahmin
            })
        
        # Tahmine göre sırala (büyükten küçüğe)
        tahminler.sort(key=lambda x: x['tahmin'], reverse=True)
        
        return tahminler
    
    except Exception as e:
        print(f"Hata: {e}")
        return []

# Test
if __name__ == '__main__':
    print("Talep Tahmini Testi")
    print("=" * 40)
    
    # Tek mahalle testi
    balat_tahmin = talep_tahmin(9900, ay=12)
    print(f"Balat (9900 konteyner, Aralık): {balat_tahmin} ton")
    
    # Tüm mahalleler
    print("\nTüm Mahalleler (İlk 10):")
    print("-" * 40)
    tahminler = talep_tahmin_tum_mahalleler()
    for t in tahminler[:10]:
        print(f"{t['mahalle']:<20} {t['konteyner']:>6} konteyner → {t['tahmin']:>6.2f} ton")
