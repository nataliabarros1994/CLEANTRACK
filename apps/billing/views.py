"""
Stripe webhook handlers for billing events

This module handles webhook events from Stripe to manage:
- Account activation/deactivation based on subscription status
- Facility activation after checkout completion
- Payment failure notifications
- Subscription lifecycle management
"""
import stripe
import logging
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from apps.accounts.models import Account, User
from apps.facilities.models import Facility
from apps.notifications.services import send_welcome_email

logger = logging.getLogger(__name__)

# Configure Stripe
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """
    Handle Stripe webhook events for subscription management

    Events handled:
    - customer.subscription.created: Activate account when subscription starts
    - customer.subscription.updated: Handle subscription changes
    - customer.subscription.deleted: Deactivate account when subscription ends
    - invoice.payment_succeeded: Confirm successful payment
    - invoice.payment_failed: Handle failed payment
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    # Get webhook secret from settings
    webhook_secret = settings.DJSTRIPE_WEBHOOK_SECRET

    if not webhook_secret:
        return JsonResponse({'error': 'Webhook secret not configured'}, status=500)

    try:
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    event_type = event['type']
    event_data = event['data']['object']

    print(f"Received Stripe webhook: {event_type}")

    # Subscription created - activate account
    if event_type == 'customer.subscription.created':
        handle_subscription_created(event_data)

    # Subscription updated - handle changes
    elif event_type == 'customer.subscription.updated':
        handle_subscription_updated(event_data)

    # Subscription deleted/cancelled - deactivate account
    elif event_type == 'customer.subscription.deleted':
        handle_subscription_deleted(event_data)

    # Payment succeeded
    elif event_type == 'invoice.payment_succeeded':
        handle_payment_succeeded(event_data)

    # Payment failed
    elif event_type == 'invoice.payment_failed':
        handle_payment_failed(event_data)

    # Checkout session completed - activate facility after successful checkout
    elif event_type == 'checkout.session.completed':
        handle_checkout_completed(event_data)

    return JsonResponse({'status': 'success'})


def handle_subscription_created(subscription):
    """
    Activate account when subscription is created
    """
    customer_id = subscription.get('customer')

    try:
        # Find account by Stripe customer ID (requires adding stripe_customer_id to Account model)
        # For now, we'll use metadata to link customer to account
        metadata = subscription.get('metadata', {})
        account_id = metadata.get('account_id')

        if account_id:
            account = Account.objects.get(id=account_id)
            account.is_active = True
            account.save()

            print(f" Account {account.name} activated (subscription created)")
    except Account.DoesNotExist:
        print(f" Account not found for subscription {subscription.get('id')}")
    except Exception as e:
        print(f" Error activating account: {e}")


def handle_subscription_updated(subscription):
    """
    Handle subscription updates (plan changes, status changes, etc.)
    """
    customer_id = subscription.get('customer')
    status = subscription.get('status')

    try:
        metadata = subscription.get('metadata', {})
        account_id = metadata.get('account_id')

        if account_id:
            account = Account.objects.get(id=account_id)

            # Activate if subscription is active or trialing
            if status in ['active', 'trialing']:
                account.is_active = True
                account.save()
                print(f" Account {account.name} activated (status: {status})")

            # Deactivate if subscription is past_due, unpaid, or cancelled
            elif status in ['past_due', 'unpaid', 'canceled', 'incomplete_expired']:
                account.is_active = False
                account.save()
                print(f" Account {account.name} deactivated (status: {status})")

    except Account.DoesNotExist:
        print(f" Account not found for subscription {subscription.get('id')}")
    except Exception as e:
        print(f" Error updating account: {e}")


def handle_subscription_deleted(subscription):
    """
    Deactivate account when subscription is deleted/cancelled
    """
    try:
        metadata = subscription.get('metadata', {})
        account_id = metadata.get('account_id')

        if account_id:
            account = Account.objects.get(id=account_id)
            account.is_active = False
            account.save()

            print(f" Account {account.name} deactivated (subscription deleted)")
    except Account.DoesNotExist:
        print(f" Account not found for subscription {subscription.get('id')}")
    except Exception as e:
        print(f" Error deactivating account: {e}")


def handle_payment_succeeded(invoice):
    """
    Handle successful payment
    """
    customer_id = invoice.get('customer')
    amount_paid = invoice.get('amount_paid') / 100  # Convert cents to dollars

    print(f" Payment succeeded: ${amount_paid:.2f} for customer {customer_id}")

    # You can add additional logic here, such as:
    # - Sending a payment receipt email
    # - Updating payment history
    # - Extending account validity period


def handle_payment_failed(invoice):
    """
    Handle failed payment
    """
    customer_id = invoice.get('customer')
    amount_due = invoice.get('amount_due') / 100  # Convert cents to dollars

    print(f" Payment failed: ${amount_due:.2f} for customer {customer_id}")

    # You can add additional logic here, such as:
    # - Sending a payment failure notification
    # - Scheduling retry attempts
    # - Warning about account suspension


def handle_checkout_completed(session):
    """
    Handle successful checkout completion
    Activates facility and sends welcome email

    This is triggered when a customer completes the Stripe Checkout process
    """
    try:
        # Get metadata from checkout session
        metadata = session.get('metadata', {})
        facility_id = metadata.get('facility_id')
        user_email = session.get('customer_details', {}).get('email')

        logger.info(f"Checkout completed for facility_id: {facility_id}, email: {user_email}")

        if not facility_id:
            logger.error("No facility_id found in checkout session metadata")
            return

        # Activate facility
        try:
            facility = Facility.objects.get(id=facility_id)
            facility.is_active = True
            facility.stripe_customer_id = session.get('customer')
            facility.save()

            logger.info(f"✅ Facility '{facility.name}' activated successfully")

            # Send welcome email to customer
            if user_email:
                # Get facility manager or use email from checkout
                managers = facility.managers.filter(is_active=True).first()
                user_name = managers.get_full_name() if managers else user_email.split('@')[0]

                send_welcome_email(user_email, user_name)
                logger.info(f"✅ Welcome email sent to {user_email}")

            print(f"✅ Checkout completed: Facility '{facility.name}' activated")

        except Facility.DoesNotExist:
            logger.error(f"Facility with id {facility_id} not found")
            print(f"❌ Error: Facility {facility_id} not found")

    except Exception as e:
        logger.error(f"Error handling checkout completion: {e}")
        print(f"❌ Error handling checkout: {e}")
