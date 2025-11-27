#!/usr/bin/env python
"""
Script to create a superuser for the Django application.
This can be run after deployment to create an admin user.
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nja_platform.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser():
    """Create a superuser interactively"""
    print("=" * 60)
    print("Creating Django Superuser")
    print("=" * 60)
    
    username = input("Username (leave blank to use 'admin'): ").strip() or 'admin'
    email = input("Email address: ").strip()
    
    if User.objects.filter(username=username).exists():
        print(f"Error: User '{username}' already exists!")
        return False
    
    while True:
        password = input("Password: ").strip()
        if len(password) < 8:
            print("Password must be at least 8 characters long. Try again.")
            continue
        password_confirm = input("Password (again): ").strip()
        if password != password_confirm:
            print("Passwords don't match. Try again.")
            continue
        break
    
    try:
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"\n✓ Superuser '{username}' created successfully!")
        return True
    except Exception as e:
        print(f"\n✗ Error creating superuser: {e}")
        return False

if __name__ == '__main__':
    create_superuser()

