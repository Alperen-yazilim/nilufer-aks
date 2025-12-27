# NilüferAKS - Akıllı Atık Kontrol Sistemi

AI destekli atık toplama optimizasyonu ve gamification sistemi

## 🚀 Hızlı Başlangıç

### 1. Gereksinimler
```bash
python 3.8+
```

### 2. Kurulum
```bash
# Repository'yi klonla
git clone https://github.com/guldasahmet/hackathon.git
cd hackathon

# Gereksinimleri yükle
pip install -r requirements.txt

# İlk kurulumu yap (veritabanı + mock veriler)
python setup.py
```

### 3. Çalıştırma
```bash
python app.py
```

Tarayıcıda: http://localhost:5000

## 👤 Varsayılan Kullanıcılar

### Yönetici
- **Kullanıcı:** admin
- **Şifre:** admin123

### Şoför
- **Kullanıcı:** mehmet.yilmaz
- **Şifre:** surucu123

### Vatandaş
- Kayıt ol sayfasından yeni hesap oluşturabilirsiniz

## 🎮 Özellikler

### 1. VRP Optimizasyonu
- AI destekli rota optimizasyonu
- Yakıt tasarrufu hesaplama
- Mahalle bazlı talep tahmini

### 2. Şoför Gamification Sistemi
- Performans puanlama (0-100)
- Seviye sistemi (Altın/Gümüş/Bronz/Çaylak)
- Prim hesaplama (%5-15)
- Rozetler ve başarılar
- Liderlik tablosu

### 3. Canlı Takip
- Gerçek zamanlı araç takibi
- Mahalle bazlı durum
- Simülasyon modu

## 📊 Puan Sistemi

| Kriter | Ağırlık |
|--------|---------|
| Rota Uyumu | %30 |
| Zamanında Tamamlama | %25 |
| Yakıt Verimliliği | %25 |
| Toplanan Tonaj | %20 |

## 🏆 Seviyeler

| Seviye | Puan | Prim |
|--------|------|------|
| 🥇 Altın | 95-100 | %15 |
| 🥈 Gümüş | 85-94 | %10 |
| 🥉 Bronz | 75-84 | %5 |
| 🚛 Çaylak | 0-74 | %0 |

## 📁 Proje Yapısı

```
hackathon/
├── app.py                      # Ana uygulama
├── setup.py                    # İlk kurulum scripti
├── requirements.txt            # Python bağımlılıkları
├── ai/                         # AI modülleri
│   ├── rota_optimizer.py      # VRP algoritması
│   ├── talep_tahmin.py        # Talep tahmini
│   └── gamification_helper.py # Puan hesaplama
├── backend/
│   ├── api/                   # API endpoint'leri
│   │   ├── gamification.py   # Gamification API
│   │   ├── routes_api.py     # Rota API
│   │   └── ...
│   └── database/              # Veritabanı
│       ├── database.py        # DB fonksiyonları
│       └── init_db.py         # Veri import
├── templates/                 # HTML şablonları
│   ├── driver_performance.html
│   ├── admin_gamification.html
│   └── ...
└── scripts/                   # Yardımcı scriptler
    ├── setup_gamification.py
    └── add_achievements.py
```

## 🔧 Sorun Giderme

### Veritabanı hatası
```bash
# Veritabanını sıfırla
rm backend/database/nilufer.db
python setup.py
```

### Modül bulunamadı
```bash
pip install -r requirements.txt
```

### Port zaten kullanımda
```python
# app.py son satırı düzenle
app.run(debug=True, port=5001)  # Farklı port
```

## 📞 İletişim

- GitHub: https://github.com/guldasahmet/hackathon
- Demo: http://localhost:5000

## 📄 Lisans

MIT License
