# Environment Variables Setup Guide

## 📝 Current Configuration

Your `.env` file is simplified with only essential variables:

```bash
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=postgres://cleantrack_user:secure_password_123@db:5432/cleantrack

# Resend
RESEND_API_KEY=re_1234567890abcdef

# Stripe
STRIPE_TEST_PUBLIC_KEY=pk_test_...
STRIPE_TEST_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

---

## 🔧 Variable Descriptions

### Django Settings

**DEBUG**
```
Current: True
Production: False
Purpose: Enables detailed error pages and debug info
```

**SECRET_KEY**
```
Current: your-secret-key-here-change-in-production
Production: Generate a strong random key
Purpose: Cryptographic signing, sessions, CSRF protection

Generate new key:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**DATABASE_URL**
```
Current: postgres://cleantrack_user:secure_password_123@db:5432/cleantrack
Format: postgres://USER:PASSWORD@HOST:PORT/DATABASE

Components:
- User: cleantrack_user
- Password: secure_password_123
- Host: db (Docker service name) or localhost (local dev)
- Port: 5432 (PostgreSQL default)
- Database: cleantrack
```

### Resend (Email Service)

**RESEND_API_KEY**
```
Current: re_1234567890abcdef (placeholder)
Get yours: https://resend.com/api-keys
Format: re_[alphanumeric]

Steps to get API key:
1. Sign up at https://resend.com
2. Verify your domain (or use resend.dev for testing)
3. Go to API Keys section
4. Create new API key
5. Copy and paste here
```

### Stripe (Payment Processing)

**STRIPE_TEST_PUBLIC_KEY**
```
Current: pk_test_... (placeholder)
Get yours: https://dashboard.stripe.com/test/apikeys
Format: pk_test_[alphanumeric]
Purpose: Client-side Stripe integration

Visible in browser, safe to expose
```

**STRIPE_TEST_SECRET_KEY**
```
Current: sk_test_... (placeholder)
Get yours: https://dashboard.stripe.com/test/apikeys
Format: sk_test_[alphanumeric]
Purpose: Server-side Stripe API calls

⚠️ KEEP SECRET! Never commit to git or expose publicly
```

**STRIPE_WEBHOOK_SECRET**
```
Current: whsec_... (placeholder)
Get yours: https://dashboard.stripe.com/test/webhooks
Format: whsec_[alphanumeric]
Purpose: Verify webhook signatures

Steps:
1. Go to Stripe Dashboard > Developers > Webhooks
2. Click "Add endpoint"
3. URL: http://localhost:8000/billing/webhooks/stripe/ (or your domain)
4. Select events to listen for
5. Copy the "Signing secret"
```

---

## 🚀 Quick Setup

### Option 1: Use Defaults (Development Only)
```bash
# Current .env works out of the box!
# Just start the project:
docker-compose up --build
```

**What works:**
- ✅ Django app
- ✅ PostgreSQL database
- ✅ All features except email and payments

**What needs real keys:**
- ❌ Email sending (needs real RESEND_API_KEY)
- ❌ Stripe payments (needs real Stripe keys)

### Option 2: Add Real API Keys
```bash
# 1. Copy .env.example to .env (if not done)
cp .env.example .env

# 2. Edit .env and add real keys
nano .env

# 3. Add your keys:
RESEND_API_KEY=re_your_real_key_here
STRIPE_TEST_PUBLIC_KEY=pk_test_your_real_key
STRIPE_TEST_SECRET_KEY=sk_test_your_real_key
STRIPE_WEBHOOK_SECRET=whsec_your_real_webhook_secret

# 4. Save and start
docker-compose up --build
```

---

## 🔐 Security Best Practices

### Development
```bash
✅ Use .env file (already in .gitignore)
✅ Use test API keys (pk_test_..., sk_test_...)
✅ Keep DEBUG=True for detailed errors
⚠️ Use simple SECRET_KEY (but still keep it secret)
```

### Production
```bash
✅ Use environment variables or secrets manager
✅ Use live API keys (pk_live_..., sk_live_...)
✅ Set DEBUG=False
✅ Generate strong SECRET_KEY (50+ random characters)
✅ Use HTTPS only
✅ Set strong database passwords
✅ Enable SSL for database connection
```

---

## 🧪 Testing API Keys

### Test Resend
```python
# Django shell
docker-compose exec web python manage.py shell

# Test email
from cleantrack.email_service import send_template_email
result = send_template_email(
    to_email='your@email.com',
    subject='Test Email',
    template_name='emails/welcome.html',
    context={'user_name': 'Test', 'account_name': 'Test Org'}
)
print("Email sent!" if result else "Failed - check RESEND_API_KEY")
```

### Test Stripe
```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Listen for webhooks
stripe listen --forward-to localhost:8000/billing/webhooks/stripe/

# In another terminal, trigger test event
stripe trigger customer.subscription.created
```

---

## 🔄 Switching Environments

### Development → Production
```bash
# Update .env:
DEBUG=False
SECRET_KEY=[generate new strong key]
DATABASE_URL=postgres://user:pass@production-host:5432/db
RESEND_API_KEY=re_live_key
STRIPE_TEST_PUBLIC_KEY=pk_live_key  # Change to live key
STRIPE_TEST_SECRET_KEY=sk_live_key  # Change to live key
STRIPE_WEBHOOK_SECRET=whsec_live_webhook_secret
```

### Local → Docker
```bash
# Change DATABASE_URL host:
DATABASE_URL=postgres://cleantrack_user:secure_password_123@db:5432/cleantrack
#                                                            ^^
#                                                          "db" not "localhost"
```

---

## 📋 Complete .env Template

```bash
# =============================================================================
#                          CLEANTRACK ENVIRONMENT
# =============================================================================

# Django Settings
# -----------------------------------------------------------------------------
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=postgres://cleantrack_user:secure_password_123@db:5432/cleantrack

# Email Service (Resend)
# -----------------------------------------------------------------------------
# Get yours: https://resend.com/api-keys
RESEND_API_KEY=re_1234567890abcdef

# Payment Processing (Stripe)
# -----------------------------------------------------------------------------
# Test keys: https://dashboard.stripe.com/test/apikeys
# Live keys: https://dashboard.stripe.com/apikeys
STRIPE_TEST_PUBLIC_KEY=pk_test_...
STRIPE_TEST_SECRET_KEY=sk_test_...

# Webhook secret: https://dashboard.stripe.com/test/webhooks
STRIPE_WEBHOOK_SECRET=whsec_...

# =============================================================================
# Optional (Uncomment if needed)
# =============================================================================

# ALLOWED_HOSTS=localhost,127.0.0.1
# DEFAULT_FROM_EMAIL=noreply@cleantrack.app
# CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
# TRIAL_PRICE_MONTHLY=50
# STANDARD_PRICE_MONTHLY=100
# MAX_LOCATIONS_TRIAL=5
# MAX_LOCATIONS_STANDARD=50
```

---

## ⚠️ Important Notes

### .env vs .env.example
```
.env          → Your actual config (NOT in git)
.env.example  → Template for others (IN git)
```

### Database Host
```
Docker:   DATABASE_URL=postgres://...@db:5432/...
Local:    DATABASE_URL=postgres://...@localhost:5432/...
```

### API Key Prefixes
```
Resend:  re_...
Stripe:  pk_test_... (public), sk_test_... (secret), whsec_... (webhook)
```

---

## ✅ Checklist

Before starting the project:

- [ ] `.env` file exists
- [ ] `DATABASE_URL` points to correct host (`db` for Docker)
- [ ] `SECRET_KEY` is set (any value for dev)
- [ ] (Optional) Add real `RESEND_API_KEY` for email
- [ ] (Optional) Add real Stripe keys for payments
- [ ] `.env` is in `.gitignore` (already done)

---

Your environment is ready! Start with: `docker-compose up --build`

Real API keys are optional - the app works without them (just email/payments won't work).
