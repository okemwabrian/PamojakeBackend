#!/usr/bin/env python
"""
Test Payment Submission Fix
"""

import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from payments.serializers import PaymentCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

def test_minimal_payment():
    """Test payment with minimal required fields"""
    print("Testing minimal payment submission...")
    
    # Minimal data that frontend might send
    test_data = {
        'payment_type': 'activation_fee',
        'amount': '150.00',
        'description': 'Activation fee payment'
    }
    
    serializer = PaymentCreateSerializer(data=test_data)
    
    if serializer.is_valid():
        print("SUCCESS: Minimal payment data is valid!")
        print("Validated data includes:")
        for key, value in serializer.validated_data.items():
            print(f"  {key}: {value}")
        return True
    else:
        print("FAILED: Validation errors:")
        for field, errors in serializer.errors.items():
            print(f"  {field}: {errors}")
        return False

def test_full_payment():
    """Test payment with all fields"""
    print("\nTesting full payment submission...")
    
    test_data = {
        'payment_type': 'shares',
        'amount': '250.00',
        'description': 'Share purchase payment',
        'payment_method': 'bank_transfer',
        'transaction_id': 'TXN123456'
    }
    
    serializer = PaymentCreateSerializer(data=test_data)
    
    if serializer.is_valid():
        print("SUCCESS: Full payment data is valid!")
        print("Validated data includes:")
        for key, value in serializer.validated_data.items():
            print(f"  {key}: {value}")
        return True
    else:
        print("FAILED: Validation errors:")
        for field, errors in serializer.errors.items():
            print(f"  {field}: {errors}")
        return False

if __name__ == '__main__':
    success1 = test_minimal_payment()
    success2 = test_full_payment()
    
    if success1 and success2:
        print("\nALL TESTS PASSED! Payment submission should now work.")
        print("Note: payment_proof file can be added via FormData in frontend")
    else:
        print("\nSome tests failed. Check the errors above.")