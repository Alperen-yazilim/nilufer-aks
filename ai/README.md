# 🤖 AI Rota Optimizasyonu Modülü

Nilüfer Belediyesi çöp toplama operasyonları için geliştirilmiş akıllı rota optimizasyon sistemi.

## 📁 Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `route_optimizer.py` | Ana VRP çözücü (45 araç, tüm filo) |
| `csv_to_routes_api.py` | CSV → JSON format dönüştürücü |
| `gamification_helper.py` | Şoför performans hesaplama |

---

## 🚀 Kullanım

### Rota Optimizasyonu Çalıştırma

```bash
cd ai
python route_optimizer.py
```

**Çıktı:** `full_dataset/routes_api.json`

### JSON Format Dönüşümü

```bash
python csv_to_routes_api.py
```

---

## 🎯 Algoritma

### 1. Araç Tipi Eşleştirme
| Araç Tipi | Konteyner Tipi | Kapasite |
|-----------|----------------|----------|
| **Crane (Vinçli)** | Sadece YERALTI | 10-13 ton |
| **Large (Büyük)** | 770L, 400L, Plastik | 7-9 ton |
| **Small (Küçük)** | 770L, 400L, Plastik | 4-5 ton |

### 2. Nearest Neighbor + 2-opt
1. En yakın konteyneri seç
2. Kapasite kontrolü yap
3. Dolunca Yenikent Tesisi'ne git
4. 2-opt ile rotayı optimize et
5. Final boşaltma ekle

### 3. Zaman Yönetimi
- Başlangıç: 06:00
- Her durak: ~30 saniye
- Boşaltma: ~15 dakika
- Bitiş hedefi: 14:00

---

## 📊 Sonuçlar (Son Çalıştırma)

| Metrik | Değer |
|--------|-------|
| Toplam Araç | 45 |
| Toplam Durak | 9,399 |
| Toplam Tonaj | 411.3 ton |
| Final Boşaltma Yapan | 38 araç |

### Araç Tipi Dağılımı
- 🏗️ Crane (Vinçli): 20 araç
- 🚛 Large (Büyük): 21 araç  
- 🚐 Small (Küçük): 4 araç

---

## ⚙️ Konfigürasyon

### Yenikent Çöp Tesisi
```python
YENIKENT_LOCATION = {
    'lat': 40.2725,
    'lon': 28.8134,
    'name': 'Yenikent Katı Atık Bertaraf Tesisi'
}
```

### Araç Başlangıç Pozisyonları
`full_dataset/vehicle_start_positions.json` dosyasından okunur.

---

## 🔧 Gereksinimler

```bash
pip install numpy pandas scipy
```

---

## 📄 Çıktı Formatı (routes_api.json)

```json
{
  "generated_at": "2025-12-28T...",
  "total_vehicles": 45,
  "total_stops": 9399,
  "total_tonnage": 411.3,
  "vehicles": [
    {
      "vehicle_id": "2824",
      "vehicle_type": "Large Garbage Truck",
      "total_stops": 156,
      "total_tonnage": 8.2,
      "route": [
        {
          "step": 1,
          "lat": 40.1905,
          "lon": 28.9307,
          "mahalle": "Alaaddinbey Mh.",
          "demand_ton": 0.05,
          "load_ton": 0.05,
          "arrival_time": "2025-12-19T06:00:30"
        }
      ]
    }
  ]
}
```
