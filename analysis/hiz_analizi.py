# -*- coding: utf-8 -*-
"""
HIZ VERİSİ ANALİZİ - GPS Hız Hesaplama Kontrolü
"""
import pandas as pd
import numpy as np

print("="*80)
print("🚗 HIZ VERİSİ ANALİZİ")
print("="*80)

gps = pd.read_csv('all_merged_data.csv')
gps = gps.sort_values(['vehicle_id', 'Tarih', 'Saat']).reset_index(drop=True)

print("\n📊 HIZ DAĞILIMI:")
print(f"Toplam kayıt: {len(gps):,}")
print(f"\n0 km/h (TAM DURUŞ): {len(gps[gps['Hız(km/sa)'] == 0]):,} (%{len(gps[gps['Hız(km/sa)'] == 0])/len(gps)*100:.1f})")
print(f"0-5 km/h arasında: {len(gps[(gps['Hız(km/sa)'] > 0) & (gps['Hız(km/sa)'] <= 5)]):,}")
print(f"5-10 km/h: {len(gps[(gps['Hız(km/sa)'] > 5) & (gps['Hız(km/sa)'] <= 10)]):,}")

print(f"\n⚠️ PROBLEM: 0-5 km/h ARASI HIÇ YOK!")
print(f"GPS cihazı ya 0 km/h diyor, ya da 5+ km/h")

# Haversine formülü ile hız kontrolü
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # metre
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# Bir araç için kontrol
test_arac = gps[gps['vehicle_id'] == 2824].head(50)
print(f"\n🧪 TEST: Araç 2824 - İlk 50 kayıt")
print(f"GPS'in verdiği hız:")

for i in range(min(10, len(test_arac)-1)):
    row1 = test_arac.iloc[i]
    row2 = test_arac.iloc[i+1]
    
    # Mesafe hesapla
    if pd.notna(row1['Enlem']) and pd.notna(row2['Enlem']):
        mesafe = haversine_distance(row1['Enlem'], row1['Boylam'], 
                                      row2['Enlem'], row2['Boylam'])
        
        # Zaman farkı (saniye)
        try:
            t1 = pd.to_datetime(f"{row1['Tarih']} {row1['Saat']}", format='%d.%m.%Y %H:%M:%S')
            t2 = pd.to_datetime(f"{row2['Tarih']} {row2['Saat']}", format='%d.%m.%Y %H:%M:%S')
            zaman_fark = (t2 - t1).total_seconds()
            
            if zaman_fark > 0:
                hesaplanan_hiz = (mesafe / zaman_fark) * 3.6  # km/h
                gps_hiz = row1['Hız(km/sa)']
                
                print(f"   {i+1}. GPS: {gps_hiz:.1f} km/h | Hesaplanan: {hesaplanan_hiz:.1f} km/h | Fark: {abs(gps_hiz - hesaplanan_hiz):.1f}")
        except:
            pass

print(f"\n❓ SONUÇ:")
print(f"   GPS cihazı 0-5 km/h arasını KAYDETMĠYOR!")
print(f"   Muhtemelen 5 km/h altını otomatik 0 yapıyor.")
print(f"\n💡 ÇÖZÜM:")
print(f"   ✅ <5 km/h yerine ==0 km/h kullanalım (tam duruş)")
print(f"   ✅ VEYA koordinat değişimini kontrol edelim")
print(f"   ✅ 5-10 km/h'yi de ekleyelim (yavaş ilerlerken boşaltma)")

# Gerçek duruş analizi
print(f"\n🔍 GERÇEK DURUŞ ANALİZİ:")
tam_duruş = gps[gps['Hız(km/sa)'] == 0].copy()
print(f"Tam duruş kayıtları: {len(tam_duruş):,}")

# Aynı koordinatta kaç kayıt var?
tam_duruş['koord'] = tam_duruş['Enlem'].astype(str) + '_' + tam_duruş['Boylam'].astype(str)
ayni_koord = tam_duruş.groupby('koord').size()
print(f"Farklı duruş noktası: {len(ayni_koord):,}")
print(f"Ortalama duruş süresi (kayıt sayısı): {ayni_koord.mean():.1f}")

print("="*80)
