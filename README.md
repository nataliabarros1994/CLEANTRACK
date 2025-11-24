# 🧹 CleanTrack

**Healthcare Compliance Automation Platform**

CleanTrack is a modern SaaS platform that automates equipment cleaning compliance tracking for healthcare facilities. Replace paper logs with QR codes, mobile forms, and real-time dashboards to eliminate $10k-$500k regulatory fines.

[![Django](https://img.shields.io/badge/Django-5.0.6-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)]()

---

## 🎯 Problem & Solution

### The Problem
- 6,000+ U.S. healthcare facilities track equipment cleaning on paper/Excel
- A single missed cleaning log = $10k–$500k in regulatory fines (FDA, Joint Commission)
- Manual processes create audit anxiety and operational inefficiency
- No real-time visibility into compliance status

### The Solution
CleanTrack provides:
- **15-second logging**: QR code scan → photo → submit (no login required)
- **Real-time compliance**: Live dashboard with compliance metrics
- **Audit-ready reports**: One-click PDF generation
- **Proactive alerts**: Email notifications before inspections
- **Multi-tenant**: Isolated data per facility with granular permissions

---

## 🚀 Key Features

### 📱 Mobile-First QR System
- Equipment-specific QR codes (permanent or expirable tokens)
- Mobile-optimized forms (iOS/Android)
- Camera integration for photo evidence
- Offline-capable with sync on reconnect

### 📊 Real-Time Dashboard
- Compliance rate tracking (daily/weekly/monthly)
- Overdue equipment alerts
- Activity feed with recent cleanings
- Equipment usage statistics

### 🖨️ Thermal Printer Integration
- Direct printing to Brother, Zebra, DYMO printers
- Custom label templates (2.4" x 1.2" standard)
- Batch printing for multiple equipment
- QR code + equipment details on label

### 🔐 Multi-Tenant Architecture
- Complete data isolation per facility
- Role-based access control (RBAC)
- Facility Admin, Technician, Super Admin roles
- Manage multiple facilities from single account

### 📧 Automated Notifications
- Overdue equipment alerts (email)
- Weekly compliance reports
- Scheduled cleaning reminders
- Audit preparation checklists

### 💳 Stripe Integration
- Subscription billing ($100-$300/month)
- Usage-based pricing (per equipment)
- Webhook support for payment events
- Customer portal for self-service

### 🔒 Security & Compliance
- No PHI (Protected Health Information) storage
- HIPAA-safe by design
- Expirable access tokens (5-minute default)
- Audit trail for all actions
- HTTPS enforced in production

---

## 🏗️ Architecture

### Tech Stack

**Backend:**
- Django 5.0.6 (Python 3.10+)
- PostgreSQL 15+ (production)
- SQLite (development)
- Django REST Framework (API)

**Frontend:**
- Tailwind CSS 3.x (responsive design)
- Alpine.js (lightweight interactivity)
- HTMX (dynamic updates)
- Font Awesome icons

**Infrastructure:**
- Gunicorn (WSGI server)
- WhiteNoise (static files)
- Docker support
- Render.com ready (PaaS deployment)

**Integrations:**
- Stripe (payments via dj-stripe)
- Resend (transactional email)
- QRCode (label generation)
- ReportLab (PDF generation)

### Project Structure

```
CleanTrack/
├── apps/
│   ├── accounts/          # User authentication & management
│   ├── billing/           # Stripe subscriptions & webhooks
│   ├── cleaning_logs/     # Cleaning record tracking
│   ├── documentation/     # Feature catalog & guides
│   ├── equipment/         # Equipment management & QR codes
│   ├── facilities/        # Multi-tenant facility management
│   └── notifications/     # Email alerts & reports
├── cleantrack/
│   ├── settings.py        # Development settings
│   ├── settings_production.py  # Production settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI entry point
├── templates/
│   ├── base/              # Base responsive templates
│   ├── cleaning_logs/     # Cleaning form templates
│   ├── equipment/         # Equipment management UI
│   └── admin/             # Django admin customizations
├── static/
│   ├── css/               # Custom CSS (responsive.css)
│   ├── js/                # JavaScript utilities
│   └── images/            # Static images
├── qr_codes/              # Generated QR code images
├── media/                 # User uploads (cleaning photos)
├── docs/                  # Additional documentation
├── requirements.txt       # Python dependencies
├── build.sh               # Render deployment script
├── render.yaml            # Render infrastructure config
└── manage.py              # Django management script
```

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- PostgreSQL 15+ (production) or SQLite (development)
- pip (Python package manager)
- virtualenv (recommended)

### Local Development Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/cleantrack.git
cd CleanTrack
```

#### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables
Create `.env` file in project root:

```bash
# Django Core
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DATABASE_URL=sqlite:///db.sqlite3

# Email (Resend API)
RESEND_API_KEY=re_your_api_key_here
DEFAULT_FROM_EMAIL=noreply@cleantrack.com

# Stripe (Test Mode)
STRIPE_TEST_PUBLIC_KEY=pk_test_xxx
STRIPE_TEST_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_LIVE_MODE=False

# Site Configuration
SITE_URL=http://localhost:8000
LANGUAGE_CODE=en-us
TIME_ZONE=America/Sao_Paulo
```

#### 5. Run Migrations
```bash
python manage.py migrate
```

#### 6. Create Superuser
```bash
python manage.py createsuperuser
# Email: admin@cleantrack.com
# Password: (your secure password)
```

#### 7. Create Test Data (Optional)
```bash
python create_test_data.py
```

#### 8. Start Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```

#### 9. Access the Application
- **Admin Panel:** http://localhost:8000/admin/
- **Main Site:** http://localhost:8000/
- **API:** http://localhost:8000/api/

---

## 🚀 Deployment

### Deploy to Render.com (Recommended)

#### One-Click Deploy
1. Push code to GitHub
2. Connect GitHub to Render
3. Use `render.yaml` blueprint for automatic setup
4. Add environment variables from `.env.render`

#### Manual Deploy Steps

**1. Create PostgreSQL Database**
```
Name: cleantrack-db
Region: Oregon (US West)
Plan: Free
```

**2. Create Web Service**
```
Name: cleantrack-api
Environment: Python 3
Build Command: ./build.sh
Start Command: gunicorn cleantrack.wsgi:application
Plan: Free (or Starter for production)
```

**3. Configure Environment Variables**
Copy all variables from `.env.render` to Render Dashboard:
- `DJANGO_SETTINGS_MODULE=cleantrack.settings_production`
- `DEBUG=False`
- `SECRET_KEY` (use "Generate Value")
- `DATABASE_URL` (auto-populated from database)
- `RESEND_API_KEY`
- `STRIPE_TEST_PUBLIC_KEY`
- `STRIPE_TEST_SECRET_KEY`
- etc.

**4. Deploy**
Render will automatically:
- Install dependencies
- Run migrations
- Collect static files
- Start Gunicorn server

**5. Access Your Site**
```
https://cleantrack-api.onrender.com/admin/
```

### Deploy to Other Platforms

**Railway:**
- Use `Procfile`: `web: gunicorn cleantrack.wsgi:application`
- Add PostgreSQL plugin
- Set environment variables

**Fly.io:**
- Use `fly.toml` configuration
- Run `fly deploy`
- Add Postgres cluster

**Heroku:**
- Use `Procfile` and `runtime.txt`
- Add Heroku Postgres addon
- Set config vars

---

## 📚 Documentation

### Core Apps

#### 1. **accounts** - User Management
- Custom User model with email authentication
- Role-based permissions (Facility Admin, Technician, Super Admin)
- Multi-facility management
- User registration and login flows

**Key Models:**
- `User`: Custom user with email as username
- `Account`: Organization/billing entity
- `Profile`: Extended user information

**Key Views:**
- Login/Logout
- User registration
- Profile management
- Password reset

#### 2. **facilities** - Multi-Tenant System
- Facility (tenant) management
- Data isolation per facility
- Facility-level settings
- Equipment inventory per facility

**Key Models:**
- `Facility`: Healthcare facility (hospital, clinic, lab)

**Key Features:**
- Multi-tenant architecture
- Facility switching for admins
- Isolated equipment and logs

#### 3. **equipment** - Equipment Management
- Equipment registry
- QR code generation (permanent & expirable)
- Equipment categories and custom fields
- Maintenance schedules

**Key Models:**
- `Equipment`: Medical/lab equipment with QR codes

**Key Features:**
- Generate QR code labels
- Print labels (PDF/thermal)
- Expirable access tokens (5-minute default)
- Equipment lifecycle tracking

#### 4. **cleaning_logs** - Compliance Tracking
- Cleaning event recording
- Photo evidence storage
- Technician attribution
- Compliance calculations

**Key Models:**
- `CleaningLog`: Individual cleaning records
- `TemporaryTokenLog`: Token usage audit trail

**Key Features:**
- QR code scanning (no login required)
- Photo upload via camera
- Timestamp and geolocation (optional)
- Compliance reports

#### 5. **billing** - Stripe Integration
- Subscription management
- Usage-based billing
- Webhook handling
- Customer portal

**Key Models:**
- `Subscription`: Stripe subscription data
- `Invoice`: Billing history

**Key Features:**
- dj-stripe integration
- Webhook event processing
- Automated billing
- Usage tracking

#### 6. **notifications** - Email Alerts
- Transactional emails (Resend API)
- Scheduled reports
- Overdue alerts
- Audit reminders

**Key Features:**
- Automated email campaigns
- HTML email templates
- Scheduled tasks (cron)
- Email delivery tracking

#### 7. **documentation** - Feature Catalog
- Product feature registry
- User guides
- Help documentation
- API documentation

---

## 🔌 API Documentation

### Authentication
All API endpoints require authentication via Django session or token.

### Base URL
```
http://localhost:8000/api/
```

### Endpoints

#### Equipment
```http
GET    /api/equipment/              # List all equipment
POST   /api/equipment/              # Create equipment
GET    /api/equipment/{id}/         # Get equipment details
PUT    /api/equipment/{id}/         # Update equipment
DELETE /api/equipment/{id}/         # Delete equipment
POST   /api/equipment/{id}/generate-qr/  # Generate QR code
```

#### Cleaning Logs
```http
GET    /api/cleaning-logs/          # List cleaning logs
POST   /api/cleaning-logs/          # Create cleaning log
GET    /api/cleaning-logs/{id}/     # Get log details
POST   /api/register-cleaning/{token}/  # Public endpoint (no auth)
```

#### Facilities
```http
GET    /api/facilities/             # List facilities
GET    /api/facilities/{id}/        # Get facility details
GET    /api/facilities/{id}/compliance/  # Compliance metrics
```

### Example: Register Cleaning via QR Code

**Request:**
```http
POST /api/register-cleaning/abc123def456/
Content-Type: multipart/form-data

cleaned_by: John Doe
notes: Thorough cleaning completed
photo: [binary file]
```

**Response:**
```json
{
  "success": true,
  "message": "Cleaning recorded successfully",
  "cleaning_log_id": 42,
  "equipment": "X-Ray Machine - RM-001",
  "timestamp": "2025-01-24T10:30:00Z"
}
```

---

## 🧪 Testing

### Run Tests
```bash
# All tests
python manage.py test

# Specific app
python manage.py test apps.equipment

# With coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Data
Generate test facilities, equipment, and logs:
```bash
python create_test_data.py
```

### Manual Testing Checklist
- [ ] User registration and login
- [ ] Create facility
- [ ] Add equipment
- [ ] Generate QR codes
- [ ] Scan QR and register cleaning (mobile)
- [ ] View dashboard metrics
- [ ] Generate PDF reports
- [ ] Stripe webhook events
- [ ] Email notifications

---

## 🔒 Security

### Best Practices Implemented
- ✅ HTTPS enforced in production
- ✅ HSTS headers enabled
- ✅ CSRF protection on all forms
- ✅ XSS protection headers
- ✅ SQL injection prevention (ORM)
- ✅ Password hashing (PBKDF2)
- ✅ Expirable access tokens
- ✅ No PHI storage (HIPAA-safe)
- ✅ Audit trail for sensitive actions
- ✅ Rate limiting (configurable)

### Environment Variables
Never commit sensitive data to Git:
- Use `.env` files (add to `.gitignore`)
- Use environment variables in production
- Rotate secrets regularly

### Compliance
- **HIPAA**: No PHI stored (only equipment metadata)
- **PCI DSS**: Stripe handles payment data
- **GDPR**: User data export/deletion available

---

## 📊 Performance

### Optimization Techniques
- Database query optimization (select_related, prefetch_related)
- Static file compression (WhiteNoise)
- Image optimization (Pillow)
- CDN for static assets (optional)
- Redis caching (optional)
- Database indexing on foreign keys

### Scalability
- Multi-tenant architecture scales horizontally
- Stateless application (easy to load balance)
- Background tasks via Celery (optional)
- Database read replicas (for high traffic)

---

## 🤝 Contributing

This is a proprietary project. For authorized contributors:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Code Style
- Follow PEP 8 (Python)
- Use Black formatter
- Write docstrings for all functions
- Add tests for new features

---

## 📞 Support

### Documentation
- [Installation Guide](INSTALLATION.md)
- [API Documentation](API_DOCUMENTATION.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [User Guide](USER_GUIDE.md)

### Contact
- **Email:** natyssis23@gmail.com
- **Demo:** cleantrack.com/demo
- **Pilot Program:** pilot@cleantrack.com

---

## 📜 License

Proprietary and Confidential

Copyright (c) 2025 CleanTrack. All rights reserved.

This software is proprietary and may not be copied, modified, distributed, or used without explicit written permission from the copyright holder.

---

## 🎯 Roadmap

### Q1 2025
- ✅ MVP Launch
- ✅ Pilot program (10 facilities)
- 🔄 Mobile app (React Native)
- 🔄 Offline mode support

### Q2 2025
- 📅 Training module integration
- 📅 Advanced analytics dashboard
- 📅 Equipment manufacturer partnerships
- 📅 API marketplace

### Q3 2025
- 📅 HIPAA certification
- 📅 EU data residency
- 📅 AI-powered compliance predictions
- 📅 Mobile SDK for third-party apps

### Q4 2025
- 📅 Enterprise tier (unlimited facilities)
- 📅 White-label solution
- 📅 Integration with EHR systems
- 📅 Series A fundraising

---

## 🏆 Achievements

- ✅ Fully functional MVP
- ✅ Mobile-responsive design (iOS/Android)
- ✅ Multi-tenant architecture
- ✅ Stripe integration
- ✅ Thermal printer support
- ✅ Production-ready deployment
- ✅ Comprehensive documentation

---

## 💡 Use Cases

### 1. Hospital Equipment
- X-ray machines
- MRI scanners
- Ultrasound devices
- Surgical instruments

### 2. Laboratory Equipment
- Centrifuges
- Incubators
- Microscopes
- Analyzers

### 3. Dental Clinics
- Dental chairs
- Sterilizers
- X-ray equipment

### 4. Long-Term Care
- Patient lifts
- Wheelchairs
- Medical beds

---

## 📈 Metrics & KPIs

### Product Metrics
- Compliance rate per facility
- Average log submission time
- Equipment utilization
- Overdue equipment count

### Business Metrics
- Monthly Recurring Revenue (MRR)
- Customer Acquisition Cost (CAC)
- Lifetime Value (LTV)
- Churn rate

---

**Built with ❤️ for healthcare compliance**

*Last Updated: January 2025 | Version 1.0.0*
# CLEANTRACK
