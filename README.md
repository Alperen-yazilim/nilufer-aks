# 🚛 NilüferAKS - Akıllı Atık Kontrol Sistemi

Bursa Nilüfer Belediyesi için geliştirilen **Akıllı Çöp Toplama Rota Optimizasyonu** sistemi.

## 🎯 Proje Özeti

NilüferAKS, çöp toplama operasyonlarını optimize ederek:
- 🚗 **%18 yakıt tasarrufu**
- 🌍 **CO2 emisyonlarında azalma**
- ⏱️ **Operasyonel verimlilik artışı**

sağlamayı hedefleyen bir hackathon projesidir.

## 📊 Gerçek Veriler

- **45 Araç** (Büyük kamyon, Küçük kamyon, Vinçli araç)
- **65 Mahalle**
- **18,181+ Konteyner**
- **12 Aylık Tonaj Verisi**

## 🛠️ Teknolojiler

- **Backend:** Flask 3.0, Python 3.11+
- **Frontend:** Bootstrap 5, Leaflet.js (Harita), Chart.js
- **Database:** SQLite
- **AI/ML:** Pandas, NumPy (Talep tahmini, Rota optimizasyonu)

## 🚀 Kurulum

```bash
# Repoyu klonla
git clone https://github.com/guldasahmet/hackathon.git
cd hackathon

# Sanal ortam oluştur
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Bağımlılıkları yükle
pip install -r requirements.txt

# Uygulamayı başlat
python app.py
```

## 👥 Kullanıcı Rolleri

| Rol | Kullanıcı Adı | Şifre | Yetkiler |
|-----|---------------|-------|----------|
| Admin | admin | admin123 | Tam yetki, şoför yönetimi |
| Şoför | (admin oluşturur) | nilufer2025 | Rota görüntüleme |
| Vatandaş | (kayıt ol) | - | Çöp toplama saati takibi |

## 📁 Proje Yapısı

```
hackathon/
├── app.py                 # Ana Flask uygulaması
├── requirements.txt       # Python bağımlılıkları
├── ai/                    # AI/ML modülleri
│   ├── talep_tahmin.py    # Talep tahmin modeli
│   └── rota_optimizer.py  # Rota optimizasyonu
├── backend/
│   ├── api/               # REST API endpoints
│   │   ├── dashboard.py   # Dashboard KPI'ları
│   │   ├── vehicles.py    # Araç API
│   │   ├── neighborhoods.py # Mahalle API
│   │   └── routes_api.py  # Rota API
│   └── database/          # Veritabanı
│       ├── database.py    # DB fonksiyonları
│       └── init_db.py     # DB başlatma
├── templates/             # HTML şablonları
├── static/                # CSS, JS dosyaları
├── full_dataset/          # Gerçek operasyonel veriler
└── assets/                # Görseller, videolar
```

## 🌐 API Endpoints

| Endpoint | Açıklama |
|----------|----------|
| `/api/vehicles` | Filo bilgileri |
| `/api/neighborhoods` | Mahalle ve konteyner verileri |
| `/api/dashboard` | Dashboard KPI'ları |
| `/api/routes` | Optimize edilmiş rotalar |

## 📈 Dashboard Metrikleri

- Yıllık Tasarruf (TL)
- CO2 Azaltımı (ton)
- Mesafe Optimizasyonu (%)
- Günlük Tonaj
- Filo Dağılımı

## 🏆 Hackathon

**Etkinlik:** Bursa Nilüfer Belediyesi Hackathon 2025  
**Takım:** NilüferAKS

## 📄 Lisans

MIT License

---

**🌿 Daha yeşil bir Nilüfer için!**
