#!/bin/bash

echo "========================================="
echo "CleanTrack Setup Script"
echo "========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created. Please edit it with your API keys."
    echo ""
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create directories
echo "Creating necessary directories..."
mkdir -p logs media static staticfiles
echo "✓ Directories created"
echo ""

# Run migrations
echo "Running database migrations..."
python manage.py migrate
echo "✓ Migrations complete"
echo ""

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "✓ Static files collected"
echo ""

# Create superuser
echo ""
echo "Would you like to create a superuser now? (y/n)"
read -r create_superuser

if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys (Stripe, Resend)"
echo "2. Start the development server: python manage.py runserver"
echo "3. Start Celery worker: celery -A cleantrack worker -l info"
echo "4. Start Celery beat: celery -A cleantrack beat -l info"
echo "5. Visit http://localhost:8000"
echo "6. Access admin at http://localhost:8000/admin"
echo ""
echo "For Docker setup, run: docker-compose up --build"
echo ""
