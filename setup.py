"""
Setup script for NJA PLATFORM
Run this script to initialize the project
"""

import os
import sys
import subprocess


def run_command(command):
    """Run a shell command"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error running: {command}")
        print(f"  {e.stderr}")
        return False


def main():
    print("=" * 60)
    print("NJA PLATFORM Setup")
    print("=" * 60)
    print()
    
    # Check if Django is installed
    try:
        import django
        print(f"✓ Django is installed (version {django.get_version()})")
    except ImportError:
        print("✗ Django is not installed")
        print("  Installing dependencies...")
        if not run_command("pip install -r requirements.txt"):
            print("\nFailed to install dependencies. Please install manually:")
            print("  pip install -r requirements.txt")
            return
        print()
    
    # Run migrations
    print("Running database migrations...")
    if not run_command("python manage.py makemigrations"):
        print("Warning: Some migrations may have failed")
    if not run_command("python manage.py migrate"):
        print("Error: Migration failed")
        return
    print()
    
    # Create superuser prompt
    print("=" * 60)
    print("Next steps:")
    print("1. Create a superuser account:")
    print("   python manage.py createsuperuser")
    print()
    print("2. Run the development server:")
    print("   python manage.py runserver")
    print()
    print("3. Access the platform at:")
    print("   http://127.0.0.1:8000")
    print("=" * 60)


if __name__ == "__main__":
    main()


