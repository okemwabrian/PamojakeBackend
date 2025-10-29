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
from applications.models import Application

User = get_user_model()

def test_application_details():
    print("Testing Admin Application Details...")
    
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
    
    # Get first application
    application = Application.objects.first()
    if not application:
        print("[ERROR] No applications found")
        return
    
    print(f"Testing application ID: {application.id}")
    
    # Test application details endpoint
    response = client.get(f'/api/admin/crud/applications/{application.id}/')
    
    if response.status_code == 200:
        data = response.json()
        app_data = data.get('application', {})
        
        print("[SUCCESS] Application details retrieved")
        print(f"Application ID: {app_data.get('id')}")
        print(f"User: {app_data.get('user')}")
        print(f"Name: {app_data.get('first_name')} {app_data.get('last_name')}")
        print(f"Email: {app_data.get('email')}")
        print(f"Phone: {app_data.get('phone')}")
        print(f"Address: {app_data.get('address')}")
        print(f"City: {app_data.get('city')}")
        print(f"State: {app_data.get('state')}")
        print(f"Emergency Contact: {app_data.get('emergency_name')}")
        print(f"Membership Type: {app_data.get('membership_type')}")
        print(f"Status: {app_data.get('status')}")
        
        if app_data.get('membership_type') == 'double':
            print(f"Spouse: {app_data.get('spouse_first_name')} {app_data.get('spouse_last_name')}")
            print(f"Spouse Email: {app_data.get('spouse_email')}")
        
        print(f"Children Info: {len(app_data.get('children_info', []))} children")
        print(f"Documents: ID={bool(app_data.get('id_document'))}")
        
    else:
        print(f"[ERROR] Failed to get application details: {response.status_code}")
        print(response.json())

if __name__ == '__main__':
    test_application_details()