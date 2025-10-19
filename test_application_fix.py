#!/usr/bin/env python
"""
Test Application Submission Fix
"""

import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from applications.serializers import ApplicationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

def test_minimal_application():
    """Test application with minimal required fields"""
    print("Testing minimal application submission...")
    
    # Minimal data that frontend might send
    test_data = {
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
    
    serializer = ApplicationSerializer(data=test_data)
    
    if serializer.is_valid():
        print("SUCCESS: Minimal application data is valid!")
        print("Validated data includes:")
        for key, value in serializer.validated_data.items():
            print(f"  {key}: {value}")
        return True
    else:
        print("FAILED: Validation errors:")
        for field, errors in serializer.errors.items():
            print(f"  {field}: {errors}")
        return False

def test_double_application():
    """Test double membership application"""
    print("\nTesting double membership application...")
    
    test_data = {
        'membership_type': 'double',
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
        'emergency_relationship': 'spouse',
        'spouse_first_name': 'Jane',
        'spouse_last_name': 'Doe',
        'spouse_date_of_birth': '1992-01-01',
        'spouse_id_number': 'ID987654321'
    }
    
    serializer = ApplicationSerializer(data=test_data)
    
    if serializer.is_valid():
        print("SUCCESS: Double membership application is valid!")
        return True
    else:
        print("FAILED: Validation errors:")
        for field, errors in serializer.errors.items():
            print(f"  {field}: {errors}")
        return False

if __name__ == '__main__':
    success1 = test_minimal_application()
    success2 = test_double_application()
    
    if success1 and success2:
        print("\nALL TESTS PASSED! Application submission should now work.")
    else:
        print("\nSome tests failed. Check the errors above.")