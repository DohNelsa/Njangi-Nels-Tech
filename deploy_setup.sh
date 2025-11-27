#!/usr/bin/env bash
# Deployment setup script for Render
# This script helps prepare and verify the deployment

set -o errexit  # Exit on error

echo "=========================================="
echo "NJA PLATFORM - Deployment Setup"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "Error: manage.py not found. Please run this script from the project root."
    exit 1
fi

echo "✓ Project root detected"
echo ""

# Check Python version
echo "Checking Python version..."
python --version
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠ Warning: Virtual environment not detected"
    echo "  It's recommended to use a virtual environment"
else
    echo "✓ Virtual environment detected: $VIRTUAL_ENV"
fi
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo ""

# Install dependencies
echo "Installing dependencies from requirements.txt..."
if [ ! -f "requirements.txt" ]; then
    echo "✗ Error: requirements.txt not found!"
    exit 1
fi
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Check for migrations
echo "Checking for pending migrations..."
python manage.py makemigrations --check --dry-run
echo ""

# Collect static files (dry run check)
echo "Checking static files configuration..."
python manage.py collectstatic --no-input --dry-run
echo ""

# Verify settings
echo "Verifying Django settings..."
python manage.py check --deploy
echo ""

echo "=========================================="
echo "Setup complete! ✓"
echo "=========================================="
echo ""
echo "Next steps for Render deployment:"
echo "1. Push your code to GitHub/GitLab"
echo "2. Connect your repository to Render"
echo "3. Create a PostgreSQL database on Render"
echo "4. Set environment variables in Render:"
echo "   - SECRET_KEY (generate with: python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\")"
echo "   - DEBUG=False"
echo "   - ALLOWED_HOSTS=your-app.onrender.com"
echo "5. Set build command: ./build.sh"
echo "6. Set start command: gunicorn nja_platform.wsgi"
echo "7. After deployment, create superuser using: python create_superuser.py"
echo ""

