"""
Vehicle/Fleet API Endpoints
Araç ve filo yönetimi API'leri
"""
from flask import jsonify
import pandas as pd
from . import vehicles_bp


@vehicles_bp.route('/vehicles')
def api_vehicles():
    """Araç listesi ve durumları - GERÇEK VERİ"""
    
    try:
        # Gerçek filo verisini oku
        df = pd.read_csv('full_dataset/fleet.csv')
        
        vehicles = []
        ozet = {'vincli': 0, 'buyuk': 0, 'kucuk': 0}
        
        for _, row in df.iterrows():
            # Tip çevirisi
            tip_mapping = {
                'Crane Vehicle': 'Vinçli',
                'Large Garbage Truck': 'Büyük',
                'Small Garbage Truck': 'Küçük'
            }
            tip = tip_mapping.get(row['vehicle_type'], row['vehicle_type'])
            
            # Kapasite (m³ cinsinden)
            kapasite = float(row['capacity_m3'])
            
            vehicle = {
                'id': int(row['vehicle_id']),
                'tip': tip,
                'kapasite': kapasite,
                'agirlik': float(row['capacity_ton']),
                'durum': 'aktif',  # Gerçek durumu GPS'ten alınacak
                'surucu': row['vehicle_name']
            }
            vehicles.append(vehicle)
            
            # Özet say
            if tip == 'Vinçli':
                ozet['vincli'] += 1
            elif tip == 'Büyük':
                ozet['buyuk'] += 1
            elif tip == 'Küçük':
                ozet['kucuk'] += 1
        
        # Özet formatı
        ozet_detay = {
            'vincli': {'toplam': ozet['vincli'], 'aktif': ozet['vincli']},
            'buyuk': {'toplam': ozet['buyuk'], 'aktif': ozet['buyuk']},
            'kucuk': {'toplam': ozet['kucuk'], 'aktif': ozet['kucuk']}
        }
        
        return jsonify({'vehicles': vehicles, 'ozet': ozet_detay})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@vehicles_bp.route('/fleet-summary')
def api_fleet_summary():
    """Filo özeti - GERÇEK VERİ"""
    try:
        df = pd.read_csv('full_dataset/fleet.csv')
        
        # Tip sayılarını hesapla
        vincli = len(df[df['vehicle_type'] == 'Crane Vehicle'])
        buyuk = len(df[df['vehicle_type'] == 'Large Garbage Truck'])
        kucuk = len(df[df['vehicle_type'] == 'Small Garbage Truck'])
        toplam = len(df)
        
        return jsonify({
            'vincli': {'toplam': vincli, 'aktif': vincli},
            'buyuk': {'toplam': buyuk, 'aktif': buyuk},
            'kucuk': {'toplam': kucuk, 'aktif': kucuk},
            'genel': {'toplam': toplam, 'aktif': toplam}
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
