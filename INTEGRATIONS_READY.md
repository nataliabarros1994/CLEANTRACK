# 🎉 Integrations Configured!

## ✅ All API Keys Configured

Your CleanTrack project now has **real API keys** for both integrations:

### 1. Resend (Email Service) ✅
```
RESEND_API_KEY=***REMOVED***
```
**Status:** ✅ Fully configured - Email sending ready!

### 2. Stripe (Payment Processing) 🔶
```
STRIPE_TEST_PUBLIC_KEY=pk_test_51ST4zs69BU3LMu1Q...
STRIPE_TEST_SECRET_KEY=sk_test_51ST4zs69BU3LMu1Q...
STRIPE_WEBHOOK_SECRET=whsec_... (needs to be added)
```
**Status:** 🔶 Almost ready - Just needs webhook secret!

---

## 🚀 Quick Start

### Start Your Project
```bash
cd /home/nataliabarros1994/Desktop/CleanTrack
docker-compose up --build
```

### Setup Database (New Terminal)
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py create_demo_data
```

### Access
- 🌍 Homepage: http://localhost:8000
- 🔐 Admin: http://localhost:8000/admin

---

## 📧 Test Email Integration

Your Resend API key is configured! Test it now:

### Method 1: Quick Test via Django Shell

```bash
# Open Django shell
docker-compose exec web python manage.py shell
```

Paste this in the shell:

```python
from cleantrack.email_service import send_template_email

# Send welcome email
result = send_template_email(
    to_email='your@email.com',  # ⚠️ Replace with your email
    subject='🎉 Welcome to CleanTrack!',
    template_name='emails/welcome.html',
    context={
        'user_name': 'Test User',
        'account_name': 'Demo Hospital',
        'plan_name': 'Trial',
        'subscription_end_date': 'March 31, 2025',
        'max_locations': 5,
        'max_users': 10,
        'dashboard_url': 'http://localhost:8000/dashboard',
        'help_url': 'http://localhost:8000/help',
    }
)

if result:
    print(f"✅ Email sent successfully! ID: {result}")
else:
    print("❌ Failed to send email - check logs")

exit()
```

**Expected Result:**
- ✅ You receive a beautifully formatted welcome email
- ✅ All variables are replaced with actual values
- ✅ CleanTrack branding and styling applied

---

### Method 2: Test All Email Templates

```python
# In Django shell
from cleantrack.email_service import (
    send_welcome_email,
    send_overdue_alert_email,
    send_payment_failed_email,
    send_weekly_compliance_summary
)
from accounts.models import User, Account
from compliance.models import ComplianceAlert
from datetime import datetime, timedelta

# Get demo user and account
user = User.objects.filter(email='demo.admin@cleantrack.app').first()
account = Account.objects.first()

# Test 1: Welcome Email
print("1. Testing Welcome Email...")
send_welcome_email(user, account)
print("✅ Welcome email sent!")

# Test 2: Overdue Alert Email
print("\n2. Testing Overdue Alert Email...")
alert = ComplianceAlert.objects.first()
if alert:
    from accounts.models import User
    tech = User.objects.filter(email='demo.technician@cleantrack.app').first()
    if tech:
        send_overdue_alert_email(alert, tech)
        print("✅ Overdue alert sent!")

# Test 3: Payment Failed Email
print("\n3. Testing Payment Failed Email...")
send_payment_failed_email(
    account=account,
    amount_due=50.00,
    next_attempt=datetime.now() + timedelta(days=3)
)
print("✅ Payment failed email sent!")

# Test 4: Weekly Summary
print("\n4. Testing Weekly Summary Email...")
from datetime import date
send_weekly_compliance_summary(
    account=account,
    summary_data={
        'start_date': date.today() - timedelta(days=7),
        'end_date': date.today(),
        'total_equipment': 4,
        'cleanings_completed': 15,
        'active_alerts': 3,
        'compliance_rate': 92.5,
        'top_locations': [
            {'name': 'Main Building', 'compliance_rate': 95, 'cleanings': 10},
            {'name': 'ICU Wing', 'compliance_rate': 90, 'cleanings': 5},
        ],
        'alerts': [
            {'equipment': 'Ultrasound Unit 1', 'severity': 'High', 'hours_overdue': 8},
            {'equipment': 'Ventilator 2', 'severity': 'Medium', 'hours_overdue': 4},
        ],
    }
)
print("✅ Weekly summary sent!")

print("\n🎉 All email templates tested!")
print("Check your inbox!")
exit()
```

---

## 💳 Test Stripe Integration

You have public and secret keys configured! Just need webhook secret.

### Step 1: Setup Stripe Webhook

```bash
# 1. Go to Stripe Dashboard
https://dashboard.stripe.com/test/webhooks

# 2. Click "Add endpoint"

# 3. Endpoint URL:
http://localhost:8000/billing/webhooks/stripe/

# 4. Select these events:
☑ customer.subscription.created
☑ customer.subscription.updated
☑ customer.subscription.deleted
☑ invoice.payment_succeeded
☑ invoice.payment_failed

# 5. Click "Add endpoint"

# 6. Copy the "Signing secret" (starts with whsec_...)

# 7. Add to .env:
STRIPE_WEBHOOK_SECRET=whsec_your_actual_secret_here

# 8. Restart services:
docker-compose restart web
```

---

### Step 2: Test Stripe with CLI

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe
# or: https://github.com/stripe/stripe-cli/releases

# Login to Stripe
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:8000/billing/webhooks/stripe/
```

**You'll see:**
```
> Ready! Your webhook signing secret is whsec_...
> (This is your STRIPE_WEBHOOK_SECRET - add to .env)
```

---

### Step 3: Trigger Test Events

In another terminal:

```bash
# Test subscription created
stripe trigger customer.subscription.created

# Test payment succeeded
stripe trigger invoice.payment_succeeded

# Test payment failed
stripe trigger invoice.payment_failed

# Test subscription updated
stripe trigger customer.subscription.updated
```

**Expected:**
- ✅ Events appear in Stripe CLI
- ✅ Webhook endpoint receives events
- ✅ Account status updates in database
- ✅ Emails sent (if configured)

---

### Step 4: View Webhook Logs

```bash
# View web container logs
docker-compose logs -f web

# Filter for Stripe events
docker-compose logs web | grep -i stripe

# Expected output:
# "Received Stripe webhook: customer.subscription.created"
# "Processing subscription for customer: cus_..."
# "Account status updated to: active"
```

---

## 📊 Integration Status

| Integration | Status | What Works |
|-------------|--------|------------|
| **Resend** | ✅ Ready | All email templates functional |
| **Stripe** | 🔶 Almost | Needs webhook secret only |

---

## 🎯 What You Can Do Now

### With Resend ✅
- ✅ Send welcome emails to new users
- ✅ Send cleaning overdue alerts
- ✅ Send payment failure notifications
- ✅ Send weekly compliance summaries
- ✅ Send password reset emails
- ✅ All transactional emails

### With Stripe (after webhook setup) 🔶
- ✅ Process subscription payments
- ✅ Handle plan upgrades/downgrades
- ✅ Manage trial periods
- ✅ Auto-suspend accounts on payment failure
- ✅ Send payment receipts
- ✅ Track subscription status

---

## 🔐 Security Checklist

Your API keys are now in `.env`:

- ✅ `.env` file is in `.gitignore`
- ✅ Using test keys (not production)
- ✅ Keys only on local machine
- ⚠️ Never commit `.env` to git
- ⚠️ Never share API keys publicly
- ⚠️ Rotate keys if exposed

---

## 🧪 Complete Integration Test

Run this comprehensive test:

```bash
# 1. Start services
docker-compose up -d

# 2. Wait for services to be ready
docker-compose logs -f web
# Wait for: "Starting development server at http://0.0.0.0:8000/"

# 3. Test email
docker-compose exec web python manage.py shell
```

In the shell:
```python
from cleantrack.email_service import send_template_email

result = send_template_email(
    to_email='your@email.com',
    subject='CleanTrack Integration Test',
    template_name='emails/welcome.html',
    context={'user_name': 'Test', 'account_name': 'Test Org'}
)

print("✅ Email integration working!" if result else "❌ Email failed")
exit()
```

```bash
# 4. Test Stripe (after adding webhook secret)
stripe login
stripe listen --forward-to localhost:8000/billing/webhooks/stripe/

# In another terminal:
stripe trigger customer.subscription.created

# Check logs:
docker-compose logs web | tail -20
```

---

## 📝 Next Steps

### 1. Test Email Now ✅
```bash
docker-compose up -d
docker-compose exec web python manage.py shell
# Send test email (code above)
```

### 2. Add Stripe Webhook Secret
```bash
# Get from: https://dashboard.stripe.com/test/webhooks
# Add to: .env
# Restart: docker-compose restart web
```

### 3. Test Complete Flow
```bash
# Create demo data
docker-compose exec web python manage.py create_demo_data

# Login to admin
# http://localhost:8000/admin
# Email: demo.admin@cleantrack.app
# Password: demo123

# Explore features:
# - View equipment
# - Create cleaning logs
# - Check compliance alerts
# - Test email notifications
```

---

## 🎊 Congratulations!

Your CleanTrack integrations are configured:

- ✅ **Resend**: Ready to send emails
- 🔶 **Stripe**: Ready to process payments (add webhook secret)

**Test email now:**
```bash
docker-compose exec web python manage.py shell
```

Then send a test email and check your inbox! 📧✨

---

**CleanTrack** - Your GRC platform with working integrations! 🚀
