#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from django.urls import reverse
from rest_framework.test import APIClient

# Test the activation fee URL
try:
    # DRF automatically creates URLs with underscores for actions
    url = reverse('payment-activation-fee')
    print(f"Activation fee URL: {url}")
except:
    print("URL with hyphen not found")

try:
    # Try with underscore
    from django.urls import resolve
    from django.conf import settings
    from django.urls import get_resolver
    
    resolver = get_resolver()
    print("Available payment URLs:")
    for pattern in resolver.url_patterns:
        if 'payments' in str(pattern.pattern):
            print(f"  {pattern.pattern}")
            
except Exception as e:
    print(f"Error: {e}")

print("\nTesting direct endpoint access...")
client = APIClient()
response = client.options('/api/payments/')
print(f"OPTIONS /api/payments/: {response.status_code}")

# Check if activation_fee action exists
response = client.options('/api/payments/activation_fee/')
print(f"OPTIONS /api/payments/activation_fee/: {response.status_code}")