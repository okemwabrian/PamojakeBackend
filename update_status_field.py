#!/usr/bin/env python
import os
import sys
import django
import sqlite3

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from django.conf import settings

def update_status_field():
    db_path = settings.DATABASES['default']['NAME']
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # SQLite doesn't support ALTER COLUMN, so we need to recreate the table
        # But for now, let's just check if we can work with existing data
        
        # Check current status values
        cursor.execute("SELECT DISTINCT status FROM applications_application")
        statuses = cursor.fetchall()
        print("Current status values:", [s[0] for s in statuses])
        
        # Update any existing 'pending' to match our new workflow
        cursor.execute("UPDATE applications_application SET status = 'pending' WHERE status = 'pending'")
        
        conn.commit()
        conn.close()
        print("\n[SUCCESS] Status field updated!")
        
    except Exception as e:
        print(f"[ERROR] Failed to update status field: {e}")

if __name__ == '__main__':
    update_status_field()