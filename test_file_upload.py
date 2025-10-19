#!/usr/bin/env python
"""
Test script to verify file upload configuration
"""
import os
import django
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def test_file_upload_settings():
    """Test file upload configuration"""
    print("=== FILE UPLOAD CONFIGURATION TEST ===")
    
    # Check settings
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"FILE_UPLOAD_MAX_MEMORY_SIZE: {getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', 'Not set')}")
    print(f"DATA_UPLOAD_MAX_MEMORY_SIZE: {getattr(settings, 'DATA_UPLOAD_MAX_MEMORY_SIZE', 'Not set')}")
    print(f"DATA_UPLOAD_MAX_NUMBER_FIELDS: {getattr(settings, 'DATA_UPLOAD_MAX_NUMBER_FIELDS', 'Not set')}")
    
    # Check media directory exists
    media_root = settings.MEDIA_ROOT
    if os.path.exists(media_root):
        print(f"[OK] MEDIA_ROOT directory exists: {media_root}")
        
        # Check if writable
        try:
            test_file = default_storage.save('test_upload.txt', ContentFile('test content'))
            print(f"[OK] Media directory is writable")
            # Clean up
            default_storage.delete(test_file)
        except Exception as e:
            print(f"[ERROR] Media directory not writable: {e}")
    else:
        print(f"[ERROR] MEDIA_ROOT directory does not exist: {media_root}")
        try:
            os.makedirs(media_root, exist_ok=True)
            print(f"[OK] Created MEDIA_ROOT directory: {media_root}")
        except Exception as e:
            print(f"[ERROR] Could not create MEDIA_ROOT directory: {e}")
    
    # Check subdirectories
    subdirs = ['applications/ids', 'applications/spouse_ids', 'payment_evidence', 'share_payments', 'claims', 'documents']
    for subdir in subdirs:
        full_path = os.path.join(media_root, subdir)
        if os.path.exists(full_path):
            print(f"[OK] {subdir} directory exists")
        else:
            try:
                os.makedirs(full_path, exist_ok=True)
                print(f"[OK] Created {subdir} directory")
            except Exception as e:
                print(f"[ERROR] Could not create {subdir} directory: {e}")
    
    print("\n=== CORS CONFIGURATION ===")
    print(f"CORS_ALLOW_ALL_ORIGINS: {getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', 'Not set')}")
    print(f"CORS_ALLOW_CREDENTIALS: {getattr(settings, 'CORS_ALLOW_CREDENTIALS', 'Not set')}")
    
    print("\n=== PARSER CLASSES CHECK ===")
    from applications.views import ApplicationViewSet
    from payments.views import PaymentViewSet
    
    app_parsers = getattr(ApplicationViewSet, 'parser_classes', [])
    payment_parsers = getattr(PaymentViewSet, 'parser_classes', [])
    
    print(f"ApplicationViewSet parsers: {[p.__name__ for p in app_parsers]}")
    print(f"PaymentViewSet parsers: {[p.__name__ for p in payment_parsers]}")
    
    print("\n=== TEST COMPLETE ===")

if __name__ == '__main__':
    test_file_upload_settings()