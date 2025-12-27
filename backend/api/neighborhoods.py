"""
Neighborhood API Endpoints
Mahalle ve konteyner yönetimi API'leri
"""
from flask import jsonify
import pandas as pd
from . import neighborhoods_bp


@neighborhoods_bp.route('/mahalleler')
def api_mahalleler():
    """Mahalle listesi - GERÇEK VERİ (65 mahalle)"""
    
    try:
        # 1. Konteyner sayıları
        df_containers = pd.read_csv('full_dataset/container_counts.csv', sep=';', encoding='utf-8')
        
        # 2. Toplama programları
        df_schedule = pd.read_csv('full_dataset/neighbor_days_rotations.csv', sep=';', encoding='utf-8')
        
        # Mahalle isimlerini normalize et
        df_containers['mahalle_clean'] = df_containers['MAHALLE'].str.strip().str.upper()
        df_schedule['mahalle_clean'] = df_schedule['MAHALLE ADI'].str.replace(' MAHALLESİ', '', regex=False).str.strip().str.upper()
        
        # Merge
        df_merged = pd.merge(
            df_containers,
            df_schedule,
            on='mahalle_clean',
            how='left'
        )
        
        def safe_int(val):
            if pd.isna(val) or val == '':
                return 0
            if isinstance(val, str):
                val = val.replace('.', '').replace(',', '')
            try:
                return int(float(val))
            except:
                return 0
        
        mahalleler = []
        for _, row in df_merged.iterrows():
            mahalle = {
                'mahalle': row['MAHALLE'],
                'toplam_konteyner': safe_int(row['TOPLAM']),
                'yeralti': safe_int(row['YERALTI KONTEYNER']),
                'lt_770': safe_int(row['770 LT KONTEYNER']),
                'lt_400': safe_int(row['400 LT KONTEYNER']),
                'plastik': safe_int(row['PLASTİK']),
                'gunluk_toplama': safe_int(row['Days Collected Per Week']) if pd.notna(row.get('Days Collected Per Week')) else 3,
                'vinc_gerekli': bool(row.get('Is Crane Used')) if pd.notna(row.get('Is Crane Used')) and row.get('Is Crane Used') != 'FALSE' else False
            }
            mahalleler.append(mahalle)
        
        # Toplam konteyner
        total_containers = sum(m['toplam_konteyner'] for m in mahalleler)
        
        return jsonify({
            'mahalleler': mahalleler,
            'toplam': len(mahalleler),
            'toplam_konteyner': total_containers
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@neighborhoods_bp.route('/mahalleler/liste')
def api_mahalleler_liste():
    """Dropdown için mahalle listesi"""
    
    try:
        df = pd.read_csv('full_dataset/container_counts.csv', sep=';', encoding='utf-8')
        
        mahalleler = []
        for _, row in df.iterrows():
            mahalle_ad = str(row['MAHALLE']).strip()
            mahalleler.append({
                'id': mahalle_ad.lower().replace(' ', '_').replace('ı', 'i').replace('ö', 'o').replace('ü', 'u').replace('ş', 's').replace('ç', 'c').replace('ğ', 'g').replace('.', ''),
                'ad': mahalle_ad
            })
        
        mahalleler.sort(key=lambda x: x['ad'])
        
        return jsonify({
            'mahalleler': mahalleler,
            'toplam': len(mahalleler)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@neighborhoods_bp.route('/nilufer/sinir')
def api_nilufer_sinir():
    """Nilüfer ilçe sınırı polygon verisi"""
    
    try:
        import json
        
        with open('full_dataset/nilufer_sinir.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return jsonify(data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
