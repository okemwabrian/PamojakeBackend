#!/usr/bin/env python
import os
import sys
import django
import sqlite3

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from django.conf import settings

def add_activation_fields():
    db_path = settings.DATABASES['default']['NAME']
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Add activation fee fields to applications_application table
        fields_to_add = [
            "ALTER TABLE applications_application ADD COLUMN activation_fee_paid BOOLEAN DEFAULT 0",
            "ALTER TABLE applications_application ADD COLUMN activation_fee_amount DECIMAL(10,2) DEFAULT 50.00",
            "ALTER TABLE applications_application ADD COLUMN payment_reference VARCHAR(100) DEFAULT ''",
            "ALTER TABLE applications_application ADD COLUMN payment_verified BOOLEAN DEFAULT 0",
            "ALTER TABLE applications_application ADD COLUMN payment_verified_by_id INTEGER",
            "ALTER TABLE applications_application ADD COLUMN payment_verified_at DATETIME"
        ]
        
        for sql in fields_to_add:
            try:
                cursor.execute(sql)
                print(f"[OK] Added field: {sql.split('ADD COLUMN')[1].split()[0]}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"[SKIP] Field already exists: {sql.split('ADD COLUMN')[1].split()[0]}")
                else:
                    print(f"[ERROR] {e}")
        
        conn.commit()
        conn.close()
        print("\n[SUCCESS] Activation fee fields added to database!")
        
    except Exception as e:
        print(f"[ERROR] Failed to add fields: {e}")

if __name__ == '__main__':
    add_activation_fields()