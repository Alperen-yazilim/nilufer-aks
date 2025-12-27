"""
Veritabanı Başlatma ve CSV İmport
"""

import sqlite3
import pandas as pd
import os
from backend.database.database import init_database, create_default_users, DB_PATH

# Ana proje klasörü (backend/database/'den 2 üst)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def import_fleet_data():
    """fleet.csv'den araçları import et - GERÇEK VERİ"""
    try:
        fleet_path = os.path.join(PROJECT_ROOT, 'full_dataset', 'fleet.csv')
        df = pd.read_csv(fleet_path)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT OR REPLACE INTO fleet (vehicle_id, vehicle_name, vehicle_type, capacity_m3, capacity_ton)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                str(row['vehicle_id']),
                row['vehicle_name'],
                row['vehicle_type'],
                row['capacity_m3'],
                row['capacity_ton']
            ))
        
        conn.commit()
        conn.close()
        print(f"✅ {len(df)} araç import edildi")
    except Exception as e:
        print(f"❌ Fleet import hatası: {e}")

def import_neighborhood_data():
    """Mahalle verilerini import et - GERÇEK VERİ"""
    try:
        # Konteyner sayıları
        container_path = os.path.join(PROJECT_ROOT, 'full_dataset', 'container_counts.csv')
        df_containers = pd.read_csv(container_path, sep=';')
        df_containers.columns = df_containers.columns.str.strip()
        
        # TOPLAM sütununu temizle
        df_containers['TOPLAM'] = df_containers['TOPLAM'].astype(str).str.replace('.', '').str.replace(',', '')
        df_containers['TOPLAM'] = pd.to_numeric(df_containers['TOPLAM'], errors='coerce').fillna(0).astype(int)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        for _, row in df_containers.iterrows():
            mahalle_adi = row['MAHALLE'].strip()
            toplam_konteyner = row['TOPLAM']
            yeralti = row.get('YERALTI KONTEYNER', 0)
            
            # Vinç gerekli mi?
            try:
                yeralti_int = int(str(yeralti).replace('.', '').replace(',', '')) if pd.notna(yeralti) else 0
            except:
                yeralti_int = 0
            
            requires_crane = 1 if yeralti_int > 0 else 0
            
            cursor.execute('''
                INSERT OR REPLACE INTO neighborhoods 
                (name, total_containers, underground_containers, requires_crane)
                VALUES (?, ?, ?, ?)
            ''', (
                mahalle_adi,
                int(toplam_konteyner),
                yeralti_int,
                requires_crane
            ))
        
        conn.commit()
        conn.close()
        print(f"✅ {len(df_containers)} mahalle import edildi")
    except Exception as e:
        print(f"❌ Mahalle import hatası: {e}")

def import_tonnage_data():
    """Tonaj verilerini metrics tablosuna import et - GERÇEK VERİ"""
    try:
        tonnage_path = os.path.join(PROJECT_ROOT, 'full_dataset', 'tonnages.csv')
        # Hatalı satırları atla
        df = pd.read_csv(tonnage_path, on_bad_lines='skip')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        for _, row in df.iterrows():
            # Tarih oluştur (basit)
            ay_map = {
                'OCAK': 1, 'ŞUBAT': 2, 'MART': 3, 'NİSAN': 4,
                'MAYIS': 5, 'HAZİRAN': 6, 'TEMMUZ': 7, 'AĞUSTOS': 8,
                'EYLÜL': 9, 'EKİM': 10, 'KASIM': 11, 'ARALIK': 12
            }
            ay = ay_map.get(row['AY'].upper(), 1)
            yil = int(row['YIL'])
            tarih = f"{yil}-{ay:02d}-01"
            
            cursor.execute('''
                INSERT OR REPLACE INTO metrics (date, total_tonnage)
                VALUES (?, ?)
            ''', (tarih, row['Toplam Tonaj (TON)']))
        
        conn.commit()
        conn.close()
        print(f"✅ {len(df)} tonaj kaydı import edildi")
    except Exception as e:
        print(f"❌ Tonaj import hatası: {e}")

if __name__ == '__main__':
    print("=" * 60)
    print("NilüferAKS Veritabanı Başlatma")
    print("=" * 60)
    
    # 1. Tabloları oluştur
    print("\n1. Veritabanı tabloları oluşturuluyor...")
    init_database()
    
    # 2. Kullanıcıları oluştur
    print("\n2. Varsayılan kullanıcılar oluşturuluyor...")
    create_default_users()
    
    # 3. Fleet verisini import et
    print("\n3. Araç verileri import ediliyor...")
    import_fleet_data()
    
    # 4. Mahalle verilerini import et
    print("\n4. Mahalle verileri import ediliyor...")
    import_neighborhood_data()
    
    # 5. Tonaj verilerini import et
    print("\n5. Tonaj verileri import ediliyor...")
    import_tonnage_data()
    
    print("\n" + "=" * 60)
    print("✅ Veritabanı başlatma tamamlandı!")
    print("=" * 60)
    print("\n📋 GİRİŞ BİLGİLERİ:")
    print("-" * 60)
    print("👔 Yönetici Paneli:")
    print("   Kullanıcı: admin")
    print("   Şifre: admin123")
    print()
    print("🚛 Sürücü Portali:")
    print("   Kullanıcı: mehmet.yilmaz")
    print("   Şifre: surucu123")
    print()
    print("📍 Canlı Takip:")
    print("   Giriş gerektirmez (Public erişim)")
    print("=" * 60)
