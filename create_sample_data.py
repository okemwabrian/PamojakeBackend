#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from django.contrib.auth import get_user_model
from announcements.models import Announcement
from meetings.models import Meeting
from contact.models import ContactMessage
from claims.models import Claim
from datetime import datetime, timedelta

User = get_user_model()

def create_sample_data():
    # Create active users
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
            'profile_completed': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
    
    test_user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True,
            'profile_completed': True
        }
    )
    if created:
        test_user.set_password('test123')
        test_user.save()
    
    # Create announcements
    Announcement.objects.get_or_create(
        title='Welcome to Pamoja Kenya MN',
        defaults={
            'content': 'Welcome to our community platform. We are excited to have you join us!',
            'author': admin_user,
            'is_active': True
        }
    )
    
    Announcement.objects.get_or_create(
        title='Monthly Meeting Reminder',
        defaults={
            'content': 'Don\'t forget about our monthly community meeting this Saturday.',
            'author': admin_user,
            'is_active': True
        }
    )
    
    # Create meetings
    Meeting.objects.get_or_create(
        title='Monthly Community Meeting',
        defaults={
            'description': 'Our regular monthly meeting to discuss community matters.',
            'date': datetime.now().date() + timedelta(days=7),
            'time': datetime.now().time(),
            'platform': 'Zoom',
            'meeting_link': 'https://zoom.us/j/123456789',
            'created_by': admin_user
        }
    )
    
    # Create contact messages
    ContactMessage.objects.get_or_create(
        subject='Test Message',
        defaults={
            'user': test_user,
            'email': test_user.email,
            'message': 'This is a test message from a user.',
            'status': 'new'
        }
    )
    
    # Create sample claim
    Claim.objects.get_or_create(
        user=test_user,
        claim_type='medical',
        defaults={
            'member_name': 'Test User',
            'relationship': 'self',
            'amount_requested': 1000.00,
            'incident_date': datetime.now().date(),
            'description': 'Medical emergency claim for testing.',
            'status': 'pending'
        }
    )
    
    print("Sample data created successfully!")
    print(f"Admin user: admin / admin123")
    print(f"Test user: testuser / test123")
    print(f"Announcements: {Announcement.objects.count()}")
    print(f"Meetings: {Meeting.objects.count()}")
    print(f"Contact Messages: {ContactMessage.objects.count()}")
    print(f"Claims: {Claim.objects.count()}")

if __name__ == '__main__':
    create_sample_data()