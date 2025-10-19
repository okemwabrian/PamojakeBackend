#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from django.contrib.auth import get_user_model
from announcements.models import Announcement
from meetings.models import Meeting
from contact.models import ContactMessage
from claims.models import Claim

User = get_user_model()

def check_backend_status():
    print("=== BACKEND STATUS CHECK ===")
    print()
    
    # Check users
    print("[USERS]:")
    users = User.objects.all()
    for user in users:
        print(f"  - {user.username}: Active={user.is_active}, Staff={user.is_staff}, Email={user.email}")
    print(f"  Total: {users.count()} users")
    print()
    
    # Check announcements
    print("[ANNOUNCEMENTS]:")
    announcements = Announcement.objects.all()
    for ann in announcements:
        print(f"  - {ann.title}: Active={ann.is_active}, Author={ann.author.username}")
    print(f"  Total: {announcements.count()} announcements")
    print()
    
    # Check meetings
    print("[MEETINGS]:")
    meetings = Meeting.objects.all()
    for meeting in meetings:
        print(f"  - {meeting.title}: Date={meeting.date}, Creator={meeting.created_by.username}")
    print(f"  Total: {meetings.count()} meetings")
    print()
    
    # Check contact messages
    print("[CONTACT MESSAGES]:")
    contacts = ContactMessage.objects.all()
    for contact in contacts:
        user_info = contact.user.username if contact.user else contact.email
        print(f"  - {contact.subject}: Status={contact.status}, From={user_info}")
    print(f"  Total: {contacts.count()} messages")
    print()
    
    # Check claims
    print("[CLAIMS]:")
    claims = Claim.objects.all()
    for claim in claims:
        print(f"  - {claim.claim_type} by {claim.user.username}: Status={claim.status}, Amount=${claim.amount_requested}")
    print(f"  Total: {claims.count()} claims")
    print()
    
    print("=== STATUS CHECK COMPLETE ===")

if __name__ == '__main__':
    check_backend_status()