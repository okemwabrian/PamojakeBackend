#!/usr/bin/env python
"""
Setup script for Pamoja Kenya MN Backend
Run this script to set up the database and create initial data
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
    django.setup()

def run_migrations():
    print("Running database migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    print("✅ Migrations completed!")

def create_superuser():
    print("Creating superuser...")
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@pamojakenyamn.org',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print("✅ Superuser created!")
        print("Username: admin")
        print("Password: admin123")
    else:
        print("ℹ️ Superuser already exists")

def create_sample_data():
    print("Creating sample data...")
    from django.contrib.auth import get_user_model
    from announcements.models import Announcement
    from meetings.models import Meeting
    from django.utils import timezone
    from datetime import timedelta
    
    User = get_user_model()
    
    # Create sample user
    if not User.objects.filter(username='testuser').exists():
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            phone='555-0123',
            city='Minneapolis',
            state='MN'
        )
        print("✅ Sample user created (testuser/testpass123)")
    
    # Create sample announcement
    admin_user = User.objects.get(username='admin')
    if not Announcement.objects.exists():
        Announcement.objects.create(
            title='Welcome to Pamoja Kenya MN',
            content='Welcome to our community platform. Here you can manage your membership, submit claims, and stay updated with community news.',
            author=admin_user
        )
        print("✅ Sample announcement created")
    
    # Create sample meeting
    if not Meeting.objects.exists():
        Meeting.objects.create(
            title='Monthly Community Meeting',
            description='Join us for our monthly community meeting to discuss important matters.',
            date=timezone.now() + timedelta(days=7),
            location='Community Center, Minneapolis',
            organizer=admin_user
        )
        print("✅ Sample meeting created")

def main():
    print("🚀 Setting up Pamoja Kenya MN Backend...")
    print("=" * 50)
    
    setup_django()
    run_migrations()
    create_superuser()
    create_sample_data()
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://localhost:8000/admin")
    print("3. Login with: admin/admin123")
    print("4. API Base URL: http://localhost:8000/api")
    print("\n🔗 Available endpoints:")
    print("- Authentication: /api/auth/")
    print("- Applications: /api/applications/")
    print("- Payments: /api/payments/")
    print("- Claims: /api/claims/")
    print("- Documents: /api/documents/")
    print("- Announcements: /api/announcements/")
    print("- Meetings: /api/meetings/")
    print("- Contact: /api/contact/")

if __name__ == '__main__':
    main()