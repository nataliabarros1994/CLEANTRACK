# 🚀 CleanTrack - START HERE

## ✅ Setup Complete!

Your CleanTrack project is ready to run with a **simplified Docker configuration**.

---

## 📋 What You Have

### Docker Configuration (2 Services)
```
✅ Dockerfile          - Python 3.11-slim with 12 dependencies
✅ docker-compose.yml  - web (Django) + db (PostgreSQL)
✅ .env               - Environment variables configured
```

### Dependencies (12 Packages)
```
✅ Django 5.0.6              ✅ dj-stripe 2.12.0
✅ PostgreSQL (psycopg2)     ✅ resend 2.3.0
✅ django-allauth            ✅ Pillow 10.3.0
✅ djangorestframework       ✅ python-decouple
✅ django-cors-headers       ✅ python-dotenv
✅ whitenoise                ✅ stripe 10.0.0
```

### Django Apps
```
✅ accounts/     - Users, Accounts, Locations
✅ equipment/    - Equipment, Protocols, Types
✅ compliance/   - CleaningLog, Alerts, Reports
✅ billing/      - Stripe integration
```

---

## 🎯 Quick Start (3 Commands)

### 1. Start Services
```bash
cd /home/nataliabarros1994/Desktop/CleanTrack
docker-compose up --build
```
Wait for: "Starting development server at http://0.0.0.0:8000/"

### 2. Setup Database (New Terminal)
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py create_demo_data
```

### 3. Access Application
```
🌍 Homepage:  http://localhost:8000
🔐 Admin:     http://localhost:8000/admin
```

**Demo Login:**
- Email: `demo.admin@cleantrack.app`
- Password: `demo123`

---

## 🔧 Configuration Details

### Database Connection
```
Host:     db (inside Docker) / localhost (from host)
Port:     5432
Database: cleantrack
User:     cleantrack_user
Password: secure_password_123
URL:      postgres://cleantrack_user:secure_password_123@db:5432/cleantrack
```

### Environment Variables (.env)
```bash
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://cleantrack_user:secure_password_123@db:5432/cleantrack
REDIS_URL=redis://localhost:6379/0
STRIPE_PUBLIC_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here
RESEND_API_KEY=re_your_api_key_here
```

---

## 📚 Documentation Files

| File | Description |
|------|-------------|
| **START_HERE.md** | This file - start here! |
| **QUICK_START.txt** | Quick reference commands |
| **DEPENDENCIES.md** | Package overview & versions |
| **DOCKER_SETUP_NOTE.md** | Simplified vs full setup |
| **PROJECT_STATUS.md** | Complete feature list |
| **README.md** | Full technical documentation |
| **LEIAME_PT.md** | Portuguese documentation |
| **ACESSO_RAPIDO.md** | Portuguese quick start |

---

## 🛠️ Common Commands

### Docker Operations
```bash
# Start project
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop project
docker-compose down

# Rebuild
docker-compose up --build

# Reset everything (DELETES DATA!)
docker-compose down -v
docker-compose up --build
```

### Django Management
```bash
# Run any Django command
docker-compose exec web python manage.py [command]

# Examples:
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py create_demo_data
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py showmigrations
```

### Database Access
```bash
# Access PostgreSQL shell
docker-compose exec db psql -U cleantrack_user -d cleantrack

# Inside psql:
\dt                    # List tables
\d accounts_user       # Describe table
SELECT * FROM accounts_account;
\q                     # Quit
```

---

## ✅ What Works (Simplified Setup)

### Core Features
- ✅ Django 5.0.6 web application
- ✅ PostgreSQL 15 database
- ✅ User authentication (email-based)
- ✅ Complete admin interface
- ✅ Multi-tenant architecture (Account → Location → Equipment)
- ✅ All CRUD operations
- ✅ Image uploads (equipment photos, cleaning evidence)
- ✅ Static file serving (WhiteNoise)
- ✅ CORS support for API calls

### Integrations
- ✅ Stripe webhook handling (subscription management)
- ✅ Email sending via Resend
- ✅ REST API endpoints (Django REST Framework)

### Data Models (11 Models)
- ✅ User, Account, Location, AccountMembership
- ✅ EquipmentType, CleaningProtocol, Equipment
- ✅ CleaningLog, ComplianceAlert, AuditReport

---

## ⚠️ What's Disabled (No Celery/Redis)

Without background task services:
- ❌ Automated compliance checking (every 30 min)
- ❌ Scheduled email notifications
- ❌ Daily/weekly report generation
- ❌ Subscription monitoring tasks
- ❌ PDF/Excel export (no reportlab/openpyxl)

**To enable:** See `DOCKER_SETUP_NOTE.md` for full 5-service configuration

---

## 🎯 Next Steps

### 1. Verify Installation
```bash
# Check all services are running
docker-compose ps

# Should show:
# cleantrack_web_1    Up   0.0.0.0:8000->8000/tcp
# cleantrack_db_1     Up   0.0.0.0:5432->5432/tcp
```

### 2. Explore Admin Interface
```
1. Go to http://localhost:8000/admin
2. Login with superuser credentials
3. Explore: Accounts, Equipment, Compliance, Billing
4. View demo data (if created)
```

### 3. Test Stripe Webhook (Optional)
```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe  # Mac
# or download from: https://stripe.com/docs/stripe-cli

# Login
stripe login

# Forward webhooks to local
stripe listen --forward-to localhost:8000/billing/webhooks/stripe/

# Trigger test events
stripe trigger customer.subscription.created
stripe trigger invoice.payment_succeeded
```

### 4. Test Email Sending (Optional)
```python
# Django shell
docker-compose exec web python manage.py shell

# Send test email
from cleantrack.email_service import send_template_email
send_template_email(
    to_email='your@email.com',
    subject='CleanTrack Test',
    template_name='emails/welcome.html',
    context={'user_name': 'Test User', 'account_name': 'Test Org'}
)
```

---

## 🔍 Troubleshooting

### Port 8000 Already in Use
```bash
# Find and kill process
sudo lsof -ti:8000 | xargs kill -9

# Or change port in docker-compose.yml:
ports:
  - "8001:8000"  # Use port 8001 instead
```

### Database Connection Error
```bash
# Check database is running
docker-compose logs db

# Restart database
docker-compose restart db

# Check connection from web container
docker-compose exec web python manage.py dbshell
```

### Module Import Errors
```bash
# Rebuild with no cache
docker-compose build --no-cache

# Verify requirements installed
docker-compose exec web pip list
```

### Reset Everything
```bash
# Nuclear option - starts fresh (DELETES ALL DATA!)
docker-compose down -v
docker-compose build --no-cache
docker-compose up --build

# Then setup again:
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py create_demo_data
```

---

## 📊 Demo Data Included

After running `create_demo_data`, you'll have:

**Users (2):**
- demo.admin@cleantrack.app (Admin)
- demo.technician@cleantrack.app (Technician)

**Account (1):**
- Demo Hospital

**Locations (2):**
- Main Building
- ICU Wing

**Equipment (4):**
- GE Ultrasound Unit 1
- Philips Ventilator 1
- Philips Ventilator 2
- Siemens X-Ray Machine 1

**Cleaning Logs (2):**
- Recent cleaning records with timestamps

**Alerts (3):**
- Overdue cleaning alert
- Due soon alert
- Never cleaned alert

---

## 🎨 Tech Stack Summary

```
Frontend:  Django Templates (HTML/CSS/JS)
Backend:   Django 5.0.6 (Python 3.11)
Database:  PostgreSQL 15
Cache:     (Disabled - Redis removed)
Tasks:     (Disabled - Celery removed)
Email:     Resend API
Payments:  Stripe + dj-stripe
Auth:      django-allauth (email-based)
API:       Django REST Framework
Static:    WhiteNoise
Container: Docker + Docker Compose
```

---

## 🌟 Features Highlights

### Multi-Tenant Architecture
- Accounts can have multiple locations
- Locations can have multiple equipment items
- Role-based permissions (Admin, Manager, Technician, Auditor)
- Data isolation between accounts

### Equipment Management
- Equipment types with default cleaning protocols
- Serial numbers, QR codes, photos
- Cleaning frequency tracking
- Real-time compliance status

### Compliance Tracking
- Manual cleaning log entry
- Photo evidence support
- Protocol compliance validation
- Alert generation (overdue, due soon, never cleaned)
- Alert workflow (Active → Acknowledged → Resolved)

### Subscription Management
- Stripe integration for payments
- Plan-based limits (Trial: 5 locations, Standard: 50 locations)
- Webhook handling for subscription events
- Automatic status updates

---

## 📞 Support

For issues, check:
1. **QUICK_START.txt** - Command reference
2. **DOCKER_SETUP_NOTE.md** - Setup details
3. **DEPENDENCIES.md** - Package info
4. **README.md** - Full documentation

---

## ✨ Ready to Start!

Your CleanTrack GRC platform is ready for medical equipment compliance tracking!

**Run this now:**
```bash
docker-compose up --build
```

Then access: **http://localhost:8000** 🚀

---

**CleanTrack** - Ensuring medical equipment compliance, one cleaning at a time.
