# CleanTrack - Project Summary

## Overview
CleanTrack is a comprehensive GRC (Governance, Risk, and Compliance) software platform designed specifically for medical equipment cleaning compliance in healthcare facilities. The platform automates tracking, alerting, and reporting to ensure regulatory compliance and reduce operational risks.

## What We've Built

### 1. Core Architecture

#### Multi-Tenant System
- **Account** → **Locations** → **Equipment** hierarchy
- Role-based access control (Admin, Manager, Technician, Auditor)
- Subscription-based plans (Trial, Standard, Custom)
- Location-based permissions and filtering

#### Technology Stack
- **Backend**: Django 5.0.1 with Python 3.11+
- **Database**: PostgreSQL 15 with optimized indexes
- **Task Queue**: Celery + Redis for background jobs
- **Payments**: Stripe integration via dj-stripe
- **Email**: Resend for transactional emails
- **Containerization**: Docker + Docker Compose

### 2. Data Models

#### Accounts App
- `User`: Custom email-based authentication
- `Account`: Organization/tenant root
- `Location`: Physical locations within an account
- `AccountMembership`: User roles and permissions

#### Equipment App
- `EquipmentType`: Categories with default protocols
- `CleaningProtocol`: Step-by-step instructions with versioning
- `Equipment`: Individual items with cleaning schedules

#### Compliance App
- `CleaningLog`: Detailed cleaning records with validation
- `ComplianceAlert`: Automated alerts for violations
- `AuditReport`: Generated compliance reports

### 3. Key Features

#### Equipment Management
- Equipment registration with serial numbers, QR codes
- Automatic protocol assignment
- IoT sensor support (webhook-ready)
- Cleaning frequency tracking
- Real-time compliance status

#### Cleaning Tracking
- Manual entry with photo evidence
- QR code scanning support
- IoT sensor integration (future)
- Protocol compliance validation
- Auto-approval based on criteria
- Duration tracking

#### Compliance Monitoring
- Automated overdue detection
- Severity-based alerts (Low, Medium, High, Critical)
- Email notifications to stakeholders
- Alert workflow (Active → Acknowledged → Resolved)
- Due-soon warnings (4 hours before)

#### Reporting & Analytics
- Daily, weekly, monthly reports
- PDF and Excel export
- Compliance rate calculations
- Historical tracking
- Audit-ready documentation

#### Background Tasks (Celery)
- Check overdue cleanings: Every 30 minutes
- Generate daily reports: 8 AM daily
- Check subscriptions: Midnight daily
- Weekly compliance summaries: Weekly
- Stripe sync: Configurable

### 4. Admin Interface
Comprehensive Django admin with:
- Custom filters and search
- Bulk actions
- Inline editing
- Date hierarchies
- Export capabilities

### 5. Security Features
- Email-based authentication via AllAuth
- Role-based permissions
- CSRF protection
- SSL redirect in production
- Secure cookie handling
- Input validation
- SQL injection protection

### 6. Subscription Management
- Stripe integration
- Webhook handling
- Plan limits enforcement
- Auto-suspension on payment failure
- Expiration warnings (3 days before)

## File Structure
```
CleanTrack/
├── accounts/                   # User & Account management
│   ├── models.py              # User, Account, Location, Membership
│   ├── admin.py               # Admin configuration
│   └── management/commands/
│       └── create_demo_data.py # Demo data generator
├── equipment/                  # Equipment management
│   ├── models.py              # EquipmentType, Protocol, Equipment
│   └── admin.py
├── compliance/                 # Compliance tracking
│   ├── models.py              # CleaningLog, Alert, Report
│   ├── admin.py
│   └── tasks.py               # Celery background tasks
├── billing/                    # Subscription management
│   └── tasks.py               # Payment processing tasks
├── cleantrack/                 # Project settings
│   ├── settings.py            # Django configuration
│   ├── urls.py                # URL routing
│   ├── celery.py              # Celery configuration
│   └── wsgi.py
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   └── index.html             # Landing page
├── static/                     # Static files (CSS, JS)
├── media/                      # User uploads
├── logs/                       # Application logs
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Container definition
├── requirements.txt            # Python dependencies
├── setup.sh                    # Quick setup script
├── README.md                   # Full documentation
├── QUICKSTART.md              # Quick start guide
├── CONTRIBUTING.md            # Contribution guidelines
└── .env.example               # Environment template
```

## Quick Start

### Using Docker (Recommended)
```bash
cp .env.example .env
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py create_demo_data
```

Visit: http://localhost:8000

### Local Development
```bash
chmod +x setup.sh
./setup.sh
source venv/bin/activate
python manage.py runserver
```

## Demo Data
Create test data instantly:
```bash
python manage.py create_demo_data
```

**Demo credentials:**
- Admin: demo.admin@cleantrack.app / demo123
- Technician: demo.technician@cleantrack.app / demo123

## API Endpoints (Future)

### IoT Webhook
```
POST /api/webhooks/iot/cleaning/
```

Payload:
```json
{
  "device_id": "IOT-12345",
  "equipment_qr": "EQ-12345",
  "started_at": "2025-01-15T10:00:00Z",
  "completed_at": "2025-01-15T10:15:00Z",
  "chemicals_used": ["Disinfectant-A"],
  "sensor_data": {"temperature": 22.5, "humidity": 45}
}
```

## Subscription Plans

| Feature | Trial ($50/mo) | Standard ($100/mo) | Custom |
|---------|---------------|-------------------|--------|
| Locations | 5 | 50 | Unlimited |
| Users | 10 | 50 | Unlimited |
| Equipment | Unlimited | Unlimited | Unlimited |
| Reports | Basic | Advanced | Custom |
| Support | Email | Priority | Dedicated |
| API Access | - | ✓ | ✓ |

## Compliance Features

### Alert Types
- **Overdue**: Cleaning past due date
- **Due Soon**: Within 4 hours of due time
- **Missed**: Cleaning was skipped
- **Incomplete**: Protocol not fully followed
- **Protocol Violation**: Steps or chemicals not met
- **Equipment Issue**: Equipment-specific problems

### Alert Severity
- **Low**: Informational
- **Medium**: Requires attention
- **High**: Urgent action needed
- **Critical**: Immediate response required

## Performance Optimizations
- Database indexes on frequently queried fields
- Celery for async operations
- Redis caching
- Optimized queries with select_related/prefetch_related
- Compressed static files (WhiteNoise)
- Connection pooling

## Production Readiness
- [x] Environment-based configuration
- [x] Database migrations
- [x] Static file handling
- [x] Logging configuration
- [x] Security headers
- [x] HTTPS redirect (production)
- [x] CSRF protection
- [x] SQL injection protection
- [x] XSS protection
- [x] Error handling
- [x] Background task processing
- [x] Email notifications
- [x] Payment processing

## Next Steps (Phase 2)

### Immediate Priorities
1. IoT webhook implementation
2. Mobile app (React Native)
3. Advanced analytics dashboard
4. REST API with DRF
5. API documentation (Swagger)

### Medium-term Goals
1. Training module (videos, quizzes)
2. Predictive analytics
3. Calendar integration
4. Bulk import/export
5. Multi-language support

### Long-term Vision
1. AI-powered compliance predictions
2. White-label option
3. Partner ecosystem via public API
4. Mobile SDK for IoT manufacturers
5. Blockchain audit trail (optional)

## Environment Variables

### Required
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: PostgreSQL connection
- `REDIS_URL`: Redis connection

### Optional (for full functionality)
- `STRIPE_PUBLIC_KEY`: Stripe publishable key
- `STRIPE_SECRET_KEY`: Stripe secret key
- `RESEND_API_KEY`: Resend API key
- `DEFAULT_FROM_EMAIL`: Email sender

## Support & Documentation
- **README.md**: Full documentation
- **QUICKSTART.md**: 5-minute setup guide
- **CONTRIBUTING.md**: Development guidelines
- **Admin docs**: Built-in Django admin docs

## Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test equipment
python manage.py test compliance

# Coverage report
coverage run --source='.' manage.py test
coverage report
```

## Deployment Platforms
- **Render**: One-click deployment
- **Fly.io**: Global distribution
- **AWS ECS**: Enterprise scale
- **Heroku**: Quick deployment
- **DigitalOcean**: App Platform

## Monitoring & Logging
- Django debug toolbar (development)
- Structured logging to files
- Celery task monitoring
- Database query logging
- Email delivery tracking

## Success Metrics (MVP Goals)
- ✓ 50+ active accounts in 3 months
- ✓ 70% retention after trial
- ✓ <30s average cleaning log time
- ✓ 60% reduction in manual alerts
- ✓ 99.5% uptime

## License
Proprietary - All rights reserved

## Credits
Built with Django, PostgreSQL, Celery, Stripe, and Resend.

---

**CleanTrack** - Ensuring medical equipment compliance, one cleaning at a time.
