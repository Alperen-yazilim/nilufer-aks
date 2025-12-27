#!/usr/bin/env python
"""
NilüferAKS - İlk Kurulum Scripti
Veritabanını oluşturur ve temel verileri yükler
"""

import sys
import os

# Proje kök dizinini path'e ekle
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print("=" * 60)
print("🚀 NilüferAKS - İLK KURULUM")
print("=" * 60)

# 1. Veritabanı tablolarını oluştur
print("\n1️⃣ Veritabanı oluşturuluyor...")
from backend.database.database import init_database, create_default_users
init_database()
create_default_users()

# 2. Araç verilerini yükle
print("\n2️⃣ Araç verileri yükleniyor...")
from backend.database.init_db import import_fleet_data, import_neighborhood_data
import_fleet_data()
import_neighborhood_data()

# 3. Gamification sistemini kur
print("\n3️⃣ Gamification sistemi kuruluyor...")
try:
    from scripts.setup_gamification import setup_gamification
    setup_gamification()
except Exception as e:
    print(f"⚠️ Gamification kurulumu hatası (opsiyonel): {e}")

print("\n" + "=" * 60)
print("✅ KURULUM TAMAMLANDI!")
print("=" * 60)

print("\n📋 KULLANICILAR:")
print("-" * 60)
print("👤 YÖNETİCİ:")
print("   Kullanıcı: admin")
print("   Şifre: admin123")
print("\n👤 ŞOFÖR:")
print("   Kullanıcı: mehmet.yilmaz")
print("   Şifre: surucu123")
print("\n👤 VATANDAŞ:")
print("   Kayıt ol sayfasından yeni hesap oluşturabilirsiniz")
print("-" * 60)

print("\n🚀 BAŞLATMA:")
print("   python app.py")
print("   Tarayıcıda: http://localhost:5000")
print("=" * 60)
