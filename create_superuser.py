#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from accounts.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@pamoja.com', 'admin123')
    print("Superuser created successfully!")
else:
    print("Superuser already exists!")