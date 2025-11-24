#!/usr/bin/env bash
# Build script for production deployment (Render.com compatible)
set -o errexit  # Exit on error

echo "🚀 CleanTrack Production Build Starting..."
echo "=========================================="

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create logs directory if it doesn't exist
echo "📁 Creating logs directory..."
mkdir -p logs

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --no-input

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --no-input

# Create default Site object if it doesn't exist
echo "🌐 Configuring Django sites framework..."
python manage.py shell <<EOF
from django.contrib.sites.models import Site
site, created = Site.objects.get_or_create(id=1)
if created:
    site.domain = 'cleantrack.com'
    site.name = 'CleanTrack'
    site.save()
    print('✅ Site object created')
else:
    print('ℹ️  Site object already exists')
EOF

echo "=========================================="
echo "✅ Build completed successfully!"
echo "=========================================="
