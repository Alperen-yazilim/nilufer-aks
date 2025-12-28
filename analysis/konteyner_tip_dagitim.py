# -*- coding: utf-8 -*-
"""
KONTEYNER TIP DAGITIMI - ORAN BAZLI
Mahallelerdeki gerçek oranları kullanarak tip dağıtımı
"""
import pandas as pd
import numpy as np

print("="*80)
print("KONTEYNER TIP DAGITIMI")
print("="*80)

# Klasör oluştur
import os
os.makedirs('mah_kon', exist_ok=True)

# ============================================================================
# ADIM 1: VERİLERİ YÜKLE
# ============================================================================
print("\nVeriler yukleniyor...")

# Konteyner koordinatları + mahalle
konteyner = pd.read_csv('arac_rota/konteynerler/konteyner_mahalle.csv', encoding='utf-8')

# Mahalle bazlı gerçek dağılım
mahalle_data = pd.read_csv('master_mahalle_data.csv', encoding='utf-8')

print(f"Toplam konteyner: {len(konteyner):,}")
print(f"Mahalle sayisi: {len(mahalle_data)}")

# ============================================================================
# ADIM 2: MAHALLE İSİMLERİNİ NORMALİZE ET
# ============================================================================
def normalize_mahalle(text):
    """Mahalle ismini normalize et"""
    if not isinstance(text, str):
        return ""
    text = str(text).upper().strip()
    text = text.replace(' MAHALLESİ', '').replace(' MAHALLESI', '')
    text = text.replace(' MH.', '').replace(' MH', '')
    text = text.replace(' MAHALLE', '')
    import re
    text = re.sub(r'\s+', ' ', text).strip()
    return text

konteyner['mahalle_norm'] = konteyner['mahalle'].apply(normalize_mahalle)
mahalle_data['mahalle_norm'] = mahalle_data['mahalle'].apply(normalize_mahalle)

# ============================================================================
# ADIM 3: HER MAHALLE İÇİN TİP DAĞIT
# ============================================================================
print("\nTip dagitimi yapiliyor...")

# Tip atamak için boş liste
konteyner['tip'] = ''

for mahalle_norm in konteyner['mahalle_norm'].unique():
    # Bu mahalledeki konteynerler
    mahalle_mask = konteyner['mahalle_norm'] == mahalle_norm
    mahalle_konteynerleri = konteyner[mahalle_mask].copy()
    n_konteyner = len(mahalle_konteynerleri)
    
    # Master dosyadan oranları al
    mahalle_info = mahalle_data[mahalle_data['mahalle_norm'] == mahalle_norm]
    
    if len(mahalle_info) == 0:
        # Gerçek veri yok - hepsini "Bilinmiyor" yap
        konteyner.loc[mahalle_mask, 'tip'] = 'Bilinmiyor'
        continue
    
    # Oranları hesapla
    info = mahalle_info.iloc[0]
    n_yeralti = int(info['yeralti_konteyner'])
    n_770 = int(info['konteyner_770lt'])
    n_400 = int(info['konteyner_400lt'])
    n_plastik = int(info['plastik'])
    n_toplam = n_yeralti + n_770 + n_400 + n_plastik
    
    if n_toplam == 0:
        konteyner.loc[mahalle_mask, 'tip'] = 'Bilinmiyor'
        continue
    
    # Oranları bul
    oran_yeralti = n_yeralti / n_toplam
    oran_770 = n_770 / n_toplam
    oran_400 = n_400 / n_toplam
    oran_plastik = n_plastik / n_toplam
    
    # Kaç konteyner hangi tipe gitmeli
    hedef_yeralti = int(n_konteyner * oran_yeralti)
    hedef_770 = int(n_konteyner * oran_770)
    hedef_400 = int(n_konteyner * oran_400)
    hedef_plastik = n_konteyner - hedef_yeralti - hedef_770 - hedef_400  # Kalan
    
    # Tip listesi oluştur
    tipler = (['Yeraltı'] * hedef_yeralti + 
              ['770L'] * hedef_770 + 
              ['400L'] * hedef_400 + 
              ['Plastik'] * hedef_plastik)
    
    # Karıştır (rastgele dağıt)
    np.random.shuffle(tipler)
    
    # Ata
    indices = konteyner[mahalle_mask].index
    for i, idx in enumerate(indices):
        if i < len(tipler):
            konteyner.loc[idx, 'tip'] = tipler[i]

# ============================================================================
# ADIM 4: SONUÇLARI KAYDET
# ============================================================================
print("\nSonuclar kaydediliyor...")

# Detaylı konteyner dosyası
konteyner_final = konteyner[['konteyner_id', 'enlem', 'boylam', 'mahalle', 'tip', 'kaynak', 'tahmin_guveni']]
konteyner_final.to_csv('mah_kon/konteyner_tipli.csv', index=False, encoding='utf-8-sig')

# Mahalle bazlı özet
mahalle_ozet = konteyner.groupby(['mahalle', 'tip']).size().reset_index(name='adet')
mahalle_ozet_pivot = mahalle_ozet.pivot(index='mahalle', columns='tip', values='adet').fillna(0).astype(int)
mahalle_ozet_pivot['TOPLAM'] = mahalle_ozet_pivot.sum(axis=1)
mahalle_ozet_pivot.to_csv('mah_kon/mahalle_tip_detay.csv', encoding='utf-8-sig')

# Her mahalle için detaylı konteyner listesi
for mahalle_ismi in konteyner['mahalle'].unique():
    mahalle_konteynerleri = konteyner[konteyner['mahalle'] == mahalle_ismi][['konteyner_id', 'enlem', 'boylam', 'tip']]
    # Dosya adını güvenli yap
    safe_name = mahalle_ismi.replace(' ', '_').replace('/', '_').replace('\\', '_')[:50]
    mahalle_konteynerleri.to_csv(f'mah_kon/{safe_name}.csv', index=False, encoding='utf-8-sig')

# Genel istatistik
print("\n" + "="*80)
print("TIP DAGITIMI SONUC:")
print("="*80)
tip_dagilim = konteyner['tip'].value_counts()
for tip, sayi in tip_dagilim.items():
    print(f"{tip:<15} {sayi:>8} ({sayi/len(konteyner)*100:>5.1f}%)")
print("="*80)
print(f"{'TOPLAM':<15} {len(konteyner):>8}")
print("="*80)

print(f"\nDosyalar kaydedildi (mah_kon/ klasoru):")
print(f"  - konteyner_tipli.csv (Her konteynerin tipi)")
print(f"  - mahalle_tip_detay.csv (Mahalle bazli ozet)")
print(f"  - [Mahalle_Adi].csv ({len(konteyner['mahalle'].unique())} mahalle icin ayri dosyalar)")
