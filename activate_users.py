#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamojabackend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def activate_all_users():
    print("Activating all users...")
    
    # Get all inactive users
    inactive_users = User.objects.filter(is_active=False)
    count = inactive_users.count()
    
    if count == 0:
        print("All users are already active!")
        return
    
    # Activate all users
    inactive_users.update(is_active=True)
    
    print(f"Activated {count} users:")
    for user in User.objects.all():
        print(f"- {user.username}: Active={user.is_active}, Staff={user.is_staff}")
    
    print("\nAll users are now active and can login!")

if __name__ == '__main__':
    activate_all_users()