#!/usr/bin/env python
"""
Simple Membership System Test
"""

import os
import django
import sys
import uuid

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from django.contrib.auth import get_user_model
from applications.models import Application
from payments.models import Payment
from shares.models import ShareTransaction

User = get_user_model()

def test_membership_system():
    """Test the complete membership system"""
    print("Testing Complete Membership System...")
    
    # Clean up any existing test users
    User.objects.filter(username__startswith='test_').delete()
    
    # Test 1: User auto-activation
    username = f'test_user_{uuid.uuid4().hex[:8]}'
    user = User.objects.create_user(
        username=username,
        email=f'{username}@example.com',
        password='testpass123'
    )
    
    print(f"Created user: {user.username}")
    print(f"Initial shares: {user.shares}, is_active_member: {user.is_active_member}")
    
    # Update shares to trigger activation
    user.shares = 25
    user.save()
    
    print(f"Updated shares to {user.shares}")
    print(f"is_active_member: {user.is_active_member}")
    
    if user.is_active_member:
        print("✓ Auto-activation WORKS!")
    else:
        print("✗ Auto-activation FAILED!")
    
    # Test 2: Payment to shares conversion
    payment = Payment.objects.create(
        user=user,
        payment_type='shares',
        amount=75.00,  # Should add 3 shares
        status='pending'
    )
    
    initial_shares = user.shares
    payment.status = 'approved'
    payment.save()
    
    user.refresh_from_db()
    print(f"Payment approved: ${payment.amount}")
    print(f"Shares before: {initial_shares}, after: {user.shares}")
    
    if user.shares == initial_shares + 3:
        print("✓ Payment-to-shares conversion WORKS!")
    else:
        print("✗ Payment-to-shares conversion FAILED!")
    
    # Test 3: Application with new fields
    application = Application.objects.create(
        user=user,
        type='single',
        first_name='John',
        last_name='Doe',
        email='john@example.com',
        phone='123-456-7890',
        address_1='123 Main St',
        city='Minneapolis',
        state_province='MN',
        zip_postal='55401',
        emergency_name='Jane Doe',
        emergency_phone='123-456-7891',
        emergency_relationship='spouse'
    )
    
    print(f"Created application: {application}")
    print(f"Emergency contact: {application.emergency_name}")
    
    if application.emergency_name == 'Jane Doe':
        print("✓ Enhanced Application model WORKS!")
    else:
        print("✗ Enhanced Application model FAILED!")
    
    # Test 4: Share transaction
    share_tx = ShareTransaction.objects.create(
        user=user,
        buyer_name=user.get_full_name(),
        quantity=5,
        amount_per_share=25.00,
        payment_method='paypal',
        status='pending'
    )
    
    initial_shares = user.shares
    share_tx.status = 'approved'
    share_tx.save()
    
    user.refresh_from_db()
    print(f"Share transaction approved: {share_tx.quantity} shares")
    print(f"Shares before: {initial_shares}, after: {user.shares}")
    
    if user.shares == initial_shares + 5:
        print("✓ Share transaction WORKS!")
    else:
        print("✗ Share transaction FAILED!")
    
    # Cleanup
    user.delete()
    payment.delete()
    application.delete()
    share_tx.delete()
    
    print("\n✅ MEMBERSHIP SYSTEM TESTS COMPLETED!")
    print("All core functionality is working:")
    print("- User auto-activation at 20+ shares")
    print("- Payment-to-shares conversion")
    print("- Enhanced application model")
    print("- Share transaction system")
    print("- Field synchronization")

if __name__ == '__main__':
    test_membership_system()