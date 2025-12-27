# 🎯 Bursa Nilüfer Belediyesi Atık Toplama Optimizasyonu Projesi - Kapsamlı Veri Analizi ve Proje Fırsatları

## 📋 GENEL PROJE BAĞLAMI

Bu proje, Bursa Nilüfer Belediyesi'nin atık toplama operasyonlarını optimize etmeyi hedefleyen bir hackathon projesidir. Elimizde gerçek operasyonel veriler var: araç filosu, GPS takip kayıtları, konteyner envanteri, mahalle bazlı demografik bilgiler ve atık tonaj istatistikleri.

**Temel Amaç:** Atık toplama operasyonlarını daha verimli, çevre dostu ve maliyet etkin hale getirmek için veri odaklı çözümler geliştirmek.

---

## 📊 MEVCUT VERİLERİN DETAYLI İNCELENMESİ

### 1. ARAÇ FİLOSU VERİLERİ

#### `fleet.csv` - 46 Araçlık Filo
**Kritik Bilgiler:**
- **3 farklı araç tipi:**
  - **Crane Vehicle (Vinçli Araç):** 23m³ kapasite, 10-13 ton taşıma kapasitesi - Yeraltı ve büyük konteynerler için
  - **Large Garbage Truck (Büyük Kamyon):** 16.5m³ kapasite, 7-9 ton taşıma kapasitesi - Ana arterler ve geniş caddeler
  - **Small Garbage Truck (Küçük Kamyon):** 9m³ kapasite, 4-5 ton taşıma kapasitesi - Dar sokaklar ve çıkmazlar

**Filo Dağılımı:**
- 23 adet Vinçli Araç (Crane Vehicle)
- 19 adet Büyük Kamyon (Large Garbage Truck)  
- 4 adet Küçük Kamyon (Small Garbage Truck)

**Önemli Noktalar:**
- Her araç için benzersiz `vehicle_id` (4 haneli numara) mevcut
- Kapasite bilgileri hem hacim (m³) hem de ağırlık (ton) olarak verilmiş
- Araç tipleri, mahalle gereksinimlerine göre seçilmeli (dar sokaklar vs. geniş caddeler)

**Kullanım Senaryoları:**
- Rota planlamasında kapasite kısıtlamaları
- Mahalle bazlı araç tipi ataması (özellikle vinç gereksinimi olan yerler)
- Filo büyüklüğü ve kullanım verimliliği analizi

---

### 2. GPS TAKİP VERİLERİ

#### `all_merged_data.csv` - 634,298 GPS Kaydı (113 MB)
**En Kritik ve Zengin Veri Seti**

**İçerik:**
- Aralık 2025 dönemi için 46 araç için detaylı GPS takip kayıtları
- Yaklaşık 10 saniyede bir GPS kaydı
- Her kayıt şunları içeriyor:
  - GPS koordinatları (Enlem/Boylam)
  - Araç durumu (Duran/Hareketli)
  - Hız bilgisi (km/sa)
  - Duraklama süreleri
  - Rölanti süreleri
  - Adres ve mahalle bilgisi
  - Zaman damgası (tarih, saat, gün)
  - Toplam mesafe sayacı

**Önemli Sütunlar:**
- `vehicle_id`: Araç kimliği (fleet.csv ile eşleştirilebilir)
- `Enlem` / `Boylam`: GPS koordinatları
- `Durum`: Araç durumu (Duran, Hareketli, Kontak Açıldı, Kontak Kapandı, çeşitli alarm tipleri)
- `Duraklama Süresi`: Toplam duraklama süresi (örn: "04:39:50")
- `Rölanti Süresi`: Motor rölanti süresi
- `Hız(km/sa)`: Anlık hız
- `Mesafe(km)`: Segment mesafe
- `Mesafe Sayacı(km)`: Toplam mesafe sayacı
- `Adres` / `Mahalle`: Coğrafi konum bilgisi
- `Tarih` / `Saat` / `Gun`: Zaman bilgisi

**Bu Veri ile Yapılabilecekler:**
1. **Gerçekleşen Rota Analizi:** Araçların hangi mahallelerde ne kadar süre geçirdiği
2. **Duraklama Noktası Tespiti:** Konteyner toplama noktalarının otomatik tespiti
3. **Verimlilik Analizi:** Duraklama süreleri, rölanti süreleri, hız profilleri
4. **Mahalle Bazlı Hizmet Süreleri:** Her mahallede harcanan süre
5. **Zaman Serisi Analizi:** Günlük/haftalık operasyon pattern'leri
6. **Yakıt Optimizasyonu:** Rölanti ve hız analizleri ile yakıt tüketimi tahmini
7. **Anomali Tespiti:** Normal operasyon dışı durumlar (uzun duraklamalar, hızlı harekeller)

**Teknik Notlar:**
- Dosya boyutu 113 MB - büyük veri işleme teknikleri gerekebilir
- Pandas ile chunking veya Dask kullanımı önerilir
- Coğrafi analizler için GeoPandas kullanılabilir
- Görselleştirme için Folium/Plotly ile harita üzerinde gösterim

---

### 3. KONTEYNER ENVANTERİ VERİLERİ

#### `container_counts.csv` - 64 Mahalle için Konteyner Dağılımı
**Kritik Bilgiler:**

**Konteyner Tipleri:**
1. **YERALTI KONTEYNER:** Vinçli araç gerektirir (büyük hacimli, yeraltı)
2. **770 LT KONTEYNER:** Büyük hacimli yerüstü konteyner
3. **400 LT KONTEYNER:** Standart yerüstü konteyner
4. **PLASTİK:** Küçük plastik çöp bidonları

**İstatistikler:**
- Toplam 30,000+ konteyner
- Mahalleler arası büyük fark: 23 konteyner (en az) - 2,590 konteyner (en fazla)
- **Özel Durum:** Gölyazı Mahallesi "YER ÇÖPÜ" sistemi kullanıyor (manuel toplama)

**En Yüksek Konteyner Yoğunluğuna Sahip Mahalleler:**
- Karaman: 2,414 konteyner
- Çamlıca: 2,107 konteyner
- Altınşehir: 1,711 konteyner
- Dumlupınar: 1,313 konteyner
- İhsaniye: 1,296 konteyner

**Bu Veri ile Yapılabilecekler:**
1. **Araç Tipi Ataması:** Yeraltı konteyner olan mahalleler mutlaka vinçli araç gerektirir
2. **Rota Yoğunluğu Planlaması:** Konteyner sayısına göre rota süresi tahmini
3. **Kapasite Planlaması:** Toplam konteyner kapasitesi vs araç kapasitesi
4. **Coğrafi Kümeleme:** Benzer konteyner profillerine sahip mahalleler
5. **Hizmet Önceliklendirme:** Yüksek konteyner yoğunluğu olan bölgeler

---

### 4. MAHALLE VE NÜFUS VERİLERİ

#### `mahalle_nufus.csv` - 65 Mahalle Demografik Bilgisi
**İçerik:**
- Mahalle bazlı nüfus verileri
- Toplam nüfus: ~560,000 kişi
- Nüfus aralığı: 92 (Üçpınar) - 32,489 (Görükle)

**En Kalabalık Mahalleler:**
1. Görükle: 32,489 kişi
2. İhsaniye: 28,846 kişi
3. Dumlupınar: 28,594 kişi
4. Konak: 24,807 kişi
5. Beşevler: 23,320 kişi

**Bu Veri ile Yapılabilecekler:**
1. **Atık Üretimi Tahmini:** Nüfus bazlı atık miktarı tahmini (kişi başı atık x nüfus)
2. **Hizmet Önceliklendirme:** Kalabalık mahalleler için daha sık toplama
3. **Yoğunluk Analizi:** Nüfus / konteyner sayısı oranı
4. **Kapasite Planlaması:** Nüfus artışına göre gelecek ihtiyaçları

---

### 5. TOPLAMA GÜNLERİ VE ROTASYON VERİLERİ

#### `neighbor_days_rotations.csv` - 69 Kayıt (Bazı Mahalleler Çoklu Tip)
**Kritik Operasyonel Bilgiler:**

**Toplama Frekansları:**
- **3 gün/hafta:** Çoğunluk mahalle (Pazartesi-Çarşamba-Cuma veya Salı-Perşembe-Cumartesi)
- **6 gün/hafta:** Yüksek yoğunluk mahalleleri (Pazartesi-Cumartesi)
- **7 gün/hafta:** Kritik mahalleler (Dumlupınar, Görükle - her gün toplama)

**Vinç Kullanımı:**
- 17 mahallede vinçli araç gerekli (Is Crane Used = TRUE)
- Vinç rotasyon günü: Genellikle 6 gün (haftanın her günü)

**Özel Durumlar:**
- **Gölyazı:** Gece toplama yapılıyor (Night)
- **Esentepe, Hasanağa:** Hem büyük hem küçük kamyon kullanıyor (çoklu tip)
- **Dumlupınar ve Görükle:** Günlük toplama (en yoğun hizmet)

**Araç Tipi Atamaları:**
- Çoğunlukla Large Garbage Truck kullanılıyor
- Dar sokakları olan mahallelerde Small Garbage Truck
- Yeraltı konteyneri olan mahalleler için Crane Vehicle

**Bu Veri ile Yapılabilecekler:**
1. **Rota Planlama Kısıtlamaları:** Hangi mahalleler hangi günler hizmet alıyor
2. **Araç-Mahalle Eşleştirmesi:** Araç tipi gereksinimlerine göre atama
3. **Vinçli Araç Optimizasyonu:** Vinç gerektiren mahallelerin rotalaması
4. **Hizmet Seviyesi Analizi:** Toplama frekansı vs nüfus/konteyner sayısı
5. **Operasyonel Verimlilik:** Mevcut planlama vs optimal planlama karşılaştırması

---

### 6. TONAJ İSTATİSTİKLERİ

#### `tonnages.csv` - 24 Aylık Atık Tonaj Verileri (Ocak 2024 - Kasım 2025)
**İçerik:**
- Aylık bazda toplanan atık tonajları
- Yerüstü ve Yeraltı konteynerleri ayrı ayrı
- Günlük ortalama tonaj hesaplamaları

**İstatistikler:**
- **Ortalama aylık tonaj:** ~17,000 ton
- **Günlük ortalama:** 550-690 ton/gün
- **En yüksek:** Ağustos 2025 (20,703 ton)
- **En düşük:** Şubat 2024 (14,698 ton)
- **Yeraltı konteyner oranı:** Yaklaşık %10

**Mevsimsel Trendler:**
- **Yaz ayları (Haziran-Ağustos):** Yüksek tonaj (17,000-20,700 ton)
- **Kış ayları (Aralık-Şubat):** Düşük tonaj (14,400-16,200 ton)
- Yaz aylarında yaklaşık %30-40 artış gözlemleniyor

**Bu Veri ile Yapılabilecekler:**
1. **Mevsimsel Talep Tahmini:** Yaz/kış farkını hesaba katarak planlama
2. **Trend Analizi:** Zaman serisi modelleri (ARIMA, Prophet) ile gelecek tahminleri
3. **Kapasite Planlaması:** Yüksek talep dönemlerinde ek kaynak ihtiyacı
4. **Bütçe Planlaması:** Tonaj bazlı maliyet hesaplamaları
5. **Performans Kıyaslama:** Aylık hedefler vs gerçekleşen

---

### 7. DİĞER VERİLER

#### `address_data.csv` - Adres Veritabanı (17 MB, ~150,000 kayıt)
- Nilüfer ilçesindeki sokak/cadde adları
- Mahalle bilgileri ve koordinatlar
- **Kullanım:** Konteyner yerleştirme planlaması, servis bölgesi tanımlama

#### `Yol-2025-12-16_13-38-47.json` - JSON Veri (9.1 MB)
- JSON formatında yapısal veri
- Muhtemelen yollara ait coğrafi veriler
- **Kullanım:** Rota planlama, yol ağı analizi

---

## 🎯 ÖNERİLEN PROJE FİKİRLERİ VE YAKLAŞIMLAR

### 1. AKıLLı ROTA OPTİMİZASYONU SİSTEMİ

**Hedef:** GPS verilerinden öğrenilen pattern'ler ve kısıtlamalar ile optimal rotalar oluşturmak

**Kullanılacak Veriler:**
- `all_merged_data.csv`: Mevcut rota analizi için
- `neighbor_days_rotations.csv`: Toplama günleri kısıtlamaları
- `container_counts.csv`: Konteyner lokasyonları
- `fleet.csv`: Araç kapasiteleri

**Yaklaşım:**
- Vehicle Routing Problem (VRP) modelleme
- Kapasite kısıtlamaları (CVRP)
- Zaman pencereleri (VRPTW)
- Çoklu depo (MDVRP) - araçlar farklı depolarda başlayabilir
- Metaheuristik algoritmalar: Genetic Algorithm, Simulated Annealing, Ant Colony
- Ya da OR-Tools ile optimal çözüm

**Çıktılar:**
- Mahalle bazlı optimized rotalar
- Tahmini süre ve mesafe azaltımı
- Yakıt tasarrufu hesaplamaları
- Görselleştirilmiş rota haritaları

---

### 2. TALEBİN TAHMİNLEME VE DİNAMİK PLANLAMA

**Hedef:** Atık miktarını tahmin ederek dinamik operasyonel planlama

**Kullanılacak Veriler:**
- `tonnages.csv`: Geçmiş tonaj verileri
- `mahalle_nufus.csv`: Nüfus bilgileri
- `all_merged_data.csv`: Sezonsal pattern'ler
- Dış veriler: Hava durumu, tatil günleri

**Yaklaşım:**
- Time Series Forecasting: ARIMA, SARIMA, Prophet
- Machine Learning: Random Forest, XGBoost, LSTM
- Mahalle bazlı talep tahmini (nüfus + konteyner sayısı)
- Sezonalite ve trend analizi

**Çıktılar:**
- Günlük/haftalık atık miktarı tahminleri
- Mahalle bazlı talep haritası
- Dinamik araç atama önerileri
- Yüksek talep günleri için uyarı sistemi

---

### 3. FİLO VE KAYNAK OPTİMİZASYONU

**Hedef:** Mevcut filo kullanımını analiz ederek kaynak optimizasyonu

**Kullanılacak Veriler:**
- `fleet.csv`: Araç kapasiteleri
- `all_merged_data.csv`: Araç kullanım verileri
- `neighbor_days_rotations.csv`: Mevcut araç atamaları
- `container_counts.csv`: Toplama noktaları

**Yaklaşım:**
- Araç kullanım oranı analizi (kapasite kullanım yüzdesi)
- Boş araç tespiti (underutilized vehicles)
- Araç tipi optimizasyonu (vinç vs normal kamyon)
- Operasyonel maliyet analizi

**Çıktılar:**
- Filo büyüklüğü önerileri (fazla/eksik araç tespiti)
- Araç tipi dönüşüm önerileri
- Maliyet azaltım potansiyeli
- ROI hesaplamaları

---

### 4. DURAKLAMA VE VERİMLİLİK ANALİZİ

**Hedef:** GPS verilerinden duraklama noktalarını analiz ederek verimliliği artırmak

**Kullanılacak Veriler:**
- `all_merged_data.csv`: Duraklama süreleri, rölanti süreleri
- `container_counts.csv`: Konteyner yoğunlukları

**Yaklaşım:**
- Clustering algoritmaları (DBSCAN, K-Means) ile duraklama noktası tespiti
- Anomali tespiti: Normalden uzun duraklamalar
- Rölanti süreleri analizi - yakıt israfı
- Toplama noktası başına süre analizi

**Çıktılar:**
- Otomatik tespit edilmiş konteyner lokasyonları
- Verimlilik metrikleri (dakika/konteyner)
- Yakıt tasarrufu önerileri
- İyileştirme potansiyeli raporu

---

### 5. COĞRAFYA BAZLI HIZ VE YAKıT OPTİMİZASYONU

**Hedef:** GPS verilerinden hız profillerini analiz ederek yakıt optimizasyonu

**Kullanılacak Veriler:**
- `all_merged_data.csv`: Hız, mesafe, rölanti verileri
- `address_data.csv`: Yol ağı bilgileri

**Yaklaşım:**
- Hız profili analizi (mahalle/yol tipi bazlı)
- Rölanti süreleri ve yakıt tüketimi korelasyonu
- Trafik pattern analizi (zaman dilimi bazlı)
- Eco-driving skorlaması

**Çıktılar:**
- Yakıt tüketimi tahmini
- Optimal hız profilleri
- Sürücü performans skorları
- CO2 emisyon hesaplamaları

---

### 6. MAKİNE ÖĞRENMESİ BAZLI TAHMİNSEL BAKIM

**Hedef:** Araç performans verilerinden arıza tahmini

**Kullanılacak Veriler:**
- `all_merged_data.csv`: Mesafe sayacı, hız, duraklama verileri
- `fleet.csv`: Araç yaşı ve tip bilgileri

**Yaklaşım:**
- Anomali tespiti (unusual patterns in vehicle behavior)
- Mesafe bazlı bakım planlaması
- Performans düşüşü tespiti

**Çıktılar:**
- Bakım zamanı tahminleri
- Kritik araç uyarıları
- Toplam sahip olma maliyeti (TCO) optimizasyonu

---

### 7. VATANDAŞ ODAKLI DASHBOARD VE GÖRSELLEŞTIRME

**Hedef:** Operasyonel verileri anlık takip edebilecek dashboard

**Kullanılacak Veriler:**
- Tüm veri setleri

**Yaklaşım:**
- Web tabanlı dashboard (Streamlit, Dash, Flask)
- Gerçek zamanlı GPS tracking
- KPI göstergeleri
- İnteraktif haritalar

**Çıktılar:**
- Gerçek zamanlı araç takip sistemi
- Mahalle bazlı hizmet durumu
- Performans metrikleri (günlük tonaj, rota süresi)
- Tahminsel analizler (gelecek hafta tahmini)

---

### 8. SÜRDÜRÜLEBİLİRLİK VE ÇEVRE ETKİSİ ANALİZİ

**Hedef:** Karbon ayak izi ve çevre etkisini minimize etme

**Kullanılacak Veriler:**
- `all_merged_data.csv`: Mesafe ve yakıt verileri
- `tonnages.csv`: Atık miktarları

**Yaklaşım:**
- CO2 emisyon hesaplamaları
- Geri dönüşüm potansiyeli analizi
- Alternatif yakıt/elektrikli araç geçiş simülasyonu
- Optimizasyon ile çevre etkisi azaltma

**Çıktılar:**
- Karbon ayak izi raporu
- Emisyon azaltım potansiyeli
- Sürdürülebilirlik skorları
- Alternatif senaryo simülasyonları

---

## 🔧 TEKNİK ARAÇLAR VE KÜTÜPHANELER

### Veri İşleme:
- **Pandas:** Veri manipülasyonu ve analizi
- **NumPy:** Sayısal hesaplamalar
- **Dask:** Büyük veri setleri için (all_merged_data.csv)

### Coğrafi Analiz:
- **GeoPandas:** Coğrafi veri işleme
- **Shapely:** Geometrik operasyonlar
- **Folium/Plotly:** Harita görselleştirme
- **Kepler.gl:** İleri seviye coğrafi görselleştirme

### Optimizasyon:
- **OR-Tools (Google):** VRP çözümü için
- **PuLP/Pyomo:** Doğrusal programlama
- **Scipy.optimize:** Optimizasyon algoritmaları

### Machine Learning:
- **Scikit-learn:** Temel ML algoritmaları
- **XGBoost/LightGBM:** Gradient boosting
- **Prophet/ARIMA:** Zaman serisi tahmini
- **TensorFlow/PyTorch:** Deep learning (LSTM)

### Görselleştirme:
- **Matplotlib/Seaborn:** Temel grafikler
- **Plotly/Bokeh:** İnteraktif görselleştirme
- **Streamlit/Dash:** Web dashboard

### Kümeleme ve Anomali Tespiti:
- **Scikit-learn DBSCAN/K-Means:** Clustering
- **Isolation Forest:** Anomali tespiti
- **PyOD:** Outlier detection

---

## 📈 BAŞLANGIÇ İÇİN ÖNERİLER

### Adım 1: Veri Keşfi (2-3 saat)
1. `fleet.csv` ve `truck_types.csv` ile filo yapısını anla
2. `neighbor_days_rotations.csv` ile operasyonel kısıtlamaları incele
3. `container_counts.csv` ile mahalle profillerini çıkar
4. `tonnages.csv` ile genel trendi gözlemle

### Adım 2: GPS Veri Analizi (4-6 saat)
1. `all_merged_data.csv`'yi sample olarak yükle (ilk 100K satır)
2. Araç bazlı hareket pattern'lerini analiz et
3. Duraklama noktalarını tespit et
4. Mahalle bazlı hizmet sürelerini hesapla

### Adım 3: Problem Tanımı (1-2 saat)
1. Yukarıdaki proje fikirlerinden birini seç
2. Açık bir problem statement yaz
3. Başarı metriklerini tanımla (örn: %20 mesafe azaltımı)

### Adım 4: Model Geliştirme (6-10 saat)
1. Baseline model oluştur (mevcut durumu simüle et)
2. Optimizasyon/ML modeli geliştir
3. Sonuçları karşılaştır

### Adım 5: Görselleştirme ve Sunum (2-3 saat)
1. Haritalar üzerinde sonuçları göster
2. Metrikleri dashboard'a dök
3. İyileştirme potansiyelini vurgula

---

## 🎯 ÖNCELİKLİ SORULAR VE CEVAPLARI

### S1: Hangi veri seti en önemli?
**C:** `all_merged_data.csv` - GPS verileri en zengin veri seti. Gerçek operasyonları gösteriyor ve optimizasyon için temel oluşturuyor.

### S2: Rota optimizasyonu için hangi algoritma?
**C:** Google OR-Tools ile VRP (Vehicle Routing Problem) çözümü en efektif. Kapasite kısıtlamaları, zaman pencereleri ve çoklu depot desteği var.

### S3: Büyük GPS verisini nasıl işlerim?
**C:** Pandas ile chunking ya da Dask kullan. İlk analizler için sample al (örn. 1 haftalık veri).

### S4: Mahalle bazlı tahmin nasıl yapılır?
**C:** Nüfus + konteyner sayısı + geçmiş tonaj verilerini feature olarak kullan. Random Forest ya da XGBoost ile regresyon.

### S5: Görselleştirme nasıl olmalı?
**C:** Folium ile interaktif haritalar, Streamlit ile dashboard. Rota öncesi/sonrası karşılaştırmaları göster.

---

## 💡 DEĞERLEME KRİTERLERİ (TAHMİNİ)

1. **Yenilikçilik (20%):** Ne kadar orijinal ve yaratıcı çözüm?
2. **Teknik Uygulama (25%):** Algoritma ve kod kalitesi
3. **Veri Kullanımı (20%):** Verileri ne kadar iyi entegre ettiniz?
4. **Etki (20%):** Gerçek hayatta uygulanabilir mi? Ne kadar tasarruf sağlar?
5. **Sunum (15%):** Görselleştirme ve anlatım kalitesi

---

## 📞 ÖNEMLİ NOTLAR

- **Veri boyutu:** `all_merged_data.csv` 113 MB - ilk analizler için sample kullan
- **Koordinat sistemi:** WGS84 (Enlem/Boylam) - harita görselleştirmeleri için uygun
- **Zaman dilimi:** Aralık 2024 - Aralık 2025 (24 aylık veri)
- **Kapsam:** Bursa Nilüfer İlçesi, 64 mahalle, ~560K nüfus
- **Özel durumlar:** Gölyazı gece toplama, bazı mahalleler günlük hizmet

---

## 🚀 HIZLI BAŞLANGIÇ KOD ÖRNEĞİ

```python
import pandas as pd
import geopandas as gpd
import folium
from datetime import datetime

# 1. Filo verilerini yükle
fleet = pd.read_csv('fleet.csv')
print(f"Toplam araç sayısı: {len(fleet)}")
print(fleet['vehicle_type'].value_counts())

# 2. Konteyner verilerini yükle
containers = pd.read_csv('container_counts.csv', sep=';')
print(f"\nToplam konteyner: {containers['TOPLAM'].sum()}")

# 3. GPS verilerini sample olarak yükle (ilk 100K satır)
gps_sample = pd.read_csv('Nilufer_bin_collection_dataset/all_merged_data.csv', 
                         sep=';', nrows=100000)
print(f"\nGPS kayıt sayısı: {len(gps_sample)}")

# 4. Tonaj verilerini yükle ve trend analizi
tonnages = pd.read_csv('tonnages.csv')
tonnages['Tarih'] = pd.to_datetime(tonnages['AY'] + ' ' + tonnages['YIL'].astype(str), 
                                   format='%B %Y', errors='coerce')
print(f"\nOrtalama aylık tonaj: {tonnages['Toplam Tonaj (TON)'].mean():.0f} ton")

# 5. Basit harita oluştur
m = folium.Map(location=[40.23, 28.98], zoom_start=12)
# GPS verilerini işaretle (örnek)
for idx, row in gps_sample.head(100).iterrows():
    folium.CircleMarker([row['Enlem'], row['Boylam']], radius=1).add_to(m)
m.save('map.html')
print("\nHarita oluşturuldu: map.html")
```

---

**SON SÖZ:** Bu proje, gerçek dünya problemi çözmek için harika bir fırsat. Veriler zengin ve gerçek. Hangi yaklaşımı seçersen seç, amacın somut, ölçülebilir iyileştirmeler göstermek olsun. Başarılar! 🎯🚛♻️
