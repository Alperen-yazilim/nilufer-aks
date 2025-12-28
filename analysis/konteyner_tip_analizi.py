"""
KONTEYNER TİP DAĞILIMI VE DOĞRULUK ANALİZİ
"""
import pandas as pd
import numpy as np

print("="*70)
print("📊 KONTEYNER TİP DAĞILIMI VE DOĞRULUK ANALİZİ")
print("="*70)

# Veri yükle
df = pd.read_csv('mah_kon/konteyner_tipli.csv', encoding='utf-8')

print(f"\n✅ Toplam konteyner: {len(df):,}")

# ============================================================================
# 1. TİP DAĞILIMI
# ============================================================================
print("\n" + "="*70)
print("1️⃣ TİP DAĞILIMI")
print("="*70)

tip_dagilim = df['tip'].value_counts()
print("\nKonteyner Tipleri:")
for tip, sayi in tip_dagilim.items():
    oran = (sayi / len(df)) * 100
    print(f"  {tip:12s}: {sayi:6,} adet ({oran:5.1f}%)")

# ============================================================================
# 2. KAYNAK ANALİZİ (GPS vs ML)
# ============================================================================
print("\n" + "="*70)
print("2️⃣ KAYNAK ANALİZİ")
print("="*70)

kaynak_dagilim = df['kaynak'].value_counts()
print("\nKonteyner Kaynağı:")
for kaynak, sayi in kaynak_dagilim.items():
    oran = (sayi / len(df)) * 100
    print(f"  {kaynak:15s}: {sayi:6,} adet ({oran:5.1f}%)")

# ============================================================================
# 3. GÜVEN SEVİYESİ ANALİZİ
# ============================================================================
print("\n" + "="*70)
print("3️⃣ GÜVEN SEVİYESİ ANALİZİ")
print("="*70)

print("\nTahmin Güveni Dağılımı:")
print(f"  Ortalama güven: {df['tahmin_guveni'].mean():.3f}")
print(f"  Minimum güven: {df['tahmin_guveni'].min():.3f}")
print(f"  Maksimum güven: {df['tahmin_guveni'].max():.3f}")

# Güven aralıkları
print("\nGüven Aralıkları:")
yuksek_guven = len(df[df['tahmin_guveni'] >= 0.9])
orta_guven = len(df[(df['tahmin_guveni'] >= 0.7) & (df['tahmin_guveni'] < 0.9)])
dusuk_guven = len(df[df['tahmin_guveni'] < 0.7])

print(f"  Yüksek güven (≥0.9): {yuksek_guven:6,} ({yuksek_guven/len(df)*100:5.1f}%)")
print(f"  Orta güven (0.7-0.9): {orta_guven:6,} ({orta_guven/len(df)*100:5.1f}%)")
print(f"  Düşük güven (<0.7):  {dusuk_guven:6,} ({dusuk_guven/len(df)*100:5.1f}%)")

# ============================================================================
# 4. TİP BAŞINA DOĞRULUK (GPS_Bulundu olanlar kesin doğru)
# ============================================================================
print("\n" + "="*70)
print("4️⃣ TİP BAŞINA DOĞRULUK TAHMİNİ")
print("="*70)

print("\nGPS ile Doğrulanan Tipler (Kesin Doğru):")
gps_tipleri = df[df['kaynak'] == 'GPS_Bulundu']['tip'].value_counts()
for tip, sayi in gps_tipleri.items():
    oran = (sayi / len(df[df['kaynak'] == 'GPS_Bulundu'])) * 100
    print(f"  {tip:12s}: {sayi:6,} adet ({oran:5.1f}%) ✅ DOĞRULANDI")

# ML tahminleri
if 'ML_Tahmin' in df['kaynak'].values:
    print("\nML ile Tahmin Edilen Tipler:")
    ml_tipleri = df[df['kaynak'] == 'ML_Tahmin']['tip'].value_counts()
    for tip, sayi in ml_tipleri.items():
        oran = (sayi / len(df[df['kaynak'] == 'ML_Tahmin'])) * 100
        ortalama_guven = df[(df['kaynak'] == 'ML_Tahmin') & (df['tip'] == tip)]['tahmin_guveni'].mean()
        print(f"  {tip:12s}: {sayi:6,} adet ({oran:5.1f}%) - Ortalama güven: {ortalama_guven:.2f}")

# ============================================================================
# 5. MAHALLE BAŞINA İSTATİSTİK (Top 10)
# ============================================================================
print("\n" + "="*70)
print("5️⃣ EN FAZLA KONTEYNER OLAN 10 MAHALLE")
print("="*70)

mahalle_sayilari = df['mahalle'].value_counts().head(10)
for i, (mahalle, sayi) in enumerate(mahalle_sayilari.items(), 1):
    mahalle_tipleri = df[df['mahalle'] == mahalle]['tip'].value_counts()
    tip_str = ", ".join([f"{tip}:{count}" for tip, count in mahalle_tipleri.head(3).items()])
    print(f"  {i:2d}. {mahalle:25s}: {sayi:4,} konteyner ({tip_str})")

# ============================================================================
# 6. BİLİNMEYEN TİPLER
# ============================================================================
print("\n" + "="*70)
print("6️⃣ BİLİNMEYEN TİPLER ANALİZİ")
print("="*70)

bilinmeyen = df[df['tip'].isin(['Bilinmiyor', 'Unknown', ''])]
print(f"\nBilinmeyen tip sayısı: {len(bilinmeyen):,} ({len(bilinmeyen)/len(df)*100:.1f}%)")

if len(bilinmeyen) > 0:
    print("\nBilinmeyen tiplerin kaynağı:")
    bilinmeyen_kaynak = bilinmeyen['kaynak'].value_counts()
    for kaynak, sayi in bilinmeyen_kaynak.items():
        print(f"  {kaynak:15s}: {sayi:6,} adet")
    
    print("\nBilinmeyen tiplerin ortalama güveni:")
    print(f"  {bilinmeyen['tahmin_guveni'].mean():.3f}")

print("\n" + "="*70)
print("✅ ANALİZ TAMAMLANDI")
print("="*70)
