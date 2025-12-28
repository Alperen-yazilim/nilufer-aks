# 🚛 NilüferAKS - Akıllı Atık Kontrol Sistemi

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=for-the-badge&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=for-the-badge&logo=sqlite)
![Leaflet](https://img.shields.io/badge/Leaflet.js-Maps-199900?style=for-the-badge&logo=leaflet)

**Bursa Nilüfer Belediyesi için geliştirilen Akıllı Çöp Toplama Rota Optimizasyonu ve Filo Yönetim Sistemi**

</div>

---

## 🎯 Proje Özeti

NilüferAKS, **Vehicle Routing Problem (VRP)** çözümü ile çöp toplama operasyonlarını optimize eden, yapay zeka destekli bir filo yönetim sistemidir.

### 🏆 AI Optimizasyon Sonuçları (5 Araçlık Gerçek Verilerle Test Edildi!)

> 📊 **Not:** Aşağıdaki sonuçlar **5 araçlık gerçek operasyonel verilerle** elde edilmiştir. Belediyenin toplam **45 araçlık** filosu için tasarruf **9 kat daha fazla** olacaktır.

| Metrik | Mevcut | AI Optimize | Tasarruf (5 Araç) |
|--------|--------|-------------|-------------------|
| 🚗 **Mesafe** | 378 km | 153 km | **%59.6** |
| ⛽ **Yakıt** | 113 L | 46 L | **68 L/gün** |
| 🌍 **CO2 Emisyonu** | 300 kg | 121 kg | **179 kg/gün** |
| 💰 **Günlük Maliyet** | ₺2,945 | ₺1,190 | **₺1,755/gün** |

### 📅 Yıllık Projeksiyon (45 Araç - Tam Filo)

| Metrik | 5 Araç (Test) | 45 Araç (Tam Filo) |
|--------|---------------|---------------------|
| 💰 **Yıllık Tasarruf** | ~₺526,500 | **~₺4,738,500** |
| 🌍 **CO2 Azaltımı** | ~53.7 ton/yıl | **~483 ton/yıl** |
| 🛣️ **Mesafe Azaltımı** | ~67,500 km/yıl | **~607,500 km/yıl** |

---

## 📊 Gerçek Operasyonel Veriler

Bu proje, Nilüfer Belediyesi'nin **gerçek operasyonel verileri** üzerine inşa edilmiştir:

| Veri | Miktar | Açıklama |
|------|--------|----------|
| 🚛 **Araç Filosu** | 45 Araç | 20 Vinçli, 21 Büyük Kamyon, 4 Küçük Kamyon |
| 🏘️ **Mahalle** | 64 Mahalle | Nilüfer ilçesi tam kapsam |
| 🗑️ **Konteyner** | 30.000+ | Yeraltı, 770L, 400L, Plastik |
| 📍 **GPS Kaydı** | 634.298 | Aralık 2025 verisi |
| 📅 **Tonaj Verisi** | 12 Ay | Aylık toplama istatistikleri (~411 ton/gün) |
| 👥 **Nüfus** | ~560.000 | Mahalle bazlı demografik veri |

---

## ✨ Özellikler

### 🎛️ Yönetici Paneli (Dashboard)
- Gerçek zamanlı KPI göstergeleri
- Filo durumu ve dağılımı
- AI optimizasyon sonuçları karşılaştırması
- Mahalle bazlı talep analizi

### 🗺️ Filo İzleme & Simülasyon
- Leaflet.js ile interaktif harita
- **3 Görünüm Modu:**
  - 🔴 **Mevcut**: Gerçek GPS rotalarının simülasyonu
  - 🟢 **AI Optimize**: AI tarafından optimize edilen rotaların simülasyonu
  - 🔵 **Karşılaştır**: Her iki rotanın statik karşılaştırması
- Smooth interpolasyon ile akıcı araç hareketi
- Araç bazlı renk kodlaması

### 🤖 AI Rota Optimizasyonu
- **Nearest Neighbor + 2-opt** algoritması
- Araç tipi kısıtlamaları (Vinçli sadece yeraltı konteyner)
- Kapasite yönetimi ve ara boşaltma
- Yenikent Çöp Tesisi'ne final boşaltma
- Gerçek zamanlı mesafe/yakıt/CO2 hesaplama

### 👨‍✈️ Şoför Portalı
- Günlük rota görüntüleme
- Durak listesi ve ilerleme takibi
- GPS verilerinden gerçek rota çizimi
- Performans puanlama sistemi

### 🎮 Gamification Sistemi
- Performans puanlama (0-100)
- Seviye sistemi (Altın/Gümüş/Bronz/Çaylak)
- Prim hesaplama (%5-15)
- Rozetler ve başarılar

---

## 🛠️ Teknoloji Stack

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                             │
├─────────────────────────────────────────────────────────────┤
│  Bootstrap 5  │  Leaflet.js  │  Chart.js  │  Jinja2        │
├─────────────────────────────────────────────────────────────┤
│                        BACKEND                              │
├─────────────────────────────────────────────────────────────┤
│  Flask 3.0  │  Flask-CORS  │  SQLite  │  Pandas  │  NumPy  │
├─────────────────────────────────────────────────────────────┤
│                      AI/ML ENGINE                           │
├─────────────────────────────────────────────────────────────┤
│  VRP Solver (NN + 2-opt)  │  Haversine Distance  │  XGBoost│
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Kurulum

### Gereksinimler
- Python 3.11+
- pip

### Adımlar

```bash
# 1. Repoyu klonla
git clone https://github.com/guldasahmet/hackathon.git
cd hackathon

# 2. Sanal ortam oluştur
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. İlk kurulumu yap (veritabanı + mock veriler)
python setup.py

# 5. Uygulamayı başlat
python app.py
```

### Erişim
```
🌐 http://localhost:5000
```

---

## 👥 Kullanıcı Hesapları

| Rol | Kullanıcı Adı | Şifre | Erişim Alanları |
|-----|---------------|-------|-----------------|
| 🔴 **Admin** | `admin` | `admin123` | Dashboard, Şoför Yönetimi, Filo İzleme |
| 🟢 **Şoför** | `mehmet.yilmaz` | `surucu123` | Rotam, Performans |
| 🔵 **Vatandaş** | *(kayıt ol)* | *(kendi belirler)* | Canlı Takip |

---

## 📁 Proje Yapısı

```
hackathon/
├── 📄 app.py                      # Ana Flask uygulaması
├── 📄 setup.py                    # Kurulum scripti
├── 📄 requirements.txt            # Python bağımlılıkları
│
├── 🤖 ai/                         # AI Rota Optimizasyonu
│   ├── route_optimizer.py         # Ana VRP çözücü
│   ├── csv_to_routes_api.py       # CSV → JSON dönüştürücü
│   └── gamification_helper.py     # Şoför performans hesaplama
│
├── ⚙️ backend/
│   ├── api/                       # REST API Endpoints
│   │   ├── dashboard.py           # KPI ve istatistikleri
│   │   ├── vehicles.py            # Araç filo API
│   │   └── routes_api.py          # Rota ve GPS verileri API
│   │
│   └── database/
│       ├── database.py            # SQLite CRUD işlemleri
│       └── nilufer.db             # SQLite veritabanı
│
├── 🎨 templates/                  # Jinja2 HTML Şablonları
│   ├── base.html                  # Ana layout (dark theme)
│   ├── dashboard.html             # Yönetici paneli
│   ├── filo_izleme.html           # Filo simülasyonu (AI karşılaştırma)
│   ├── driver.html                # Şoför portalı
│   └── ...
│
├── 📊 full_dataset/               # Gerçek Operasyonel Veriler
│   ├── fleet.csv                  # 45 araç bilgisi
│   ├── container_counts.csv       # 64 mahalle konteyner sayıları
│   ├── mahalle_nufus.csv          # Mahalle nüfus verileri
│   ├── tonnages.csv               # 12 aylık tonaj istatistikleri
│   ├── routes_api.json            # AI optimize rotalar
│   ├── vehicle_start_positions.json # Araç başlangıç GPS'leri
│   └── Nilufer_bin_collection_dataset/
│       └── all_merged_data.csv    # 634K GPS kaydı
│
├── 📍 vehicle_stops/               # Araç Durağan Nokta Verileri
│   └── arac_*_duragan.csv         # 45 araç GPS durak verileri
│
└── 🔬 analysis/                    # ML Modelleri & Analiz
    ├── konteyner_ml_v3.py         # Konteyner tespit modeli
    └── konteyner_tip_ml.py        # Konteyner tipi sınıflandırma
```

---

## 🌐 API Endpoints

### Dashboard & KPI
| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/dashboard` | Gerçek veriden hesaplanan KPI'lar |
| GET | `/api/tahmin` | Mahalle bazlı talep tahminleri |
| POST | `/api/optimize` | AI rota optimizasyonu tetikle |

### Araç & Filo
| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/vehicles` | Tüm araç listesi |
| GET | `/api/fleet-summary` | Filo özet istatistikleri |
| GET | `/api/arac/{id}/rota?tarih=DD.MM.YYYY` | Araç günlük rotası |
| GET | `/api/routes-optimized` | AI optimize rotalar (routes_api.json) |

---

## 🤖 AI Rota Optimizasyonu Detayları

### Algoritma
1. **Araç Tipi Eşleştirme**: Vinçli → Yeraltı, Büyük/Küçük → Diğer konteynerler
2. **Nearest Neighbor**: İlk çözüm oluşturma
3. **2-opt İyileştirme**: Lokal arama ile optimizasyon
4. **Kapasite Yönetimi**: Dolunca Yenikent Tesisi'ne boşaltma
5. **Final Boşaltma**: Rota sonunda kalan yükü boşaltma

### Hesaplama Formülleri
```python
# Yakıt tüketimi
yakıt = mesafe_km × 0.30 L/km

# CO2 emisyonu  
co2 = yakıt_litre × 2.65 kg/L

# Maliyet
maliyet = yakıt_litre × ₺26/L
```

---

## 📈 Performans Metrikleri

### Filo İzleme Karşılaştırma Modu
- **Mevcut Rota**: Soluk, düz çizgi (arka plan)
- **AI Rota**: Parlak, kesikli çizgi (ön plan)
- Her araç kendi rengini korur
- Statik görünüm ile net karşılaştırma

### Puan Sistemi (Şoförler)
| Kriter | Ağırlık |
|--------|---------|
| Rota Uyumu | %30 |
| Zamanında Tamamlama | %25 |
| Yakıt Verimliliği | %25 |
| Toplanan Tonaj | %20 |

---

## 🏆 Hackathon

**Etkinlik:** Bursa Nilüfer Belediyesi Hackathon 2025  
**Proje:** NilüferAKS - Akıllı Atık Kontrol Sistemi  
**Takım:** NilüferAKS

---

## 📄 Lisans

MIT License

---

<div align="center">

**🌱 Daha temiz bir Nilüfer için akıllı çözümler**

Made with ❤️ in Bursa

</div>
