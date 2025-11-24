"""
Billing views including Stripe webhook handler
"""
import stripe
import logging
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from accounts.models import Account

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """
    Handle Stripe webhook events

    Supported events:
    - customer.subscription.created
    - customer.subscription.updated
    - customer.subscription.deleted
    - invoice.payment_succeeded
    - invoice.payment_failed
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.DJSTRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Invalid Stripe webhook payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid Stripe webhook signature: {e}")
        return HttpResponse(status=400)

    # Log the event
    logger.info(f"Received Stripe webhook event: {event['type']}")

    # Handle the event
    event_type = event['type']
    data_object = event['data']['object']

    try:
        if event_type == 'customer.subscription.created':
            handle_subscription_created(data_object)
        elif event_type == 'customer.subscription.updated':
            handle_subscription_updated(data_object)
        elif event_type == 'customer.subscription.deleted':
            handle_subscription_deleted(data_object)
        elif event_type == 'invoice.payment_succeeded':
            handle_payment_succeeded(data_object)
        elif event_type == 'invoice.payment_failed':
            handle_payment_failed(data_object)
        else:
            logger.info(f"Unhandled webhook event type: {event_type}")
    except Exception as e:
        logger.error(f"Error handling webhook {event_type}: {e}", exc_info=True)
        return HttpResponse(status=500)

    return HttpResponse(status=200)


def handle_subscription_created(subscription):
    """Handle new subscription creation"""
    customer_id = subscription.get('customer')
    subscription_id = subscription.get('id')
    status = subscription.get('status')
    current_period_end = subscription.get('current_period_end')

    logger.info(f"New subscription created: {subscription_id}")

    try:
        account = Account.objects.get(stripe_customer_id=customer_id)
        account.stripe_subscription_id = subscription_id

        if status == 'active':
            account.status = 'active'
            account.subscription_end_date = timezone.datetime.fromtimestamp(
                current_period_end, tz=timezone.utc
            )

        account.save()
        logger.info(f"Account {account.name} subscription activated")
    except Account.DoesNotExist:
        logger.warning(f"No account found for Stripe customer {customer_id}")


def handle_subscription_updated(subscription):
    """Handle subscription updates"""
    subscription_id = subscription.get('id')
    status = subscription.get('status')
    current_period_end = subscription.get('current_period_end')

    try:
        account = Account.objects.get(stripe_subscription_id=subscription_id)

        if status == 'active':
            account.status = 'active'
            account.subscription_end_date = timezone.datetime.fromtimestamp(
                current_period_end, tz=timezone.utc
            )
        elif status in ['past_due', 'unpaid']:
            account.status = 'suspended'
        elif status == 'canceled':
            account.status = 'cancelled'

        account.save()
    except Account.DoesNotExist:
        logger.warning(f"No account found for subscription {subscription_id}")


def handle_subscription_deleted(subscription):
    """Handle subscription cancellation"""
    subscription_id = subscription.get('id')

    try:
        account = Account.objects.get(stripe_subscription_id=subscription_id)
        account.status = 'cancelled'
        account.subscription_end_date = timezone.now()
        account.save()
        logger.info(f"Account {account.name} subscription cancelled")
    except Account.DoesNotExist:
        logger.warning(f"No account found for subscription {subscription_id}")


def handle_payment_succeeded(invoice):
    """Handle successful payment"""
    customer_id = invoice.get('customer')
    amount_paid = invoice.get('amount_paid') / 100

    logger.info(f"Payment succeeded: ${amount_paid} for customer {customer_id}")

    try:
        account = Account.objects.get(stripe_customer_id=customer_id)
        if account.status == 'suspended':
            account.status = 'active'
            account.save()
            logger.info(f"Account {account.name} reactivated")
    except Account.DoesNotExist:
        logger.warning(f"No account found for customer {customer_id}")


def handle_payment_failed(invoice):
    """Handle failed payment"""
    customer_id = invoice.get('customer')
    amount_due = invoice.get('amount_due') / 100

    logger.warning(f"Payment failed: ${amount_due} for customer {customer_id}")

    try:
        account = Account.objects.get(stripe_customer_id=customer_id)
        account.status = 'suspended'
        account.save()
        logger.info(f"Account {account.name} suspended due to payment failure")
    except Account.DoesNotExist:
        logger.warning(f"No account found for customer {customer_id}")
