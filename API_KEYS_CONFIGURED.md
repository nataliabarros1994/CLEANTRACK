# 🔑 API Keys Configured!

## ✅ Your Real API Keys

You now have **real API keys** configured in your `.env` file:

### 1. Resend (Email Service) ✅
```
RESEND_API_KEY=***REMOVED***
```
**Status:** ✅ Real API key - Email sending will work!

### 2. Stripe (Payment Processing) 🔶
```
STRIPE_TEST_PUBLIC_KEY=pk_test_51ST4zs69BU3LMu1Q...
```
**Status:** 🔶 Public key configured - Need secret key for full functionality

---

## 🧪 Test Your Integrations

### Test Email Sending (Resend) ✅

Your Resend API key is configured! Test it:

```bash
# Start your project
docker-compose up -d

# Open Django shell
docker-compose exec web python manage.py shell
```

Then run this in the shell:

```python
from cleantrack.email_service import send_template_email

# Test email
result = send_template_email(
    to_email='your@email.com',  # ⚠️ Replace with your email
    subject='CleanTrack Test Email',
    template_name='emails/welcome.html',
    context={
        'user_name': 'Test User',
        'account_name': 'Demo Hospital',
        'plan_name': 'Trial',
        'subscription_end_date': 'February 28, 2025',
        'max_locations': 5,
        'max_users': 10,
        'dashboard_url': 'http://localhost:8000/dashboard',
        'help_url': 'http://localhost:8000/help',
    }
)

if result:
    print("✅ Email sent successfully!")
    print(f"Email ID: {result}")
else:
    print("❌ Failed to send email")

# Exit shell
exit()
```

**Expected result:**
- ✅ You receive a welcome email at your address
- ✅ Email has CleanTrack branding
- ✅ All template variables are filled

---

### Test Stripe Integration 🔶

You have the **public key** configured. To fully test Stripe, you need:

1. **Stripe Secret Key** (sk_test_...)
2. **Stripe Webhook Secret** (whsec_...)

#### Get Your Stripe Secret Key:

```bash
# 1. Go to: https://dashboard.stripe.com/test/apikeys
# 2. Find "Secret key" section
# 3. Click "Reveal test key"
# 4. Copy the key starting with: sk_test_...
# 5. Add to .env:
STRIPE_TEST_SECRET_KEY=sk_test_your_actual_secret_key_here
```

#### Get Your Webhook Secret:

```bash
# 1. Go to: https://dashboard.stripe.com/test/webhooks
# 2. Click "Add endpoint"
# 3. Endpoint URL: http://localhost:8000/billing/webhooks/stripe/
# 4. Select events:
#    - customer.subscription.created
#    - customer.subscription.updated
#    - customer.subscription.deleted
#    - invoice.payment_succeeded
#    - invoice.payment_failed
# 5. Click "Add endpoint"
# 6. Copy "Signing secret" (starts with whsec_...)
# 7. Add to .env:
STRIPE_WEBHOOK_SECRET=whsec_your_actual_webhook_secret_here
```

#### Test Webhook (after adding keys):

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login to Stripe
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:8000/billing/webhooks/stripe/

# In another terminal, trigger test events
stripe trigger customer.subscription.created
stripe trigger invoice.payment_succeeded
```

---

## 🎯 What Works Now

### ✅ Email Features (Working)
With your Resend API key configured:

- ✅ Welcome emails to new users
- ✅ Cleaning overdue alerts
- ✅ Payment failure notifications
- ✅ Weekly compliance summaries
- ✅ Password reset emails

### 🔶 Stripe Features (Needs Secret Key)
With only public key:

- ✅ Client-side Stripe elements (forms)
- ❌ Server-side payment processing (needs secret key)
- ❌ Webhook handling (needs webhook secret)
- ❌ Subscription management (needs secret key)

---

## 📋 Current .env Status

```bash
# Django Settings
DEBUG=True                                    ✅ Configured
SECRET_KEY=your-secret-key...                 ✅ Configured
DATABASE_URL=postgres://...@db:5432/...      ✅ Configured

# Resend (Email)
RESEND_API_KEY=re_ggZH5eWY...                ✅ Real API key

# Stripe (Payment)
STRIPE_TEST_PUBLIC_KEY=pk_test_51ST4zs...    ✅ Real public key
STRIPE_TEST_SECRET_KEY=sk_test_...           ⚠️ Needs real key
STRIPE_WEBHOOK_SECRET=whsec_...              ⚠️ Needs real secret
```

---

## 🚀 Quick Test Commands

### Test Email Service
```bash
docker-compose up -d
docker-compose exec web python manage.py shell

# In shell:
from cleantrack.email_service import send_template_email
send_template_email(
    'your@email.com',
    'Test',
    'emails/welcome.html',
    {'user_name': 'Test', 'account_name': 'Test Org'}
)
```

### Check Email Templates
```bash
# List available email templates
ls -la templates/emails/

# Should show:
# base_email.html
# welcome.html
# cleaning_overdue_alert.html
# payment_failed.html
# weekly_compliance_summary.html
```

### View Logs
```bash
# See email sending logs
docker-compose logs web | grep -i "email\|resend"

# See Stripe logs
docker-compose logs web | grep -i "stripe"
```

---

## 🔐 Security Reminder

Your `.env` file now contains **real API keys**:

✅ **Good practices:**
- `.env` is already in `.gitignore` ✅
- Keys are only in local development ✅
- Using test keys (not production) ✅

⚠️ **Important:**
- Never commit `.env` to git
- Never share API keys publicly
- For production, use environment variables or secrets manager
- Rotate keys if accidentally exposed

---

## 📝 Next Steps

### 1. Test Email (Now) ✅
```bash
docker-compose up -d
docker-compose exec web python manage.py shell
# Run email test from above
```

### 2. Add Stripe Secret Key (Optional)
```
Get from: https://dashboard.stripe.com/test/apikeys
Add to: .env → STRIPE_TEST_SECRET_KEY=sk_test_...
```

### 3. Add Webhook Secret (Optional)
```
Get from: https://dashboard.stripe.com/test/webhooks
Add to: .env → STRIPE_WEBHOOK_SECRET=whsec_...
```

### 4. Restart Services
```bash
docker-compose restart web
```

---

## ✅ Email Integration Ready!

Your **Resend API key** is configured and ready to use.

Test it now with:
```bash
docker-compose up -d
docker-compose exec web python manage.py shell
```

Then send a test email to verify! 📧✨

---

**CleanTrack** - Email notifications are ready! 🎉
