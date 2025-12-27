"""
Routes API Endpoints
Rota optimizasyonu ve takip API'leri
"""
from flask import jsonify
from datetime import datetime
from . import routes_bp


@routes_bp.route('/routes')
def api_routes():
    """Optimize edilmiş rotalar"""
    
    # Örnek rota verisi (gerçekte optimize_rotalar() fonksiyonundan gelir)
    rotalar = [
        {
            'vehicle_id': 2824,
            'vehicle_tip': 'Vinçli',
            'surucu': 'Mehmet Yılmaz',
            'duraklar': [
                {'sira': 1, 'mahalle': 'Görükle', 'talep': 24.5, 'durum': 'tamamlandi', 'saat': '08:15'},
                {'sira': 2, 'mahalle': 'İhsaniye', 'talep': 18.2, 'durum': 'tamamlandi', 'saat': '09:42'},
                {'sira': 3, 'mahalle': 'Dumlupınar', 'talep': 22.1, 'durum': 'devam', 'saat': None},
                {'sira': 4, 'mahalle': 'Konak', 'talep': 15.8, 'durum': 'bekliyor', 'saat': None},
                {'sira': 5, 'mahalle': 'Beşevler', 'talep': 12.4, 'durum': 'bekliyor', 'saat': None},
            ],
            'toplam_mesafe': 34,
            'toplam_yuk': 93.0,
            'ilerleme': 66
        },
        {
            'vehicle_id': 1409,
            'vehicle_tip': 'Büyük',
            'surucu': 'Ali Demir',
            'duraklar': [
                {'sira': 1, 'mahalle': 'Balat', 'talep': 28.8, 'durum': 'tamamlandi', 'saat': '07:30'},
                {'sira': 2, 'mahalle': 'Fethiye', 'talep': 28.5, 'durum': 'devam', 'saat': None},
                {'sira': 3, 'mahalle': 'Ataevler', 'talep': 26.7, 'durum': 'bekliyor', 'saat': None},
            ],
            'toplam_mesafe': 28,
            'toplam_yuk': 84.0,
            'ilerleme': 45
        }
    ]
    
    return jsonify(rotalar)


@routes_bp.route('/route/<int:vehicle_id>')
def api_vehicle_route(vehicle_id):
    """Belirli bir aracın rotası"""
    
    # Örnek - gerçekte veritabanından çekilir
    rota = {
        'vehicle_id': vehicle_id,
        'tarih': datetime.now().strftime('%d Aralık %Y'),
        'duraklar': [
            {'sira': 1, 'mahalle': 'Görükle', 'talep': 24.5, 'durum': 'tamamlandi', 'saat': '08:15', 'lat': 40.2230, 'lon': 28.8720},
            {'sira': 2, 'mahalle': 'İhsaniye', 'talep': 18.2, 'durum': 'tamamlandi', 'saat': '09:42', 'lat': 40.2180, 'lon': 28.8650},
            {'sira': 3, 'mahalle': 'Dumlupınar', 'talep': 22.1, 'durum': 'devam', 'saat': None, 'lat': 40.2250, 'lon': 28.8800},
            {'sira': 4, 'mahalle': 'Konak', 'talep': 15.8, 'durum': 'bekliyor', 'saat': None, 'lat': 40.2100, 'lon': 28.8800},
            {'sira': 5, 'mahalle': 'Beşevler', 'talep': 12.4, 'durum': 'bekliyor', 'saat': None, 'lat': 40.2050, 'lon': 28.8900},
        ],
        'ozet': {
            'toplam_mesafe': 34,
            'toplam_yuk': 93.0,
            'kapasite_kullanim': 78,
            'ilerleme': 66,
            'kalan_durak': 3,
            'tahmini_bitis': '14:30'
        }
    }
    
    return jsonify(rota)
