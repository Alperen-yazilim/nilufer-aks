# -*- coding: utf-8 -*-
import pandas as pd

print("="*80)
print("📊 DOĞRULUK ANALİZİ - SONUÇ RAPORU")
print("="*80)

# Gerçek konteyner sayısı
mahalle = pd.read_csv('container_counts.csv', sep=';', encoding='utf-8')
toplam_gercek = pd.to_numeric(mahalle['TOPLAM'], errors='coerce').fillna(0).sum()

# Bulduklarımız
gps_bulunan = 22179
ml_bulunan = 30518
ml_tahmin = ml_bulunan - gps_bulunan

print(f"\n🎯 GERÇEK KONTEYNER SAYISI:")
print(f"   {int(toplam_gercek):,} konteyner (container_counts.csv)")

print(f"\n📍 GPS İLE BULUNAN:")
print(f"   {gps_bulunan:,} konteyner")
print(f"   Başarı oranı: {gps_bulunan/toplam_gercek*100:.1f}%")

print(f"\n🤖 ML İLE TAHMİN EDİLEN:")
print(f"   +{ml_tahmin:,} yeni konteyner")
print(f"   Toplam: {ml_bulunan:,} konteyner")
print(f"   Başarı oranı: {ml_bulunan/toplam_gercek*100:.1f}%")

print(f"\n⚖️ DURUM:")
if ml_bulunan > toplam_gercek:
    print(f"   ⚠️ FAZLA TAHMİN: +{ml_bulunan - int(toplam_gercek):,} konteyner")
    print(f"   Fazlalık oranı: %{(ml_bulunan/toplam_gercek - 1)*100:.1f}")
    print(f"\n   💡 Sebep:")
    print(f"      - ML bazı depo/park yerlerini konteyner sandı")
    print(f"      - Güven skoru çok düşük (>0.6)")
    print(f"      - Mahalle bazlı filtreleme yok")
else:
    print(f"   ✅ İYİ TAHMİN: Hedefe yakın!")
    print(f"   Eksik: -{int(toplam_gercek) - ml_bulunan:,} konteyner")

# Tip bazlı karşılaştırma
print(f"\n📦 TİP BAZLI GERÇEK SAYILAR:")
yeraltı = pd.to_numeric(mahalle['YERALTI KONTEYNER'], errors='coerce').fillna(0).sum()
ltr_770 = pd.to_numeric(mahalle['770 LT KONTEYNER'], errors='coerce').fillna(0).sum()
ltr_400 = pd.to_numeric(mahalle['400 LT KONTEYNER'], errors='coerce').fillna(0).sum()
plastik = pd.to_numeric(mahalle['PLASTİK'], errors='coerce').fillna(0).sum()

print(f"   Yeraltı: {int(yeraltı):,}")
print(f"   770L: {int(ltr_770):,}")
print(f"   400L: {int(ltr_400):,}")
print(f"   Plastik: {int(plastik):,}")
print(f"   TOPLAM: {int(toplam_gercek):,}")

print(f"\n💡 ÖNERİ:")
print(f"   1. Güven skorunu yükselt (>0.6 → >0.85)")
print(f"   2. Mahalle bazlı filtreleme ekle")
print(f"   3. Depo noktalarını temizle (>50 nokta)")

print("="*80)
