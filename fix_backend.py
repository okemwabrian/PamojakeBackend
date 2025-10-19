#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from django.contrib.auth import get_user_model
from announcements.models import Announcement
from meetings.models import Meeting
from contact.models import ContactMessage
from claims.models import Claim

User = get_user_model()

def create_sample_data():
    print("Creating sample data...")
    
    # Create admin user if not exists
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@pamoja.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
            'profile_completed': True,
            'shares_owned': 100,
            'available_shares': 50
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("[OK] Admin user created")
    else:
        print("[OK] Admin user already exists")
    
    # Create test user if not exists
    test_user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@pamoja.com',
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True,
            'profile_completed': True,
            'shares_owned': 25,
            'available_shares': 10
        }
    )
    if created:
        test_user.set_password('test123')
        test_user.save()
        print("[OK] Test user created")
    else:
        print("[OK] Test user already exists")
    
    # Create sample announcements
    announcements_data = [
        {
            'title': 'Welcome to Pamoja Kenya MN',
            'content': 'Welcome to our community platform. Here you can manage your membership, buy shares, submit claims, and stay updated with community news.',
            'priority': 'high',
            'is_pinned': True
        },
        {
            'title': 'Monthly Meeting Reminder',
            'content': 'Don\'t forget about our monthly community meeting this Saturday at 2 PM. We will discuss important community matters.',
            'priority': 'medium'
        },
        {
            'title': 'New Share Purchase Options',
            'content': 'We have introduced new flexible payment options for share purchases. Check out the Shares section for more details.',
            'priority': 'low'
        }
    ]
    
    for ann_data in announcements_data:
        announcement, created = Announcement.objects.get_or_create(
            title=ann_data['title'],
            defaults={
                'content': ann_data['content'],
                'author': admin_user,
                'priority': ann_data['priority'],
                'is_pinned': ann_data.get('is_pinned', False)
            }
        )
        if created:
            print(f"[OK] Created announcement: {ann_data['title']}")
    
    # Create sample meetings
    meetings_data = [
        {
            'title': 'Monthly Community Meeting',
            'description': 'Our regular monthly meeting to discuss community matters, financial updates, and upcoming events.',
            'date': datetime.now() + timedelta(days=7),
            'duration': 120,
            'type': 'virtual',
            'meeting_link': 'https://zoom.us/j/123456789'
        },
        {
            'title': 'Annual General Meeting',
            'description': 'Annual meeting for all members to review the year\'s activities and elect new committee members.',
            'date': datetime.now() + timedelta(days=30),
            'duration': 180,
            'type': 'in_person',
            'require_registration': True
        }
    ]
    
    for meet_data in meetings_data:
        meeting, created = Meeting.objects.get_or_create(
            title=meet_data['title'],
            defaults={
                'description': meet_data['description'],
                'date': meet_data['date'],
                'duration': meet_data['duration'],
                'type': meet_data['type'],
                'meeting_link': meet_data.get('meeting_link', ''),
                'require_registration': meet_data.get('require_registration', False),
                'created_by': admin_user
            }
        )
        if created:
            print(f"[OK] Created meeting: {meet_data['title']}")
    
    # Create sample contact messages
    contact_data = [
        {
            'user': test_user,
            'name': 'Test User',
            'email': 'test@pamoja.com',
            'subject': 'Question about membership',
            'message': 'I have a question about the membership benefits. Can you provide more information?',
            'status': 'new'
        },
        {
            'user': None,
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Interest in joining',
            'message': 'I am interested in joining Pamoja Kenya MN. How can I apply for membership?',
            'status': 'replied',
            'admin_reply': 'Thank you for your interest! Please visit our membership section to apply.',
            'replied_by': admin_user
        }
    ]
    
    for contact in contact_data:
        message, created = ContactMessage.objects.get_or_create(
            subject=contact['subject'],
            email=contact['email'],
            defaults=contact
        )
        if created:
            print(f"[OK] Created contact message: {contact['subject']}")
    
    # Create sample claims
    claims_data = [
        {
            'user': test_user,
            'claim_type': 'medical',
            'member_name': 'Test User',
            'relationship': 'self',
            'amount_requested': Decimal('500.00'),
            'incident_date': datetime.now().date() - timedelta(days=10),
            'description': 'Medical expenses for hospital treatment',
            'status': 'pending'
        },
        {
            'user': test_user,
            'claim_type': 'education',
            'member_name': 'Jane Doe',
            'relationship': 'daughter',
            'amount_requested': Decimal('1000.00'),
            'amount_approved': Decimal('800.00'),
            'incident_date': datetime.now().date() - timedelta(days=30),
            'description': 'School fees for secondary education',
            'status': 'approved',
            'admin_notes': 'Approved with reduced amount based on available funds'
        }
    ]
    
    for claim_data in claims_data:
        claim, created = Claim.objects.get_or_create(
            user=claim_data['user'],
            claim_type=claim_data['claim_type'],
            member_name=claim_data['member_name'],
            defaults=claim_data
        )
        if created:
            print(f"[OK] Created claim: {claim_data['claim_type']} for {claim_data['member_name']}")
    
    print("\n[SUCCESS] Sample data creation completed!")
    print("\nLogin credentials:")
    print("Admin: username=admin, password=admin123")
    print("Test User: username=testuser, password=test123")

if __name__ == '__main__':
    create_sample_data()