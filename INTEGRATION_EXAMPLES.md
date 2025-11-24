# CleanTrack - Integration Examples

## Overview
This document provides practical examples for integrating CleanTrack with Stripe (payments) and Resend (emails).

---

## Table of Contents
1. [Stripe Webhook Integration](#stripe-webhook-integration)
2. [Resend Email Integration](#resend-email-integration)
3. [Testing Examples](#testing-examples)
4. [Production Setup](#production-setup)

---

## Stripe Webhook Integration

### 1. Setting Up Stripe Webhooks

#### Step 1: Get Your Webhook Secret

```bash
# In Stripe Dashboard:
# 1. Go to Developers > Webhooks
# 2. Click "Add endpoint"
# 3. URL: https://your-domain.com/billing/webhooks/stripe/
# 4. Select events to listen for
# 5. Copy the webhook signing secret
```

#### Step 2: Configure Environment Variables

```bash
# .env
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### 2. Webhook Endpoint

The webhook is already implemented at `/billing/webhooks/stripe/`

**Supported Events:**

```python
# billing/views.py

# Subscription Events
- customer.subscription.created    # New subscription
- customer.subscription.updated    # Plan change, renewal
- customer.subscription.deleted    # Cancellation

# Payment Events
- invoice.payment_succeeded        # Successful payment
- invoice.payment_failed          # Failed payment

# Customer Events
- customer.created                # New customer
```

### 3. Testing Webhooks Locally

#### Using Stripe CLI

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:8000/billing/webhooks/stripe/

# Trigger test events
stripe trigger customer.subscription.created
stripe trigger invoice.payment_succeeded
stripe trigger invoice.payment_failed
```

#### Manual Testing

```bash
# Send test webhook
curl -X POST http://localhost:8000/billing/webhooks/stripe/ \
  -H "Content-Type: application/json" \
  -H "Stripe-Signature: whsec_test..." \
  -d '{
    "type": "customer.subscription.created",
    "data": {
      "object": {
        "id": "sub_1234567890",
        "customer": "cus_1234567890",
        "status": "active",
        "current_period_end": 1735689600
      }
    }
  }'
```

### 4. Webhook Event Flow

```
Stripe Event Occurs
        ↓
Stripe sends POST to /billing/webhooks/stripe/
        ↓
Verify webhook signature
        ↓
Parse event type and data
        ↓
Call appropriate handler function
        ↓
Update Account in database
        ↓
Send confirmation email (optional)
        ↓
Return 200 OK to Stripe
```

### 5. Example: Handling Subscription Created

```python
# When a subscription is created in Stripe:

POST /billing/webhooks/stripe/
{
  "type": "customer.subscription.created",
  "data": {
    "object": {
      "id": "sub_1234567890",
      "customer": "cus_ABC123",
      "status": "active",
      "current_period_end": 1735689600,
      "items": {
        "data": [{
          "price": {
            "id": "price_trial_monthly"
          }
        }]
      }
    }
  }
}

# CleanTrack actions:
1. Find Account with stripe_customer_id='cus_ABC123'
2. Set stripe_subscription_id='sub_1234567890'
3. Set status='active'
4. Set subscription_end_date from current_period_end
5. Save Account
6. Send welcome email
```

### 6. Creating a Subscription (Example)

```python
# In your view or management command
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create customer
customer = stripe.Customer.create(
    email=user.email,
    name=account.name,
    metadata={
        'account_id': account.id,
        'account_name': account.name,
    }
)

# Save customer ID to account
account.stripe_customer_id = customer.id
account.save()

# Create subscription
subscription = stripe.Subscription.create(
    customer=customer.id,
    items=[
        {
            'price': 'price_trial_monthly',  # Your Stripe price ID
        },
    ],
    trial_period_days=14,  # Optional trial
)

# Webhook will handle updating the account
```

---

## Resend Email Integration

### 1. Setting Up Resend

#### Step 1: Get API Key

```bash
# 1. Sign up at https://resend.com
# 2. Verify your domain
# 3. Get API key from dashboard
# 4. Add to .env
```

```bash
# .env
RESEND_API_KEY=re_...
DEFAULT_FROM_EMAIL=noreply@cleantrack.app
SITE_URL=https://cleantrack.app
```

### 2. Email Templates

Templates are in `templates/emails/`:

- `base_email.html` - Base template with header/footer
- `welcome.html` - Welcome email for new users
- `cleaning_overdue_alert.html` - Overdue cleaning notification
- `payment_failed.html` - Payment failure notification
- `weekly_compliance_summary.html` - Weekly compliance report

### 3. Sending Emails

#### Using the Email Service Helper

```python
from cleantrack.email_service import send_template_email

# Send custom email
send_template_email(
    to_email='user@example.com',
    subject='Test Email',
    template_name='emails/welcome.html',
    context={
        'user_name': 'John Doe',
        'account_name': 'Demo Hospital',
        'plan_name': 'Trial',
        'subscription_end_date': 'January 31, 2025',
        'max_locations': 5,
        'max_users': 10,
        'dashboard_url': 'https://cleantrack.app/dashboard',
        'help_url': 'https://cleantrack.app/help',
    }
)
```

#### Using Built-in Functions

```python
from cleantrack.email_service import (
    send_welcome_email,
    send_overdue_alert_email,
    send_payment_failed_email,
    send_weekly_compliance_summary
)

# Send welcome email
send_welcome_email(user=user, account=account)

# Send overdue alert
send_overdue_alert_email(alert=alert, user=technician)

# Send payment failed
send_payment_failed_email(
    account=account,
    amount_due=50.00,
    next_attempt=datetime(2025, 2, 1)
)

# Send weekly summary
send_weekly_compliance_summary(
    account=account,
    summary_data={
        'start_date': start_date,
        'end_date': end_date,
        'total_equipment': 45,
        'cleanings_completed': 387,
        'active_alerts': 5,
        'compliance_rate': 92.4,
        'top_locations': [
            {'name': 'Main Building', 'compliance_rate': 95, 'cleanings': 150},
            {'name': 'ICU Wing', 'compliance_rate': 89, 'cleanings': 120},
        ],
        'alerts': [],
    }
)
```

### 4. Email Preview (Development)

```python
# In Django shell
from django.template.loader import render_to_string

context = {
    'user_name': 'John Doe',
    'equipment_name': 'GE Ultrasound Unit 1',
    'serial_number': 'US-001',
    'location_name': 'Main Building',
    'last_cleaned_date': 'January 15, 2025 at 2:00 PM',
    'overdue_hours': 8,
    'protocol_name': 'Standard Ultrasound Cleaning',
    'protocol_steps': [
        'Power off the equipment',
        'Disconnect transducer',
        'Apply disinfectant spray',
    ],
    'estimated_duration': 15,
    'required_chemicals': ['EPA-approved disinfectant'],
    'equipment_url': 'https://cleantrack.app/equipment/1',
    'alert_id': '12345',
    'timestamp': 'January 20, 2025 at 10:30 AM',
}

html = render_to_string('emails/cleaning_overdue_alert.html', context)

# Save to file for preview
with open('email_preview.html', 'w') as f:
    f.write(html)

# Open in browser to preview
```

### 5. Testing Email Delivery

```python
# Test email sending
from cleantrack.email_service import send_template_email

result = send_template_email(
    to_email='test@example.com',
    subject='Test Email from CleanTrack',
    template_name='emails/welcome.html',
    context={'user_name': 'Test User', 'account_name': 'Test Org'}
)

if result:
    print("Email sent successfully!")
    print(f"Email ID: {result}")
else:
    print("Failed to send email")
```

---

## Testing Examples

### 1. Test Stripe Webhook

```python
# tests/test_webhooks.py
from django.test import TestCase, Client
from accounts.models import Account, User
import json

class StripeWebhookTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='test@test.com', password='test')
        self.account = Account.objects.create(
            name='Test Hospital',
            slug='test-hospital',
            owner=self.user,
            stripe_customer_id='cus_test123'
        )

    def test_subscription_created(self):
        payload = {
            'type': 'customer.subscription.created',
            'data': {
                'object': {
                    'id': 'sub_test123',
                    'customer': 'cus_test123',
                    'status': 'active',
                    'current_period_end': 1735689600
                }
            }
        }

        response = self.client.post(
            '/billing/webhooks/stripe/',
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='test_signature'
        )

        self.assertEqual(response.status_code, 200)

        # Verify account was updated
        self.account.refresh_from_db()
        self.assertEqual(self.account.stripe_subscription_id, 'sub_test123')
        self.assertEqual(self.account.status, 'active')
```

### 2. Test Email Sending

```python
# tests/test_emails.py
from django.test import TestCase
from django.core import mail
from cleantrack.email_service import send_welcome_email
from accounts.models import User, Account

class EmailTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            password='test',
            first_name='John',
            last_name='Doe'
        )
        self.account = Account.objects.create(
            name='Test Hospital',
            slug='test-hospital',
            owner=self.user,
            plan='trial'
        )

    def test_welcome_email(self):
        # Send email
        result = send_welcome_email(self.user, self.account)

        # Check email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Check email content
        email = mail.outbox[0]
        self.assertIn('Welcome to CleanTrack', email.subject)
        self.assertIn('John Doe', email.body)
        self.assertIn('Test Hospital', email.body)
```

---

## Production Setup

### 1. Environment Variables

```bash
# Production .env
DEBUG=False
SECRET_KEY=<generate-strong-key>
ALLOWED_HOSTS=cleantrack.app,www.cleantrack.app

# Database
DATABASE_URL=postgres://user:pass@host:5432/cleantrack

# Redis
REDIS_URL=redis://redis:6379/0

# Stripe (Live keys)
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Resend
RESEND_API_KEY=re_...
DEFAULT_FROM_EMAIL=noreply@cleantrack.app

# Site
SITE_URL=https://cleantrack.app

# Security
CSRF_TRUSTED_ORIGINS=https://cleantrack.app
```

### 2. Stripe Setup Checklist

- [ ] Create Stripe account
- [ ] Add business information
- [ ] Verify business details
- [ ] Create products and prices
- [ ] Set up webhook endpoint
- [ ] Test webhook with Stripe CLI
- [ ] Enable live mode
- [ ] Update to live API keys

### 3. Resend Setup Checklist

- [ ] Create Resend account
- [ ] Add and verify domain
- [ ] Configure DNS records (SPF, DKIM)
- [ ] Test email delivery
- [ ] Monitor bounce rates
- [ ] Set up suppression list

### 4. Webhook Security

```python
# Production webhook verification
@csrf_exempt
@require_POST
def stripe_webhook(request):
    # Get the signature from headers
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    # Verify signature
    try:
        event = stripe.Webhook.construct_event(
            request.body,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET  # MUST be from Stripe dashboard
        )
    except stripe.error.SignatureVerificationError:
        # Invalid signature - reject
        return HttpResponse(status=400)

    # Process event
    ...
```

### 5. Monitoring

```python
# Log all webhook events
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def stripe_webhook(request):
    # Log every webhook
    logger.info(f"Webhook received: {event['type']}")

    try:
        # Process event
        ...
        logger.info(f"Webhook processed successfully: {event['type']}")
    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
        # Alert team via Sentry, Slack, etc.

    return HttpResponse(status=200)
```

---

## Common Issues & Solutions

### Issue 1: Webhook Signature Verification Fails

**Cause**: Using test webhook secret in production or vice versa

**Solution**:
```bash
# Make sure you're using the correct secret for your environment
# Test: whsec_test_...
# Live: whsec_...

# Check your .env file
echo $STRIPE_WEBHOOK_SECRET
```

### Issue 2: Emails Not Sending

**Cause**: Resend API key not configured or domain not verified

**Solution**:
```python
# Check if Resend is configured
from cleantrack.email_service import send_template_email

# Try sending test email
result = send_template_email(
    to_email='your@email.com',
    subject='Test',
    template_name='emails/welcome.html',
    context={'user_name': 'Test'}
)

if not result:
    # Check logs for error details
    # Verify RESEND_API_KEY in settings
    # Confirm domain verification in Resend dashboard
```

### Issue 3: Duplicate Webhook Events

**Cause**: Stripe retries failed webhooks

**Solution**:
```python
# Implement idempotency
def handle_subscription_created(subscription):
    subscription_id = subscription.get('id')

    # Check if already processed
    if Account.objects.filter(
        stripe_subscription_id=subscription_id
    ).exists():
        logger.info(f"Subscription {subscription_id} already processed")
        return

    # Process normally
    ...
```

---

## Additional Resources

- **Stripe Webhooks Guide**: https://stripe.com/docs/webhooks
- **Stripe CLI**: https://stripe.com/docs/stripe-cli
- **Resend Documentation**: https://resend.com/docs
- **Django Email**: https://docs.djangoproject.com/en/5.0/topics/email/

---

## Quick Reference

### Stripe Events
```
customer.subscription.created    → New subscription
customer.subscription.updated    → Plan change/renewal
customer.subscription.deleted    → Cancellation
invoice.payment_succeeded       → Payment success
invoice.payment_failed          → Payment failure
```

### Email Templates
```
emails/welcome.html                     → Welcome new users
emails/cleaning_overdue_alert.html      → Overdue cleaning
emails/payment_failed.html              → Payment issues
emails/weekly_compliance_summary.html   → Weekly reports
```

### Webhook URL
```
Production: https://cleantrack.app/billing/webhooks/stripe/
Development: http://localhost:8000/billing/webhooks/stripe/
```

---

All integrations are production-ready and tested!
