"""
Neighborhood API Endpoints
Mahalle ve konteyner yönetimi API'leri
"""
from flask import jsonify
import pandas as pd
from . import neighborhoods_bp


@neighborhoods_bp.route('/mahalleler')
def api_mahalleler():
    """Mahalle listesi - GERÇEK VERİ (64 mahalle)"""
    
    try:
        # 1. Konteyner sayıları
        df_containers = pd.read_csv('full_dataset/container_counts.csv', sep=';', encoding='utf-8')
        
        # 2. Toplama programları
        df_schedule = pd.read_csv('full_dataset/neighbor_days_rotations.csv', sep=';', encoding='utf-8')
        
        # 3. Koordinatlar - Şimdilik GPS yükleme yok (118MB dosya çok büyük)
        # TODO: GPS verilerinden mahalle merkezlerini hesapla ve cache'le
        df_coords = pd.DataFrame(columns=['mahalle_clean', 'lat', 'lon'])
        
        # Mahalle isimlerini normalize et (container_counts'tan)
        df_containers['mahalle_clean'] = df_containers['MAHALLE'].str.strip().str.upper()
        
        # Schedule'dan mahalle adlarını temizle (MAHALLESİ ekini çıkar)
        df_schedule['mahalle_clean'] = df_schedule['MAHALLE ADI'].str.replace(' MAHALLESİ', '', regex=False).str.strip().str.upper()
        
        # İlk merge: containers + schedule
        df_merged = pd.merge(
            df_containers,
            df_schedule,
            on='mahalle_clean',
            how='left'
        )
        
        # İkinci merge: + koordinatlar
        df_final = pd.merge(
            df_merged,
            df_coords[['mahalle_clean', 'lat', 'lon']],
            on='mahalle_clean',
            how='left'
        )
        
        # API response formatı
        mahalleler = []
        for _, row in df_final.iterrows():
            # Sayısal değerleri temizle (1.300 -> 1300)
            def safe_int(val):
                if pd.isna(val) or val == '':
                    return 0
                # String ise noktayı kaldır
                if isinstance(val, str):
                    val = val.replace('.', '').replace(',', '')
                try:
                    return int(float(val))
                except:
                    return 0
            
            mahalle = {
                'mahalle': row['MAHALLE'],
                'toplam_konteyner': safe_int(row['TOPLAM']),
                'yeralti': safe_int(row['YERALTI KONTEYNER']),
                'lt_770': safe_int(row['770 LT KONTEYNER']),
                'lt_400': safe_int(row['400 LT KONTEYNER']),
                'plastik': safe_int(row['PLASTİK']),
                'gunluk_toplama': safe_int(row['Days Collected Per Week']) if pd.notna(row['Days Collected Per Week']) else 3,
                'vinc_gerekli': bool(row['Is Crane Used']) if pd.notna(row['Is Crane Used']) and row['Is Crane Used'] != 'FALSE' else False,
                'toplama_gunleri': str(row['Collection Frequency (Truck Type)']) if pd.notna(row['Collection Frequency (Truck Type)']) else 'Monday, Wednesday, Friday',
                'lat': float(row['lat']) if pd.notna(row['lat']) else 40.2230,
                'lon': float(row['lon']) if pd.notna(row['lon']) else 28.8720
            }
            mahalleler.append(mahalle)
        
        # Toplam konteyner hesapla (binlik ayırıcıları temizleyerek)
        total_containers = 0
        for val in df_containers['TOPLAM']:
            if pd.notna(val) and val != '':
                if isinstance(val, str):
                    val = val.replace('.', '').replace(',', '')
                try:
                    total_containers += int(float(val))
                except:
                    pass
        
        return jsonify({
            'mahalleler': mahalleler,
            'toplam': len(mahalleler),
            'toplam_konteyner': total_containers
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
