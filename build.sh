#!/usr/bin/env bash
set -e

echo "=== Build Starting ==="
echo "PWD: $(pwd)"
echo "Files:"
ls -la | head -20
echo ""

# Find project root (where manage.py is)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Changed to: $(pwd)"
echo "Looking for requirements.txt..."

# Try multiple locations
if [ -f "requirements.txt" ]; then
    echo "Found requirements.txt in current directory"
    REQ_FILE="requirements.txt"
elif [ -f "./requirements.txt" ]; then
    echo "Found requirements.txt with ./"
    REQ_FILE="./requirements.txt"
else
    echo "ERROR: requirements.txt not found!"
    echo "Current directory: $(pwd)"
    echo "Files here:"
    ls -la
    exit 1
fi

echo "Using: $REQ_FILE"
echo ""

# Install dependencies
pip install --upgrade pip
pip install -r "$REQ_FILE"

# Verify Django
python -c "import django; print('Django OK')"

# Collect static
python manage.py collectstatic --no-input

# Migrate
python manage.py migrate --no-input || echo "Migration warning (will retry at startup)"

echo "=== Build Complete ==="
