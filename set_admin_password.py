import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('admin123')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    print("Admin password set to 'admin123'")
except User.DoesNotExist:
    admin_user = User.objects.create_superuser('admin', 'admin@pamoja.com', 'admin123')
    print("Admin user created with password 'admin123'")