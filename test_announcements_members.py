#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def test_announcements_and_members():
    print("Testing Announcements and Members Endpoints...")
    
    # Get admin user
    admin_user = User.objects.filter(is_staff=True).first()
    if not admin_user:
        print("[ERROR] No admin user found")
        return
    
    # Get JWT token
    refresh = RefreshToken.for_user(admin_user)
    access_token = str(refresh.access_token)
    
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    print("\nTesting Announcements...")
    
    # Test announcements list
    response = client.get('/api/announcements/')
    if response.status_code == 200:
        data = response.json()
        print(f"[SUCCESS] Announcements list: {len(data.get('announcements', []))} announcements")
    else:
        print(f"[ERROR] Announcements list failed: {response.status_code}")
    
    # Test create announcement
    announcement_data = {
        'title': 'Test Announcement',
        'content': 'This is a test announcement from admin.',
        'priority': 'high'
    }
    response = client.post('/api/announcements/', announcement_data)
    if response.status_code == 201:
        data = response.json()
        print(f"[SUCCESS] Created announcement: {data.get('announcement', {}).get('title')}")
        announcement_id = data.get('announcement', {}).get('id')
        
        # Test announcement detail
        if announcement_id:
            response = client.get(f'/api/announcements/{announcement_id}/')
            if response.status_code == 200:
                print("[SUCCESS] Retrieved announcement details")
            else:
                print(f"[ERROR] Announcement details failed: {response.status_code}")
    else:
        print(f"[ERROR] Create announcement failed: {response.status_code}")
        print(response.json())
    
    print("\nTesting Registered Members...")
    
    # Test registered members list
    response = client.get('/api/admin/members/')
    if response.status_code == 200:
        data = response.json()
        print(f"[SUCCESS] Members list: {data.get('total_count')} members")
        print(f"Active: {data.get('active_members')}, Approved: {data.get('approved_members')}")
        
        # Test member details for first member
        members = data.get('members', [])
        if members:
            first_member_id = members[0]['id']
            response = client.get(f'/api/admin/members/{first_member_id}/')
            if response.status_code == 200:
                member_data = response.json()
                member = member_data.get('member', {})
                stats = member_data.get('statistics', {})
                print(f"[SUCCESS] Member details: {member.get('username')}")
                print(f"Applications: {stats.get('total_applications')}, Payments: {stats.get('total_payments')}")
            else:
                print(f"[ERROR] Member details failed: {response.status_code}")
    else:
        print(f"[ERROR] Members list failed: {response.status_code}")
        print(response.json())
    
    print("\nAnnouncements and Members Test Complete!")

if __name__ == '__main__':
    test_announcements_and_members()