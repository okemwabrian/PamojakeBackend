#!/usr/bin/env python
"""
Debug Application Submission Error
"""

import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from applications.models import Application
from applications.serializers import ApplicationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

def debug_application_fields():
    """Debug what fields the Application model expects"""
    print("=== APPLICATION MODEL FIELDS ===")
    
    # Get all model fields
    fields = Application._meta.get_fields()
    required_fields = []
    optional_fields = []
    
    for field in fields:
        if hasattr(field, 'blank') and hasattr(field, 'null'):
            if not field.blank and not field.null and field.name not in ['id', 'created_at', 'updated_at']:
                required_fields.append(field.name)
            else:
                optional_fields.append(field.name)
        elif hasattr(field, 'blank'):
            if not field.blank and field.name not in ['id', 'created_at', 'updated_at']:
                required_fields.append(field.name)
            else:
                optional_fields.append(field.name)
        else:
            optional_fields.append(field.name)
    
    print(f"REQUIRED FIELDS ({len(required_fields)}):")
    for field in sorted(required_fields):
        print(f"  - {field}")
    
    print(f"\nOPTIONAL FIELDS ({len(optional_fields)}):")
    for field in sorted(optional_fields):
        print(f"  - {field}")

def debug_serializer():
    """Debug what the serializer expects"""
    print("\n=== SERIALIZER VALIDATION ===")
    
    # Test minimal data
    test_data = {
        'membership_type': 'single',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@test.com',
        'phone': '123-456-7890'
    }
    
    serializer = ApplicationSerializer(data=test_data)
    if serializer.is_valid():
        print("✓ Minimal data is valid")
    else:
        print("✗ Validation errors:")
        for field, errors in serializer.errors.items():
            print(f"  {field}: {errors}")

def check_model_structure():
    """Check the actual model structure"""
    print("\n=== MODEL FIELD DETAILS ===")
    
    model_fields = {
        'membership_type': getattr(Application, 'membership_type', None),
        'type': getattr(Application, 'type', None),
        'first_name': getattr(Application, 'first_name', None),
        'address': getattr(Application, 'address', None),
        'address_1': getattr(Application, 'address_1', None),
        'state': getattr(Application, 'state', None),
        'state_province': getattr(Application, 'state_province', None),
        'zip_code': getattr(Application, 'zip_code', None),
        'zip_postal': getattr(Application, 'zip_postal', None),
    }
    
    for field_name, field_obj in model_fields.items():
        if field_obj:
            print(f"✓ {field_name}: EXISTS")
        else:
            print(f"✗ {field_name}: MISSING")

def test_application_creation():
    """Test creating an application with minimal data"""
    print("\n=== TEST APPLICATION CREATION ===")
    
    try:
        # Get or create a test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )
        
        # Try to create application with minimal data
        app_data = {
            'user': user,
            'membership_type': 'single',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@test.com',
            'phone': '123-456-7890',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'zip_code': '12345',
            'emergency_name': 'Jane Doe',
            'emergency_phone': '987-654-3210',
            'emergency_relationship': 'spouse'
        }
        
        application = Application(**app_data)
        application.save()
        print("✓ Application created successfully")
        
        # Clean up
        application.delete()
        if created:
            user.delete()
            
    except Exception as e:
        print(f"✗ Error creating application: {str(e)}")

if __name__ == '__main__':
    debug_application_fields()
    debug_serializer()
    check_model_structure()
    test_application_creation()