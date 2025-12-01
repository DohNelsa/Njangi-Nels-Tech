#!/usr/bin/env bash
# Build script for Render deployment

set -e  # Exit on error

echo "=========================================="
echo "Starting build process..."
echo "=========================================="

# Debug: Show current directory and files
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -la
echo ""

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "ERROR: manage.py not found in current directory!"
    echo "Current directory: $(pwd)"
    exit 1
fi

# Check for requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt not found!"
    echo "Current directory: $(pwd)"
    echo "Looking for requirements.txt in: $(pwd)/requirements.txt"
    echo "Files in directory:"
    ls -la
    exit 1
fi

echo "✓ Found requirements.txt"
echo ""

# Upgrade pip
echo "Step 1: Upgrading pip..."
pip install --upgrade pip || echo "Warning: pip upgrade failed, continuing..."

# Install dependencies
echo "Step 2: Installing dependencies from requirements.txt..."
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
