# Docker Setup - Simplified Configuration

## Current Setup (Simplified)

Your `docker-compose.yml` now has a **simplified 2-service setup**:

```yaml
services:
  web:       # Django application (port 8000)
  db:        # PostgreSQL 15
```

### ✅ What Works
- Django web application
- PostgreSQL database
- Basic CRUD operations
- Admin interface
- User authentication
- All models (Equipment, CleaningLog, Alerts, etc.)

### ⚠️ What's Disabled (No Redis/Celery)

Without Redis and Celery services, these features won't work:
- ❌ **Automated compliance alerts** (no background task checking)
- ❌ **Daily/weekly reports generation** (no scheduled tasks)
- ❌ **Email notifications** (no async email sending)
- ❌ **Subscription expiration checks** (no scheduled monitoring)
- ❌ **Celery tasks** (check_overdue_cleanings, generate_daily_reports, etc.)

---

## Quick Start (Simplified)

```bash
# 1. Start services
docker-compose up --build

# 2. In another terminal, run migrations
docker-compose exec web python manage.py migrate

# 3. Create superuser
docker-compose exec web python manage.py createsuperuser

# 4. (Optional) Create demo data
docker-compose exec web python manage.py create_demo_data

# 5. Access the application
# http://localhost:8000
# http://localhost:8000/admin
```

---

## Full Setup (If You Need Background Tasks)

If you want the full functionality with background tasks, use this `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=cleantrack
      - POSTGRES_USER=cleantrack_user
      - POSTGRES_PASSWORD=secure_password_123
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  celery:
    build: .
    command: celery -A cleantrack worker -l info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis

  celery-beat:
    build: .
    command: celery -A cleantrack beat -l info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

Then update `.env`:
```bash
DATABASE_URL=postgres://cleantrack_user:secure_password_123@db:5432/cleantrack
REDIS_URL=redis://redis:6379/0
```

---

## Recommendation

**For Development/Testing:**
- Use the **simplified setup** (current) - faster startup, less resources

**For Production/Full Features:**
- Use the **full setup** with Redis + Celery - enables all background tasks

---

## Database Credentials

```
Host: db (inside Docker) or localhost (from host)
Port: 5432
Database: cleantrack
User: cleantrack_user
Password: secure_password_123
```

**Connection String:**
```
postgres://cleantrack_user:secure_password_123@db:5432/cleantrack
```

---

## Switch Between Setups

### To Full Setup:
1. Replace `docker-compose.yml` with the full version above
2. Update `.env` with Redis URL
3. Run: `docker-compose up --build`

### To Simplified Setup:
1. Keep current `docker-compose.yml`
2. Remove Redis from `.env` (optional)
3. Run: `docker-compose up --build`

---

Your simplified setup is ready to use! 🚀
