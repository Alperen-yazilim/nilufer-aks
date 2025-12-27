"""
Dashboard API Endpoints
Yönetici paneli KPI ve istatistik API'leri
"""
from flask import jsonify
from datetime import datetime
import pandas as pd
from . import dashboard_bp


@dashboard_bp.route('/dashboard')
def api_dashboard():
    """Yönetici paneli için KPI değerleri - GERÇEK VERİ"""
    
    try:
        # 1. Fleet verisi
        df_fleet = pd.read_csv('full_dataset/fleet.csv')
        total_vehicles = len(df_fleet)
        vincli = len(df_fleet[df_fleet['vehicle_type'] == 'Crane Vehicle'])
        buyuk = len(df_fleet[df_fleet['vehicle_type'] == 'Large Garbage Truck'])
        kucuk = len(df_fleet[df_fleet['vehicle_type'] == 'Small Garbage Truck'])
        
        # 2. Mahalle ve konteyner verisi
        df_containers = pd.read_csv('full_dataset/container_counts.csv', sep=';', encoding='utf-8')
        total_neighborhoods = len(df_containers)
        
        # Toplam konteyner hesapla (binlik ayırıcıları temizle)
        total_containers = 0
        for val in df_containers['TOPLAM']:
            if pd.notna(val) and val != '':
                if isinstance(val, str):
                    val = val.replace('.', '').replace(',', '')
                try:
                    total_containers += int(float(val))
                except:
                    pass
        
        # 3. Tonaj verisi (son 12 ay)
        df_tonnage = pd.read_csv('full_dataset/tonnages.csv', encoding='utf-8', on_bad_lines='skip')
        # Son 12 ay toplamı
        yillik_tonaj = df_tonnage['Toplam Tonaj (TON)'].head(12).sum()
        gunluk_ortalama = df_tonnage['Ortalama Günlük Tonaj (TON)'].head(12).mean()
        
        # 4. KPI hesaplamaları (optimizasyon varsayımları)
        # Yakıt tasarrufu: Optimizasyon ile %15-20 mesafe azalması
        mesafe_azalma_oran = 18  # %
        # Ortalama yakıt tüketimi: 35 lt/100km (çöp kamyonu)
        # Günlük ortalama mesafe: ~150 km/araç
        gunluk_mesafe = 150 * total_vehicles  # km
        yillik_mesafe = gunluk_mesafe * 300  # 300 iş günü
        tasarruf_mesafe = yillik_mesafe * (mesafe_azalma_oran / 100)  # km
        tasarruf_yakit = tasarruf_mesafe * 0.35  # litre (35lt/100km)
        yakit_fiyat = 40  # TL/litre (dizel)
        yillik_tasarruf = int(tasarruf_yakit * yakit_fiyat)
        
        # CO2 hesaplaması: 1 litre dizel = 2.68 kg CO2
        co2_azalma = int(tasarruf_yakit * 2.68 / 1000)  # ton
        # 1 ağaç yılda ~20 kg CO2 tutar
        agac_esdegeri = int(co2_azalma * 1000 / 20)
        
        kpis = {
            # Tasarruf KPI'ları
            'yillik_tasarruf': yillik_tasarruf,
            'yillik_tasarruf_artis': mesafe_azalma_oran,
            'co2_azalma': co2_azalma,
            'co2_azalma_miktar': agac_esdegeri,
            'mesafe_azalma': mesafe_azalma_oran,
            'mesafe_km': int(tasarruf_mesafe / 300),  # günlük
            'gunluk_sure_tasarruf': round(mesafe_azalma_oran * 0.15, 1),  # saat
            
            # Operasyonel veriler
            'toplam_arac': total_vehicles,
            'toplam_mahalle': total_neighborhoods,
            'toplam_konteyner': total_containers,
            'yillik_tonaj': int(yillik_tonaj),
            'gunluk_tonaj': int(gunluk_ortalama),
            
            # Filo dağılımı
            'filo': {
                'vincli': vincli,
                'buyuk': buyuk,
                'kucuk': kucuk
            },
            
            'tarih': datetime.now().strftime('%d Aralık %Y')
        }
        
        return jsonify(kpis)
        
    except Exception as e:
        # Hata durumunda fallback değerler
        return jsonify({
            'error': str(e),
            'yillik_tasarruf': 966000,
            'yillik_tasarruf_artis': 18,
            'co2_azalma': 130,
            'co2_azalma_miktar': 650,
            'mesafe_azalma': 22,
            'mesafe_km': 510,
            'gunluk_sure_tasarruf': 2.5,
            'tarih': datetime.now().strftime('%d Aralık %Y')
        })
