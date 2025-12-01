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

# Install dependencies directly (no requirements.txt needed)
echo "Installing dependencies..."
pip install Django==5.1.7
pip install asgiref==3.8.1
pip install sqlparse==0.5.3
pip install django-crispy-forms==2.3
pip install crispy-bootstrap5==2024.2
pip install Pillow==10.4.0
pip install openpyxl==3.1.5
pip install reportlab==4.3.1
pip install gunicorn==21.2.0
pip install whitenoise==6.11.0
pip install psycopg2-binary==2.9.9
pip install python-dotenv==1.1.1
pip install dj-database-url==2.1.0

# Verify Django
python -c "import django; print('Django OK')"

# Collect static
python manage.py collectstatic --no-input

# Migrate
python manage.py migrate --no-input || echo "Migration warning (will retry at startup)"

echo "=== Build Complete ==="
