import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

# Get or create admin user
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@pamoja.com',
        'is_staff': True,
        'is_superuser': True
    }
)

if created:
    admin_user.set_password('admin123')
    admin_user.save()

# Get or create token
token, created = Token.objects.get_or_create(user=admin_user)

print(f"Admin user: {admin_user.username}")
print(f"Token: {token.key}")

# Test endpoints
base_url = 'http://localhost:8000/api/admin'
headers = {
    'Authorization': f'Token {token.key}',
    'Content-Type': 'application/json'
}

endpoints = [
    '/users/',
    '/applications/',
    '/claims/',
    '/payments/',
    '/contact/'
]

print("\nTesting admin endpoints:")
for endpoint in endpoints:
    try:
        response = requests.get(f"{base_url}{endpoint}", headers=headers)
        print(f"{endpoint}: Status {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Data count: {len(data) if isinstance(data, list) else 'N/A'}")
        else:
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"{endpoint}: Connection error - {e}")