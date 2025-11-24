# CleanTrack - Quick Start Guide

Get CleanTrack up and running in 5 minutes!

## Option 1: Docker (Recommended)

The fastest way to get started:

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Edit .env and add your API keys (optional for testing)
nano .env

# 3. Start all services
docker-compose up --build

# 4. In a new terminal, run migrations
docker-compose exec web python manage.py migrate

# 5. Create superuser
docker-compose exec web python manage.py createsuperuser

# 6. Visit http://localhost:8000
```

That's it! CleanTrack is now running with PostgreSQL, Redis, Celery, and all services.

## Option 2: Local Development

If you prefer running locally:

```bash
# 1. Run the setup script
chmod +x setup.sh
./setup.sh

# 2. Activate virtual environment
source venv/bin/activate

# 3. Start the server
python manage.py runserver

# 4. In separate terminals, start Celery (optional for full functionality)
celery -A cleantrack worker -l info
celery -A cleantrack beat -l info

# 5. Visit http://localhost:8000
```

## First Steps

1. **Access Admin Panel**: http://localhost:8000/admin
   - Login with your superuser credentials

2. **Create an Account**:
   - Go to Accounts → Add Account
   - Set name, slug, owner, and plan

3. **Create a Location**:
   - Go to Locations → Add Location
   - Associate with your account

4. **Add Equipment Type**:
   - Go to Equipment Types → Add Equipment Type
   - Example: "Ultrasound Machine", cleaning frequency: 24 hours

5. **Add Cleaning Protocol**:
   - Go to Cleaning Protocols → Add Protocol
   - Define steps, chemicals, and duration

6. **Register Equipment**:
   - Go to Equipment → Add Equipment
   - Link to location, type, and protocol

7. **Log a Cleaning**:
   - Go to Cleaning Logs → Add Cleaning Log
   - Record the cleaning activity

8. **View Compliance**:
   - Check Compliance Alerts for any overdue cleanings
   - Generate Audit Reports

## Testing Alerts

To test the automated alert system:

```bash
# Manually trigger alert check
docker-compose exec web python manage.py shell
>>> from compliance.tasks import check_overdue_cleanings
>>> check_overdue_cleanings()
```

## Sample Data (Optional)

Create sample data for testing:

```bash
docker-compose exec web python manage.py shell
```

```python
from accounts.models import User, Account, Location
from equipment.models import EquipmentType, Equipment
from django.utils import timezone

# Create test account
user = User.objects.create_user(email='test@cleantrack.app', password='test123')
account = Account.objects.create(
    name='Test Hospital',
    slug='test-hospital',
    owner=user,
    plan='trial'
)

# Create location
location = Location.objects.create(
    account=account,
    name='Main Building',
    city='San Francisco',
    state='CA'
)

# Create equipment type
eq_type = EquipmentType.objects.create(
    name='Ultrasound Machine',
    default_cleaning_frequency=24,
    requires_fda_compliance=True
)

# Create equipment
equipment = Equipment.objects.create(
    location=location,
    equipment_type=eq_type,
    name='GE Ultrasound Unit 1',
    serial_number='US-001',
    cleaning_frequency=24
)

print("Sample data created successfully!")
```

## Environment Variables

### Required for Production:
- `STRIPE_PUBLIC_KEY` - Stripe publishable key
- `STRIPE_SECRET_KEY` - Stripe secret key
- `RESEND_API_KEY` - Resend API key for emails

### Optional for Development:
- `DEBUG=True` (default)
- `SECRET_KEY` (auto-generated for dev)

## Troubleshooting

### Database Connection Error
```bash
# Reset database (Docker)
docker-compose down -v
docker-compose up --build
docker-compose exec web python manage.py migrate
```

### Celery Not Running
```bash
# Check Celery worker status (Docker)
docker-compose logs celery

# Restart Celery
docker-compose restart celery celery-beat
```

### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput
```

### Port Already in Use
```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- Review the Product Requirements Document (PRD) for feature details

## Support

For issues or questions:
- Email: support@cleantrack.app
- GitHub: Create an issue

---

Happy tracking!
