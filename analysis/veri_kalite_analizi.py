# -*- coding: utf-8 -*-
import pandas as pd

print("="*80)
print("📊 VERİ KALİTE ANALİZİ")
print("="*80)

# Veri yükle
gps = pd.read_csv('all_merged_data.csv')
fleet = pd.read_csv('fleet.csv')
container_counts = pd.read_csv('container_counts.csv', sep=';', encoding='utf-8')

gps = gps.merge(fleet[['vehicle_id', 'vehicle_type']], on='vehicle_id')

anlamli_tarihler = ['19.12.2025', '20.12.2025', '21.12.2025', '22.12.2025', 
                     '23.12.2025', '24.12.2025', '25.12.2025']
gps_anlamli = gps[gps['Tarih'].isin(anlamli_tarihler)]

print(f"\n1️⃣ VERİ KAPSAMI:")
print(f"   Toplam GPS kaydı: {len(gps_anlamli):,}")
print(f"   Durağan nokta (<5km/h): {len(gps_anlamli[gps_anlamli['Hız(km/sa)'] < 5]):,}")
print(f"   Oranı: {len(gps_anlamli[gps_anlamli['Hız(km/sa)'] < 5])/len(gps_anlamli)*100:.1f}%")

print(f"\n2️⃣ ARAÇ ÇALIŞMA ANALİZİ:")
arac_gun = gps_anlamli.groupby(['vehicle_id', 'Tarih']).size().reset_index(name='kayit')
print(f"   Toplam araç-gün kombinasyonu: {len(arac_gun)}")
print(f"   Beklenen (45 araç × 7 gün): 315")
print(f"   Eksik: {315 - len(arac_gun)} araç-gün")

print(f"\n3️⃣ GÜN BAŞINA KAYIT:")
gun_kayit = gps_anlamli['Tarih'].value_counts().sort_index()
for tarih, sayi in gun_kayit.items():
    print(f"   {tarih}: {sayi:,} kayıt")

print(f"\n4️⃣ ARAÇ TİPİ BAŞINA DURUŞ:")
duragan = gps_anlamli[gps_anlamli['Hız(km/sa)'] < 5]
tip_dagilim = duragan['vehicle_type'].value_counts()
for tip, sayi in tip_dagilim.items():
    print(f"   {tip}: {sayi:,} duruş")

print(f"\n5️⃣ KONTEYNER DAĞILIMI:")
yeraltı = pd.to_numeric(container_counts['YERALTI KONTEYNER'], errors='coerce').fillna(0).sum()
ltr_770 = pd.to_numeric(container_counts['770 LT KONTEYNER'], errors='coerce').fillna(0).sum()
ltr_400 = pd.to_numeric(container_counts['400 LT KONTEYNER'], errors='coerce').fillna(0).sum()
plastik = pd.to_numeric(container_counts['PLASTİK'], errors='coerce').fillna(0).sum()
toplam_gercek = pd.to_numeric(container_counts['TOPLAM'], errors='coerce').fillna(0).sum()

print(f"   Yeraltı: {int(yeraltı):,}")
print(f"   770L: {int(ltr_770):,}")
print(f"   400L: {int(ltr_400):,}")
print(f"   Plastik: {int(plastik):,}")
print(f"   TOPLAM: {int(toplam_gercek):,}")

print(f"\n6️⃣ NEDEN %37 EKSİK?")
print(f"   ❌ 7 gün KISA SÜRE - Tüm konteynerlere gidilmiyor")
print(f"   ❌ Bazı mahalleler seyrek ziyaret ediliyor")
print(f"   ❌ GPS kayıt eksiklikleri var")
print(f"   ❌ EPS=10m dar - Araç 11m uzaktan geçerse kaçırıyoruz")
print(f"   ❌ Hız filtresi - <5km/h'de kaydediliyor, bazıları geçilebilir")

print(f"\n💡 ÇÖZÜMLER:")
print(f"   ✅ EPS'i artır (15-20m)")
print(f"   ✅ Daha uzun veri periyodu (30 gün)")
print(f"   ✅ Mahalle bazlı doğrulama + AI tahmin")

print("="*80)
