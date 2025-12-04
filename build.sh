#!/usr/bin/env bash
set -e

echo "=== Build Starting ==="
echo "PWD: $(pwd)"
echo ""

# Find project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Changed to: $(pwd)"
echo ""

# Upgrade pip
pip install --upgrade pip

# Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "ERROR: requirements.txt not found!"
    echo "Current directory: $(pwd)"
    echo "Files:"
    ls -la
    exit 1
fi

# Verify Django
python -c "import django; print('Django OK')"

# Collect static
python manage.py collectstatic --no-input

# Migrate
python manage.py migrate --no-input || echo "Migration warning (will retry at startup)"

echo "=== Build Complete ==="
