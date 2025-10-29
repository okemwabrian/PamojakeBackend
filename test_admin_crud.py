#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def test_admin_crud_endpoints():
    print("Testing Admin CRUD System...")
    
    # Create test admin user
    admin_user, created = User.objects.get_or_create(
        username='admin_test',
        defaults={
            'email': 'admin@test.com',
            'is_staff': True,
            'is_superuser': True,
            'first_name': 'Admin',
            'last_name': 'User'
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("[SUCCESS] Created admin test user")
    
    # Get JWT token
    refresh = RefreshToken.for_user(admin_user)
    access_token = str(refresh.access_token)
    
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    print("\nTesting Dashboard Stats...")
    response = client.get('/api/admin/dashboard/stats/')
    if response.status_code == 200:
        data = response.json()
        print(f"[SUCCESS] Dashboard stats: {data['stats']['users']['total']} users, {data['stats']['applications']['total']} applications")
    else:
        print(f"[ERROR] Dashboard stats failed: {response.status_code}")
    
    print("\nTesting Applications CRUD...")
    response = client.get('/api/admin/crud/applications/')
    if response.status_code == 200:
        data = response.json()
        print(f"[SUCCESS] Applications list: {len(data.get('applications', []))} applications")
    else:
        print(f"[ERROR] Applications list failed: {response.status_code}")
    
    print("\nTesting Payments CRUD...")
    response = client.get('/api/admin/crud/payments/')
    if response.status_code == 200:
        data = response.json()
        print(f"[SUCCESS] Payments list: {len(data.get('payments', []))} payments")
    else:
        print(f"[ERROR] Payments list failed: {response.status_code}")
    
    print("\nTesting Claims CRUD...")
    response = client.get('/api/admin/crud/claims/')
    if response.status_code == 200:
        data = response.json()
        print(f"[SUCCESS] Claims list: {len(data.get('claims', []))} claims")
    else:
        print(f"[ERROR] Claims list failed: {response.status_code}")
    
    print("\nTesting Shares CRUD...")
    response = client.get('/api/admin/crud/shares/')
    if response.status_code == 200:
        data = response.json()
        print(f"[SUCCESS] Shares list: {len(data.get('shares', []))} shares")
    else:
        print(f"[ERROR] Shares list failed: {response.status_code}")
    
    print("\nTesting User Activities...")
    response = client.get('/api/admin/activities/')
    if response.status_code == 200:
        data = response.json()
        print(f"[SUCCESS] Activities list: {len(data.get('activities', []))} activities")
    else:
        print(f"[ERROR] Activities list failed: {response.status_code}")
    
    print("\nAdmin CRUD System Test Complete!")

if __name__ == '__main__':
    test_admin_crud_endpoints()