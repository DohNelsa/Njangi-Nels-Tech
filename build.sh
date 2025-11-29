#!/usr/bin/env bash
# Build script for Render deployment

set -e  # Exit on error

echo "=========================================="
echo "Starting build process..."
echo "=========================================="

# Upgrade pip
echo "Step 1: Upgrading pip..."
pip install --upgrade pip || echo "Warning: pip upgrade failed, continuing..."

# Install dependencies
echo "Step 2: Installing dependencies from requirements.txt..."
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt not found!"
    exit 1
fi
pip install -r requirements.txt

# Verify Django installation
echo "Step 3: Verifying Django installation..."
python -c "import django; print(f'Django {django.get_version()} installed')" || {
    echo "ERROR: Django not installed properly!"
    exit 1
}

# Collect static files
echo "Step 4: Collecting static files..."
python manage.py collectstatic --no-input --clear || {
    echo "ERROR: collectstatic failed!"
    exit 1
}

# Run migrations (optional - will also run at startup if this fails)
echo "Step 5: Running database migrations..."
python manage.py migrate --no-input || {
    echo "WARNING: Migrations failed (database may not be ready)."
    echo "Migrations will be attempted again at application startup."
}

echo "=========================================="
echo "Build completed successfully!"
echo "=========================================="
