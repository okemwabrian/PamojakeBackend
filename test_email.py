#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from django.core.mail import send_mail

def test_email():
    try:
        send_mail(
            'Test Email - Pamoja Kenya MN',
            'This is a test email to verify email configuration.',
            'pamojakeny@gmail.com',
            ['pamojakeny@gmail.com'],  # Send to yourself for testing
            fail_silently=False,
        )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email failed: {e}")

if __name__ == '__main__':
    test_email()