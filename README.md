# 🚛 NilüferAKS - Akıllı Atık Kontrol Sistemi

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=for-the-badge&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=for-the-badge&logo=sqlite)
![Leaflet](https://img.shields.io/badge/Leaflet.js-Maps-199900?style=for-the-badge&logo=leaflet)

**Bursa Nilüfer Belediyesi için geliştirilen Akıllı Çöp Toplama Rota Optimizasyonu ve Filo Yönetim Sistemi**

[Demo](#-demo) • [Kurulum](#-kurulum) • [Özellikler](#-özellikler) • [API](#-api-endpoints) • [Veri Seti](#-veri-seti)

</div>

---

## 🎯 Proje Özeti

NilüferAKS, **Vehicle Routing Problem (VRP)** çözümü ile çöp toplama operasyonlarını optimize eden, yapay zeka destekli bir filo yönetim sistemidir.

### Hedeflenen Kazanımlar

| Metrik | Değer | Açıklama |
|--------|-------|----------|
| 🚗 **Yakıt Tasarrufu** | %18 | Rota optimizasyonu ile mesafe azaltımı |
| 💰 **Yıllık Tasarruf** | ~966.000 TL | Yakıt ve operasyonel maliyet azaltımı |
| 🌍 **CO2 Azaltımı** | ~130 ton/yıl | Karbon ayak izi düşürme |
| ⏱️ **Zaman Tasarrufu** | ~2.7 saat/gün | Operasyonel verimlilik artışı |

---

## 📊 Gerçek Operasyonel Veriler

Bu proje, Nilüfer Belediyesi'nin **gerçek operasyonel verileri** üzerine inşa edilmiştir:

| Veri | Miktar | Kaynak |
|------|--------|--------|
| 🚛 **Araç Filosu** | 46 Araç | 3 tip: Vinçli, Büyük Kamyon, Küçük Kamyon |
| 🏘️ **Mahalle** | 64 Mahalle | Nilüfer ilçesi tam kapsam |
| 🗑️ **Konteyner** | 30.000+ | Yeraltı, 770L, 400L, Plastik |
| 📍 **GPS Kaydı** | 634.298 | Aralık 2025 verisi |
| 📅 **Tonaj Verisi** | 12 Ay | Aylık toplama istatistikleri |
| 👥 **Nüfus** | ~560.000 | Mahalle bazlı demografik veri |

---

## ✨ Özellikler

### 🎛️ Yönetici Paneli (Dashboard)
- Gerçek zamanlı KPI göstergeleri
- Filo durumu ve dağılımı
- Tasarruf metrikleri (yakıt, CO2, mesafe)
- Mahalle bazlı talep analizi
- Şoför yönetimi (CRUD işlemleri)

### 🗺️ Canlı Takip
- Leaflet.js ile interaktif harita
- Araç konum takibi (simülasyon)
- Mahalle bazlı konteyner görüntüleme
- Rota çizimi ve navigasyon

### 👨‍✈️ Şoför Portalı
- Günlük rota görüntüleme
- Durak listesi ve ilerleme takibi
- GPS verilerinden gerçek rota çizimi
- Navigasyon entegrasyonu

### 🔐 Rol Bazlı Erişim
- **Yönetici**: Tam yetki, şoför yönetimi, dashboard
- **Şoför**: Kendi rotası, araç bilgisi
- **Vatandaş**: Çöp toplama saati takibi (public)

### 🤖 AI/ML Modülleri
- **Talep Tahmini**: Mevsimsel faktörler ile mahalle bazlı günlük atık tahmini
- **Rota Optimizasyonu**: Nearest Neighbor + 2-opt algoritması ile VRP çözümü

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
│  Talep Tahmini (Mevsimsel)  │  VRP Solver (NN + 2-opt)     │
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

# 4. Uygulamayı başlat
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
| 🔴 **Admin** | `admin` | `admin123` | Dashboard, Şoför Yönetimi, Filo İzleme, Canlı Takip |
| 🟢 **Şoför** | *(admin oluşturur)* | `nilufer2025` | Rotam, Canlı Takip |
| 🔵 **Vatandaş** | *(kayıt ol)* | *(kendi belirler)* | Canlı Takip |

---

## 📁 Proje Yapısı

```
hackathon/
├── 📄 app.py                      # Ana Flask uygulaması (381 satır)
├── 📄 requirements.txt            # Python bağımlılıkları
│
├── 🤖 ai/                         # Yapay Zeka Modülleri
│   ├── talep_tahmin.py            # Mevsimsel talep tahmin modeli
│   └── rota_optimizer.py          # VRP çözümü (NN + 2-opt)
│
├── ⚙️ backend/
│   ├── api/                       # REST API Endpoints
│   │   ├── dashboard.py           # KPI ve istatistikler
│   │   ├── vehicles.py            # Araç filo API
│   │   ├── neighborhoods.py       # Mahalle ve konteyner API
│   │   └── routes_api.py          # Rota ve GPS verileri API
│   │
│   └── database/
│       ├── database.py            # SQLite CRUD işlemleri
│       ├── init_db.py             # Veritabanı başlatma
│       └── nilufer.db             # SQLite veritabanı
│
├── 🎨 templates/                  # Jinja2 HTML Şablonları
│   ├── base.html                  # Ana layout
│   ├── dashboard.html             # Yönetici paneli
│   ├── driver.html                # Şoför portalı
│   ├── tracking.html              # Canlı takip (public)
│   ├── filo_izleme.html           # Filo simülasyonu
│   ├── admin_drivers.html         # Şoför yönetimi
│   ├── login.html / register.html # Auth sayfaları
│   └── profile.html               # Kullanıcı profili
│
├── 📊 full_dataset/               # Gerçek Operasyonel Veriler
│   ├── fleet.csv                  # 46 araç bilgisi
│   ├── container_counts.csv       # 64 mahalle konteyner sayıları
│   ├── mahalle_nufus.csv          # Mahalle nüfus verileri
│   ├── tonnages.csv               # 12 aylık tonaj istatistikleri
│   ├── truck_types.csv            # Araç tipi kapasiteleri
│   ├── nilufer_sinir.json         # İlçe sınır GeoJSON
│   └── Nilufer_bin_collection_dataset/
│       └── all_merged_data.csv    # 634K GPS kaydı (113 MB)
│
├── 📍 araclarin_durdugu_noktalar/ # Araç Durağan Nokta Verileri
│   ├── arac_1520_duragan.csv      # Her araç için GPS durak noktaları
│   ├── arac_2824_duragan.csv      # Tarih, Saat, Enlem, Boylam, Hız
│   └── ... (45 araç)              # Araç tipi, Konteyner tipi
│
└── 🖼️ assets/                     # Medya dosyaları
    ├── images/
    └── video/
```

---

## 🌐 API Endpoints

### Dashboard & KPI
| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/dashboard` | Gerçek veriden hesaplanan KPI'lar |
| GET | `/api/tahmin` | Mahalle bazlı talep tahminleri |
| POST | `/api/optimize` | Rota optimizasyonu tetikle |

### Araç & Filo
| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/vehicles` | Tüm araç listesi |
| GET | `/api/fleet-summary` | Filo özet istatistikleri |
| GET | `/api/araclar` | GPS verisi olan araçlar |
| GET | `/api/arac/{id}/rota?tarih=DD.MM.YYYY` | Araç günlük rotası |
| GET | `/api/arac/{id}/tarihler` | Araç mevcut tarihleri |

### Mahalle & Konteyner
| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/neighborhoods` | Tüm mahalleler |
| GET | `/api/mahalleler` | Konteyner sayıları ile |

### Rota & Takip
| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/routes` | Optimize edilmiş rotalar |
| GET | `/api/route/{vehicle_id}` | Araç detaylı rota |
| GET | `/api/tracking` | Canlı takip verileri |

---

## 🤖 AI/ML Modülleri

### 1. Talep Tahmin Modeli (`ai/talep_tahmin.py`)

Mahalle bazlı günlük atık miktarı tahmini yapar.

```python
# Mevsim faktörleri
MEVSIM_FAKTORLERI = {
    1: 0.94,  # Ocak (düşük)
    7: 1.08,  # Temmuz (yüksek)
    8: 1.11,  # Ağustos (en yüksek)
    ...
}

# Tahmin formülü
tahmin = (mahalle_konteyner / toplam_konteyner) * günlük_ortalama * mevsim_faktörü
```

### 2. Rota Optimizasyonu (`ai/rota_optimizer.py`)

Vehicle Routing Problem (VRP) çözümü:

1. **Nearest Neighbor**: İlk çözüm oluşturma
2. **2-opt İyileştirme**: Lokal arama ile optimizasyon
3. **Haversine Mesafe**: Gerçek yol mesafesi hesabı (×1.4 faktör)

```
Algoritma Akışı:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Talepler  │───▶│   Nearest   │───▶│    2-opt    │───▶ Optimum Rota
│  + Mesafe   │    │  Neighbor   │    │ İyileştirme │
└─────────────┘    └─────────────┘    └─────────────┘
```

---

## 📊 Veri Seti

### GPS Verisi Formatı (`araclarin_durdugu_noktalar/`)

```csv
Tarih,Saat,Enlem,Boylam,Hız(km/sa),vehicle_type,konteyner_tip
19.12.2025,06:37:21,40.223456,28.876543,15.0,Crane Vehicle,YERALTI
19.12.2025,06:38:06,40.224567,28.877654,0.0,Crane Vehicle,YERALTI
```

### Konteyner Dağılımı

| Tip | Toplam | Açıklama |
|-----|--------|----------|
| Yeraltı | ~5.000 | Vinçli araç gerektirir |
| 770L | ~8.000 | Standart büyük konteyner |
| 400L | ~12.000 | Dar sokak konteyneri |
| Plastik | ~5.000 | Geri dönüşüm |

---

## 📈 Dashboard Metrikleri

Dashboard'da gösterilen KPI'lar **gerçek verilerden** hesaplanır:

```python
# Yakıt tasarrufu hesabı
günlük_mesafe = 150 km × 46 araç = 6.900 km/gün
yıllık_mesafe = 6.900 × 300 iş günü = 2.070.000 km/yıl
tasarruf = %18 optimizasyon = 372.600 km/yıl
yakıt_tasarrufu = 372.600 × 0.35 lt/km = 130.410 lt/yıl
parasal_tasarruf = 130.410 × 40 TL = 5.216.400 TL/yıl

# CO2 hesabı
co2_azalma = 130.410 lt × 2.68 kg/lt = 349 ton/yıl
```

---

## 🖼️ Ekran Görüntüleri

### Şoför Portalı
- Sol panel: Araç bilgisi, günlük durak listesi, ilerleme
- Sağ panel: Leaflet haritası ile GPS rotası
- Durak listesi: Saat, tonaj, tamamlanma durumu

### Dashboard
- KPI kartları: Tasarruf, CO2, mesafe
- Filo dağılımı grafiği
- Mahalle bazlı talep tablosu

---

## 🔧 Geliştirme

### Veritabanı Sıfırlama
```bash
# Veritabanını yeniden oluştur
python -c "from backend.database.init_db import init_all; init_all()"
```

### Test Modu
```bash
# AI modüllerini test et
python ai/talep_tahmin.py
python ai/rota_optimizer.py
```

---

## 🏆 Hackathon

**Etkinlik:** Bursa Nilüfer Belediyesi Hackathon 2025  
**Proje:** NilüferAKS - Akıllı Atık Kontrol Sistemi  
**Takım:** NilüferAKS

---

## 📝 Lisans

Bu proje Bursa Nilüfer Belediyesi Hackathon 2025 kapsamında geliştirilmiştir.

---

<div align="center">

**🌱 Daha temiz bir Nilüfer için akıllı çözümler**

Made with ❤️ in Bursa

</div>

## 📄 Lisans

MIT License

---

**🌿 Daha yeşil bir Nilüfer için!**
