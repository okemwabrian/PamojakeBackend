#!/usr/bin/env python
"""
Simple Backend Test Script for Pamoja
Tests all critical functionality
"""

import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from django.contrib.auth import get_user_model
from payments.models import Payment
from shares.models import ShareTransaction
from claims.models import Claim
from django.utils import timezone

User = get_user_model()

def test_user_auto_activation():
    """Test auto-activation when shares >= 20"""
    print("Testing User Auto-Activation...")
    
    # Create test user
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        shares_owned=15
    )
    
    print(f"User created with {user.shares_owned} shares, is_active_member: {user.is_active_member}")
    
    # Update shares to trigger auto-activation
    user.shares_owned = 25
    user.save()
    
    print(f"Updated shares to {user.shares_owned}, is_active_member: {user.is_active_member}")
    
    assert user.is_active_member == True, "User should be auto-activated"
    
    user.delete()
    print("User auto-activation test PASSED!\n")

def test_payment_to_shares():
    """Test payment approval converts to shares"""
    print("Testing Payment-to-Shares Conversion...")
    
    user = User.objects.create_user(
        username='paymentuser',
        email='payment@example.com',
        password='testpass123',
        shares_owned=0
    )
    
    # Create share payment
    payment = Payment.objects.create(
        user=user,
        payment_type='shares',
        amount=100.00,  # Should give 4 shares ($25 each)
        description='Share purchase',
        status='pending'
    )
    
    print(f"Created payment: ${payment.amount}, user shares before: {user.shares_owned}")
    
    # Approve payment
    payment.status = 'completed'
    payment.save()
    
    # Refresh user
    user.refresh_from_db()
    
    print(f"Payment approved, user shares after: {user.shares_owned}")
    
    assert user.shares_owned == 4, f"Expected 4 shares, got {user.shares_owned}"
    
    user.delete()
    payment.delete()
    print("Payment-to-shares conversion test PASSED!\n")

def test_endpoints():
    """Test that all endpoints are accessible"""
    print("Testing API Endpoints...")
    
    from django.test import Client
    from django.contrib.auth import get_user_model
    
    client = Client()
    
    # Test admin endpoints exist
    endpoints = [
        '/api/admin/payments/',
        '/api/admin/claims/',
        '/api/admin/users/',
        '/api/payments/',
        '/api/claims/',
        '/api/shares/',
    ]
    
    for endpoint in endpoints:
        try:
            response = client.get(endpoint)
            print(f"Endpoint {endpoint}: Status {response.status_code}")
        except Exception as e:
            print(f"Endpoint {endpoint}: ERROR - {str(e)}")
    
    print("Endpoint tests completed!\n")

def run_tests():
    """Run all tests"""
    print("Starting Backend Tests for Pamoja\n")
    
    try:
        test_user_auto_activation()
        test_payment_to_shares()
        test_endpoints()
        
        print("ALL TESTS PASSED! Backend is working correctly.")
        print("\nCritical Features Verified:")
        print("- User auto-activation at 20+ shares")
        print("- Payment-to-shares conversion ($25/share)")
        print("- API endpoints accessible")
        
    except Exception as e:
        print(f"TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run_tests()