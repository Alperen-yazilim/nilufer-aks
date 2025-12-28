# -*- coding: utf-8 -*-
"""
KONTEYNER TIP TAHMİNİ - ML MODEL
GPS'teki araç ziyaretlerine göre konteyner tipini öğren
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("KONTEYNER TIP TAHMINI - ML MODEL")
print("="*80)

# Klasör oluştur
os.makedirs('mah_kon', exist_ok=True)

# Kayıt dosyaları
FEATURE_FILE = 'mah_kon/features_extracted.csv'
MODEL_FILE = 'mah_kon/model_rf.pkl'

# ============================================================================
# ADIM 1: VERİLERİ YÜKLE
# ============================================================================
print("\nVeriler yukleniyor...")

# GPS verisi (hangi araç hangi konteynere gitti)
gps = pd.read_csv('all_merged_data.csv', encoding='utf-8')

# Fleet verisini yükle (araç tipleri için)
fleet = pd.read_csv('fleet.csv', encoding='utf-8')
gps = gps.merge(fleet[['vehicle_id', 'vehicle_type']], on='vehicle_id', how='left')

# Araç tipi encode
arac_tip_kod = {'Crane Vehicle': 1, 'Large Garbage Truck': 2, 'Small Garbage Truck': 3}
gps['arac_tipi'] = gps['vehicle_type'].map(arac_tip_kod).fillna(0).astype(int)

# Sadece duran noktalar
gps = gps[gps['Hız(km/sa)'] < 5].copy()

# Konteyner koordinatları
konteynerler = pd.read_csv('arac_rota/konteynerler/konteyner_mahalle.csv', encoding='utf-8')

# Mahalle bazlı gerçek oranlar (training data için)
mahalle_data = pd.read_csv('master_mahalle_data.csv', encoding='utf-8')

print(f"GPS nokta: {len(gps):,}")
print(f"Konteyner: {len(konteynerler):,}")

# ============================================================================
# ADIM 2: HER KONTEYNER İÇİN FEATURE ÇIKAR
# ============================================================================
print("\nFeature extraction (her konteyner için hangi araç ziyaret etti)...")

# Kayıtlı feature varsa yükle
if os.path.exists(FEATURE_FILE):
    print(f"   Kayitli feature bulundu! Yukleniyor: {FEATURE_FILE}")
    features_df = pd.read_csv(FEATURE_FILE, encoding='utf-8')
    print(f"   {len(features_df)} konteyner feature yuklendi!")
else:
    print("   Feature extraction baslaniyor (ilk calisma - uzun surebilir)...")

    from sklearn.neighbors import BallTree

    # BallTree ile hızlı eşleştirme
    konteyner_coords = konteynerler[['enlem', 'boylam']].values
    konteyner_coords_rad = np.radians(konteyner_coords)
    tree = BallTree(konteyner_coords_rad, metric='haversine')

    # GPS noktaları
    gps_coords = gps[['Enlem', 'Boylam']].values
    gps_coords_rad = np.radians(gps_coords)

    # Her GPS noktası hangi konteynere yakın? (10m içinde)
    YARICAP_KM = 0.010  # 10 metre
    distances, indices = tree.query_radius(gps_coords_rad, r=YARICAP_KM/6371, return_distance=True)

    # Her konteyner için feature hesapla
    features = []

    for i in range(len(konteynerler)):
        # Bu konteynere yakın GPS noktaları
        yakin_gps_mask = [i in idx_list for idx_list in indices]
        yakin_gps = gps[yakin_gps_mask].copy()
        
        if len(yakin_gps) == 0:
            # Hiç ziyaret edilmemiş (muhtemelen ML tahmin)
            features.append({
                'konteyner_id': konteynerler.iloc[i]['konteyner_id'],
                'arac_tipi_1': 0,  # Vinç
                'arac_tipi_2': 0,  # Büyük kamyon
                'arac_tipi_3': 0,  # Küçük kamyon
                'toplam_ziyaret': 0,
                'baskin_arac': 0,
                'farkli_gun': 0,
                'mahalle': konteynerler.iloc[i]['mahalle']
            })
            continue
        
        # Araç tipi sayıları
        arac_sayilari = yakin_gps['arac_tipi'].value_counts()
        n_tipi_1 = arac_sayilari.get(1, 0)  # Vinç
        n_tipi_2 = arac_sayilari.get(2, 0)  # Büyük
        n_tipi_3 = arac_sayilari.get(3, 0)  # Küçük
        
        # Baskın araç
        baskin = arac_sayilari.idxmax() if len(arac_sayilari) > 0 else 0
        
        # Kaç farklı günde ziyaret edildi
        if 'Gun' in yakin_gps.columns:
            farkli_gun = yakin_gps['Gun'].nunique()
        elif 'Tarih' in yakin_gps.columns:
            farkli_gun = yakin_gps['Tarih'].nunique()
        else:
            farkli_gun = 1
        
        features.append({
            'konteyner_id': konteynerler.iloc[i]['konteyner_id'],
            'arac_tipi_1': n_tipi_1,
            'arac_tipi_2': n_tipi_2,
            'arac_tipi_3': n_tipi_3,
            'toplam_ziyaret': len(yakin_gps),
            'baskin_arac': baskin,
            'farkli_gun': farkli_gun,
            'mahalle': konteynerler.iloc[i]['mahalle']
        })

    features_df = pd.DataFrame(features)
    print(f"Feature extraction tamamlandi! {len(features_df)} konteyner")
    
    # Kaydet
    features_df.to_csv(FEATURE_FILE, index=False, encoding='utf-8-sig')
    print(f"   Feature kaydedildi: {FEATURE_FILE}")

# ============================================================================
# ADIM 3: TRAINING DATA OLUŞTUR (MAHALLE ORANLARINDAN)
# ============================================================================
print("\nTraining data olusturuluyor...")

def normalize_mahalle(text):
    if not isinstance(text, str):
        return ""
    text = str(text).upper().strip()
    text = text.replace(' MAHALLESİ', '').replace(' MAHALLESI', '')
    text = text.replace(' MH.', '').replace(' MH', '')
    import re
    text = re.sub(r'\s+', ' ', text).strip()
    return text

features_df['mahalle_norm'] = features_df['mahalle'].apply(normalize_mahalle)
mahalle_data['mahalle_norm'] = mahalle_data['mahalle'].apply(normalize_mahalle)

# Her konteyner için tip ata (oran bazlı)
labels = []

for mahalle_norm in features_df['mahalle_norm'].unique():
    mahalle_mask = features_df['mahalle_norm'] == mahalle_norm
    n_konteyner = mahalle_mask.sum()
    
    # Master dosyadan oranları al
    mahalle_info = mahalle_data[mahalle_data['mahalle_norm'] == mahalle_norm]
    
    if len(mahalle_info) == 0:
        # Veri yok - skip
        for _ in range(n_konteyner):
            labels.append('Bilinmiyor')
        continue
    
    info = mahalle_info.iloc[0]
    n_yeralti = int(info['yeralti_konteyner'])
    n_770 = int(info['konteyner_770lt'])
    n_400 = int(info['konteyner_400lt'])
    n_plastik = int(info['plastik'])
    n_toplam = n_yeralti + n_770 + n_400 + n_plastik
    
    if n_toplam == 0:
        for _ in range(n_konteyner):
            labels.append('Bilinmiyor')
        continue
    
    # Oranları hesapla
    oran_yeralti = n_yeralti / n_toplam
    oran_770 = n_770 / n_toplam
    oran_400 = n_400 / n_toplam
    oran_plastik = n_plastik / n_toplam
    
    hedef_yeralti = int(n_konteyner * oran_yeralti)
    hedef_770 = int(n_konteyner * oran_770)
    hedef_400 = int(n_konteyner * oran_400)
    hedef_plastik = n_konteyner - hedef_yeralti - hedef_770 - hedef_400
    
    tipler = (['Yeraltı'] * hedef_yeralti + 
              ['770L'] * hedef_770 + 
              ['400L'] * hedef_400 + 
              ['Plastik'] * hedef_plastik)
    np.random.shuffle(tipler)
    
    labels.extend(tipler)

features_df['tip'] = labels

# Bilinmiyor olanları çıkar
train_data = features_df[features_df['tip'] != 'Bilinmiyor'].copy()
print(f"Training data: {len(train_data)} konteyner")
print(f"Tip dagilimi:\n{train_data['tip'].value_counts()}")

# ============================================================================
# ADIM 4: ML MODEL EĞİT
# ============================================================================
print("\nModel egitiliyor (RandomForest)...")

# Kayıtlı model varsa yükle
if os.path.exists(MODEL_FILE):
    print(f"   Kayitli model bulundu! Yukleniyor: {MODEL_FILE}")
    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)
    print("   Model yuklendi!")
else:
    print("   Model egitimi baslaniyor...")

    # Feature'lar
    X = train_data[['arac_tipi_1', 'arac_tipi_2', 'arac_tipi_3', 
                    'toplam_ziyaret', 'baskin_arac', 'farkli_gun']]
    y = train_data['tip']

    # Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Model
    model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Kaydet
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)
    print(f"   Model kaydedildi: {MODEL_FILE}")

    # Değerlendirme
    y_pred = model.predict(X_test)
    accuracy = (y_pred == y_test).mean()
    
    print(f"\nModel Accuracy: {accuracy*100:.1f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nFeature Importance:")
    for _, row in feature_importance.iterrows():
        print(f"  {row['feature']:<20} {row['importance']:.3f}")

# ============================================================================
# ADIM 5: TÜM KONTEYNERLERE TAHMİN YAP
# ============================================================================
print("\nTum konteynerlere tip tahmini yapiliyor...")

X_all = features_df[['arac_tipi_1', 'arac_tipi_2', 'arac_tipi_3', 
                      'toplam_ziyaret', 'baskin_arac', 'farkli_gun']]
features_df['tip_tahmin'] = model.predict(X_all)

# Tahmin güveni (olasılık)
tahmin_olasilik = model.predict_proba(X_all)
features_df['tahmin_guveni'] = tahmin_olasilik.max(axis=1)

# Konteynerlerle birleştir
konteyner_final = konteynerler.merge(features_df[['konteyner_id', 'tip_tahmin', 'tahmin_guveni']], 
                                       on='konteyner_id', how='left')

# ============================================================================
# ADIM 6: SONUÇLARI KAYDET
# ============================================================================
print("\nSonuclar kaydediliyor...")

konteyner_final.to_csv('mah_kon/konteyner_tipli_ml.csv', index=False, encoding='utf-8-sig')

# Mahalle bazlı detaylı özet
mahalle_tip_ozet = konteyner_final.groupby(['mahalle', 'tip_tahmin']).size().reset_index(name='adet')
mahalle_tip_pivot = mahalle_tip_ozet.pivot(index='mahalle', columns='tip_tahmin', values='adet').fillna(0).astype(int)
mahalle_tip_pivot['TOPLAM'] = mahalle_tip_pivot.sum(axis=1)
mahalle_tip_pivot.to_csv('mah_kon/mahalle_tip_detay_ml.csv', encoding='utf-8-sig')

# Özet
print("\n" + "="*80)
print("ML TIP TAHMINI SONUC:")
print("="*80)
tip_dagilim = konteyner_final['tip_tahmin'].value_counts()
for tip, sayi in tip_dagilim.items():
    print(f"{tip:<15} {sayi:>8} ({sayi/len(konteyner_final)*100:>5.1f}%)")
print("="*80)
print(f"{'TOPLAM':<15} {len(konteyner_final):>8}")
print("="*80)

print(f"\nOrtalama tahmin guveni: {konteyner_final['tahmin_guveni'].mean()*100:.1f}%")
print(f"\nDosyalar kaydedildi (mah_kon/ klasoru):")
print(f"  - konteyner_tipli_ml.csv (Her konteyner)")
print(f"  - mahalle_tip_detay_ml.csv (Mahalle bazli ozet)")
print(f"  - features_extracted.csv (Bir sonraki calisma icin)")
print(f"  - model_rf.pkl (Bir sonraki calisma icin)")
