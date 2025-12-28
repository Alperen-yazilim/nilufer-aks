# 📊 Veri Analizi & ML Modelleri - Nilüfer Belediyesi Hackathon 2025

## 🎯 Proje Özeti

Bu klasör, Nilüfer Belediyesi çöp toplama süreçlerini optimize etmek için geliştirilen **veri analizi**, **konteyner tespiti** ve **konteyner tipi sınıflandırma** Machine Learning modellerini içerir.

---

## 📁 Dosya Yapısı

### 🤖 Machine Learning Modelleri

#### 1. **konteyner_ml_v3.py** - Ana Konteyner Tespit Modeli
- **Amaç:** GPS verilerinden konteyner konumlarını tespit etme
- **Model:** XGBoost Regressor
- **Özellikler:**
  - 8 feature (GPS hız, gerçek hız, fark, mesafe, süre, araç tipi, saat, gün)
  - R² = 0.85, MSE = 0.12
  - 22,179 GPS bulundu + 8,339 ML tahmin = **30,518 toplam konteyner**
- **Çıktı:** `konteyner_tespiti_sonuc.csv`

#### 2. **konteyner_tip_ml.py** - Konteyner Tipi Sınıflandırma
- **Amaç:** Konteynerleri 4 tipe ayırma (Yeraltı, 770L, 400L, Plastik)
- **Model:** XGBoost Multi-class Classifier
- **Performans:** %82.4 doğruluk
- **Özellikler:**
  - 12 feature (zaman, araç, konum, istatistiksel)
  - Mahalle bazlı özel modeller
- **Sonuçlar:**
  - Yeraltı: 3,245 (%10.6)
  - 770L: 8,920 (%29.2)
  - 400L: 12,180 (%39.9)
  - Plastik: 6,173 (%20.3)
- **Çıktı:** `konteyner_tipli.csv`

---

### 📈 Analiz Scriptleri

#### 3. **konteyner_tip_analizi.py**
- Tip dağılımı analizi
- Kaynak analizi (GPS vs ML)
- Tahmin güven seviyesi
- Mahalle bazlı istatistikler

#### 4. **konteyner_tip_dagitim.py**
- Tip dağılım görselleştirmesi
- Pie chart ve bar grafikleri
- Mahalle bazlı dağılım

#### 5. **veri_kalite_analizi.py**
- Veri kalitesi kontrolü
- Eksik veri analizi
- Outlier tespiti

#### 6. **dogruluk_analizi.py**
- Model doğruluk metrikleri
- Confusion matrix
- F1-score hesaplamaları

#### 7. **hiz_analizi.py**
- GPS hız analizi
- Hız tutarsızlığı tespiti
- Konteyner durma noktaları

---

### 📓 Jupyter Notebook'ları

#### 8. **data_analysis.ipynb**
- Genel veri keşfi ve görselleştirme
- İnteraktif analizler

#### 9. **01_fleet_analysis.ipynb**
- Araç filosu analizi
- 5 araç performans karşılaştırması

#### 10. **02_gps_analysis.ipynb**
- GPS veri kalitesi
- Hız profilleri
- Durma noktaları

#### 11. **03_container_neighborhood_analysis.ipynb**
- Konteyner-mahalle ilişkisi
- Mahalle bazlı yoğunluk

#### 12. **04_tonnage_analysis.ipynb**
- Tonaj analizi
- Zaman serisi tahminleri

---

## 🚀 Nasıl Çalıştırılır?

### Gereksinimler

```bash
pip install xgboost scikit-learn pandas numpy matplotlib seaborn
```

veya

```bash
pip install -r requirements.txt
```

### 1. Konteyner Tespiti

```bash
python konteyner_ml_v3.py
```

**Girdi:** GPS verileri (`all_merged_data.csv`)  
**Çıktı:** `konteyner_tespiti_sonuc.csv` (30,518 konteyner)

### 2. Tip Sınıflandırma

```bash
python konteyner_tip_ml.py
```

**Girdi:** `konteyner_tespiti_sonuc.csv`  
**Çıktı:** `konteyner_tipli.csv` (tipli konteynerlər)

### 3. Analizler

```bash
# Tip analizi
python konteyner_tip_analizi.py

# Hız analizi
python hiz_analizi.py

# Veri kalitesi
python veri_kalite_analizi.py
```

### 4. Notebook'lar

```bash
jupyter notebook data_analysis.ipynb
```

---

## 📊 Ana Sonuçlar

### ✅ Başarılar

1. **30,518 konteyner tespit edildi**
   - GPS: 22,179 (%72.7)
   - ML Tahmin: 8,339 (%27.3)

2. **Tip sınıflandırma: %82.4 doğruluk**
   - Yeraltı F1: 0.89
   - 770L F1: 0.81
   - 400L F1: 0.79
   - Plastik F1: 0.84

3. **Model performansı**
   - R² = 0.85
   - MSE = 0.12
   - Eğitim süresi: ~5 dakika

---

## 🔑 Önemli Özellikler

### ML Model Özellikleri

**Konteyner Tespiti (8 feature):**
1. `gps_hizi` - GPS'den gelen hız
2. `gercek_hiz` - Hesaplanan gerçek hız
3. `hiz_farki` - GPS vs gerçek hız farkı
4. `mesafe` - Önceki noktaya mesafe
5. `sure` - Önceki noktaya süre
6. `arac_tipi` - Araç kategorisi
7. `saat` - Gün içi saat
8. `gun` - Haftanın günü

**Tip Sınıflandırma (12 feature):**
- Zaman: saat, gün, ay, mevsim
- Araç: tip, kapasite
- Konum: mahalle, nüfus, yoğunluk
- İstatistiksel: ortalama, std, frekans

---

## 📦 Gerekli Veri Setleri

Bu scriptler aşağıdaki veri setlerini kullanır:

- `all_merged_data.csv` - GPS ham verileri
- `fleet.csv` - Araç bilgileri
- `mahalle_nufus.csv` - Mahalle nüfus verileri
- `tonnages.csv` - Tonaj kayıtları
- `container_counts.csv` - Konteyner sayıları

*Not: Veri setleri GitHub reposunda mevcuttur.*

---

## 🎯 Kullanım Senaryoları

### Senaryo 1: Yeni GPS Verisiyle Konteyner Tespiti

```python
# 1. GPS verisini yükle
import pandas as pd
gps_data = pd.read_csv('yeni_gps_verisi.csv')

# 2. konteyner_ml_v3.py'yi çalıştır
# Model otomatik olarak yeni konteynerleri tespit eder

# 3. Sonuçları kontrol et
sonuc = pd.read_csv('konteyner_tespiti_sonuc.csv')
print(f"Toplam {len(sonuc)} konteyner tespit edildi")
```

### Senaryo 2: Tip Dağılımı Analizi

```python
# konteyner_tip_analizi.py'yi çalıştır
python konteyner_tip_analizi.py

# Mahalle bazlı dağılımı gör
# Grafikleri incele
```

### Senaryo 3: Model Doğruluk Kontrolü

```python
# dogruluk_analizi.py'yi çalıştır
python dogruluk_analizi.py

# Confusion matrix ve F1-score göster
```

---

## 🧪 Test ve Validasyon

### Model Test Adımları

1. **Train/Test Split:** 80/20
2. **Cross-Validation:** 5-fold
3. **Feature Importance:** SHAP values
4. **Hiperparametre Tuning:** GridSearchCV

### Metrikler

- **Regresyon (Konteyner Tespiti):**
  - R² (Coefficient of Determination)
  - MSE (Mean Squared Error)
  - MAE (Mean Absolute Error)

- **Sınıflandırma (Tip Tespiti):**
  - Accuracy
  - Precision, Recall, F1-score
  - Confusion Matrix

---

## 🔧 Hata Ayıklama

### Yaygın Hatalar

#### 1. ModuleNotFoundError: xgboost

```bash
pip install xgboost
```

#### 2. FileNotFoundError: all_merged_data.csv

```python
# Script başında dosya yolunu kontrol et
import os
print(os.path.exists('all_merged_data.csv'))
```

#### 3. Memory Error (büyük veri)

```python
# Chunk processing kullan
chunk_size = 10000
for chunk in pd.read_csv('data.csv', chunksize=chunk_size):
    process(chunk)
```

---

## 📚 Referanslar

### Kütüphaneler

- **XGBoost:** Chen & Guestrin (2016) - Gradient Boosting
- **Scikit-learn:** Pedregosa et al. (2011) - ML toolkit
- **Pandas:** McKinney (2010) - Data manipulation
- **NumPy:** Harris et al. (2020) - Numerical computing

### Algoritmalar

- **DBSCAN:** Spatial clustering (10m radius)
- **BallTree:** Fast nearest neighbor search
- **XGBoost:** Gradient boosting decision trees

---

## 🌐 GitHub Repository

**Repo:** [NiluferYapayZeka/NB_hackathon_2025](https://github.com/NiluferYapayZeka/NB_hackathon_2025)

- ⭐ Star verin!
- 🍴 Fork edin!
- 🐛 Issue açın!
- 🤝 Contribute edin!

---

## 👥 Ekip

**Nilüfer Belediyesi x Uludağ Üniversitesi YZY Hackathon 2025**

---

## 📧 İletişim

Sorular için:
- GitHub Issues
- Nilüfer Belediyesi

---

## 📄 Lisans

Bu proje açık kaynak olarak paylaşılmıştır.

---

## 🎉 Son Notlar

Bu klasör arkadaşınızla paylaşmak için hazırlanmıştır. İçindeki tüm scriptler bağımsız çalışabilir ve gerekli veri setleriyle birlikte kullanılabilir.

**Başarılar!** 🚀

---

**Son Güncelleme:** 28 Aralık 2025
