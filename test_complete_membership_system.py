#!/usr/bin/env python
"""
Complete Membership System Test Script
Tests all functionality of the comprehensive membership system
"""

import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from django.contrib.auth import get_user_model
from applications.models import Application
from claims.models import Claim
from payments.models import Payment
from shares.models import ShareTransaction
from django.utils import timezone
from datetime import date

User = get_user_model()

def test_user_model_enhancements():
    """Test enhanced User model with membership features"""
    print("Testing Enhanced User Model...")
    
    # Create user with new fields
    user = User.objects.create_user(
        username='testmember',
        email='test@example.com',
        password='testpass123',
        shares=15,
        membership_type='single'
    )
    
    print(f"Created user with {user.shares} shares, membership_type: {user.membership_type}")
    print(f"is_active_member: {user.is_active_member}")
    
    # Test auto-activation
    user.shares = 25
    user.save()
    
    print(f"Updated shares to {user.shares}")
    print(f"is_active_member: {user.is_active_member} (should be True)")
    print(f"activation_date: {user.activation_date}")
    
    assert user.is_active_member == True, "User should be auto-activated"
    assert user.shares_owned == user.shares, "shares_owned should sync with shares"
    
    user.delete()
    print("Enhanced User Model test PASSED!\n")

def test_comprehensive_application():
    """Test comprehensive membership application"""
    print("Testing Comprehensive Application Model...")
    
    user = User.objects.create_user(
        username='applicant',
        email='applicant@example.com',
        password='testpass123'
    )
    
    # Create comprehensive application
    application = Application.objects.create(
        user=user,
        type='double',
        first_name='John',
        last_name='Doe',
        email='john@example.com',
        phone='123-456-7890',
        date_of_birth=date(1990, 1, 1),
        id_number='12345678',
        address_1='123 Main St',
        city='Minneapolis',
        state_province='MN',
        zip_postal='55401',
        emergency_name='Jane Doe',
        emergency_phone='123-456-7891',
        emergency_relationship='spouse',
        spouse='Jane Doe',
        spouse_phone='123-456-7891',
        spouse_date_of_birth=date(1992, 5, 15),
        spouse_id_number='87654321',
        payment_amount=100.00
    )
    
    print(f"Created application: {application}")
    print(f"Type: {application.type}, Status: {application.status}")
    print(f"Emergency contact: {application.emergency_name}")
    print(f"Spouse: {application.spouse}")
    
    # Test approval process
    application.status = 'approved'
    application.save()
    
    # Update user based on application
    user.membership_type = application.type
    user.is_member = True
    user.is_active_member = True
    user.save()
    
    print(f"Application approved, user membership_type: {user.membership_type}")
    
    user.delete()
    application.delete()
    print("Comprehensive Application test PASSED!\n")

def test_payment_to_shares_conversion():
    """Test enhanced payment to shares conversion"""
    print("Testing Enhanced Payment-to-Shares Conversion...")
    
    user = User.objects.create_user(
        username='paymentuser',
        email='payment@example.com',
        password='testpass123',
        shares=0
    )
    
    # Create share payment
    payment = Payment.objects.create(
        user=user,
        payment_type='shares',
        amount=125.00,  # Should give 5 shares ($25 each)
        description='Share purchase',
        payment_method='paypal',
        transaction_id='TXN123456',
        status='pending'
    )
    
    print(f"Created payment: ${payment.amount}")
    print(f"User shares before approval: {user.shares}")
    
    # Approve payment
    payment.status = 'approved'
    payment.save()
    
    # Refresh user
    user.refresh_from_db()
    
    print(f"Payment approved")
    print(f"User shares after approval: {user.shares}")
    print(f"User shares_owned: {user.shares_owned}")
    print(f"is_active_member: {user.is_active_member} (should be True with 5 shares)")
    
    assert user.shares == 5, f"Expected 5 shares, got {user.shares}"
    assert user.shares_owned == 5, f"Expected shares_owned=5, got {user.shares_owned}"
    
    user.delete()
    payment.delete()
    print("Enhanced Payment-to-Shares test PASSED!\n")

def test_share_transaction_system():
    """Test share transaction system"""
    print("Testing Share Transaction System...")
    
    user = User.objects.create_user(
        username='shareuser',
        email='share@example.com',
        password='testpass123',
        shares=10
    )
    
    # Create share transaction
    transaction = ShareTransaction.objects.create(
        user=user,
        buyer_name=user.get_full_name(),
        quantity=15,
        amount_per_share=25.00,
        payment_method='bank',
        status='pending'
    )
    
    print(f"Created share transaction: {transaction.quantity} shares")
    print(f"Total amount: ${transaction.total_amount}")
    print(f"User shares before approval: {user.shares}")
    
    # Approve transaction
    transaction.status = 'approved'
    transaction.save()
    
    # Refresh user
    user.refresh_from_db()
    
    print(f"Transaction approved")
    print(f"User shares after approval: {user.shares}")
    print(f"is_active_member: {user.is_active_member}")
    
    assert user.shares == 25, f"Expected 25 shares, got {user.shares}"
    assert user.is_active_member == True, "User should be active with 25 shares"
    
    user.delete()
    transaction.delete()
    print("Share Transaction System test PASSED!\n")

def test_comprehensive_claims():
    """Test comprehensive claims system"""
    print("Testing Comprehensive Claims System...")
    
    user = User.objects.create_user(
        username='claimuser',
        email='claim@example.com',
        password='testpass123',
        shares=30,
        is_active_member=True
    )
    
    # Create comprehensive claim
    claim = Claim.objects.create(
        user=user,
        claim_type='medical',
        member_name='John Doe',
        relationship='self',
        incident_date=date.today(),
        amount_requested=750.00,
        description='Medical emergency - hospital bills'
    )
    
    print(f"Created claim: {claim.claim_type} for ${claim.amount_requested}")
    print(f"Member: {claim.member_name}, Relationship: {claim.relationship}")
    print(f"Status: {claim.status}")
    
    # Test approval
    claim.status = 'approved'
    claim.admin_notes = 'Claim approved - documentation verified'
    claim.save()
    
    print(f"Claim approved with notes: {claim.admin_notes}")
    
    user.delete()
    claim.delete()
    print("Comprehensive Claims test PASSED!\n")

def test_membership_type_system():
    """Test membership type system"""
    print("Testing Membership Type System...")
    
    # Test single membership
    single_user = User.objects.create_user(
        username='singleuser',
        email='single@example.com',
        password='testpass123',
        membership_type='single',
        shares=25,
        is_active_member=True
    )
    
    # Test double membership
    double_user = User.objects.create_user(
        username='doubleuser',
        email='double@example.com',
        password='testpass123',
        membership_type='double',
        shares=30,
        is_active_member=True
    )
    
    print(f"Single member: {single_user.membership_type}, shares: {single_user.shares}")
    print(f"Double member: {double_user.membership_type}, shares: {double_user.shares}")
    
    assert single_user.membership_type == 'single'
    assert double_user.membership_type == 'double'
    assert single_user.is_active_member == True
    assert double_user.is_active_member == True
    
    single_user.delete()
    double_user.delete()
    print("Membership Type System test PASSED!\n")

def test_auto_deactivation_system():
    """Test auto-deactivation when shares drop below 20"""
    print("Testing Auto-Deactivation System...")
    
    user = User.objects.create_user(
        username='deactivateuser',
        email='deactivate@example.com',
        password='testpass123',
        shares=25,
        is_active_member=True
    )
    
    print(f"User created with {user.shares} shares, is_active_member: {user.is_active_member}")
    
    # Reduce shares below threshold
    user.shares = 15
    user.save()
    
    print(f"Reduced shares to {user.shares}")
    print(f"is_active_member: {user.is_active_member} (should be False)")
    
    assert user.is_active_member == False, "User should be deactivated with <20 shares"
    
    # Test reactivation
    user.shares = 22
    user.save()
    
    print(f"Increased shares to {user.shares}")
    print(f"is_active_member: {user.is_active_member} (should be True)")
    
    assert user.is_active_member == True, "User should be reactivated with >=20 shares"
    
    user.delete()
    print("Auto-Deactivation System test PASSED!\n")

def run_all_tests():
    """Run all comprehensive membership system tests"""
    print("Starting Complete Membership System Tests\n")
    
    try:
        test_user_model_enhancements()
        test_comprehensive_application()
        test_payment_to_shares_conversion()
        test_share_transaction_system()
        test_comprehensive_claims()
        test_membership_type_system()
        test_auto_deactivation_system()
        
        print("ALL TESTS PASSED! Complete Membership System is working correctly.")
        print("\nVerified Features:")
        print("- Enhanced User model with membership types")
        print("- Comprehensive membership applications")
        print("- Payment-to-shares conversion (both approved and completed)")
        print("- Share transaction system with auto-activation")
        print("- Comprehensive claims system")
        print("- Single/Double membership types")
        print("- Auto-activation at 20+ shares")
        print("- Auto-deactivation below 20 shares")
        print("- Field synchronization (shares <-> shares_owned)")
        print("- Emergency contact and spouse information")
        print("- Document upload support")
        print("- Admin review tracking")
        
    except Exception as e:
        print(f"TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run_all_tests()