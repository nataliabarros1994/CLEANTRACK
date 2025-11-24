"""
DJ-Stripe webhook handlers for automated billing lifecycle management

This module uses dj-stripe's @webhooks.handler decorator to handle
Stripe webhook events cleanly and robustly.

Events handled:
- checkout.session.completed: Activate facility/account after checkout
- customer.subscription.created: Activate on new subscription
- customer.subscription.updated: Update status based on subscription
- customer.subscription.deleted: Deactivate on cancellation
- invoice.payment_succeeded: Log successful payments
- invoice.payment_failed: Handle payment failures and deactivate after retries
"""
import logging

# Defensive imports - fail gracefully if djstripe is not available
try:
    from djstripe import webhooks
except ImportError:
    # Create a dummy decorator if djstripe is not installed
    class webhooks:
        @staticmethod
        def handler(event_type):
            def decorator(func):
                return func
            return decorator

from apps.accounts.models import Account, User
from apps.facilities.models import Facility

# Defensive import for notifications
try:
    from apps.notifications.services import send_welcome_email
except ImportError:
    # Dummy function if notifications app is not available
    def send_welcome_email(*args, **kwargs):
        pass

logger = logging.getLogger(__name__)


@webhooks.handler("checkout.session.completed")
def handle_checkout_session_completed(event, **kwargs):
    """
    Handle successful checkout completion.
    This is triggered when a customer completes payment via Stripe Checkout.

    Expected metadata in checkout session:
    - facility_id: ID of the facility to activate
    - account_id: ID of the account to activate

    Or use client_reference_id for facility_id
    """
    session = event.data["object"]
    customer_id = session.get("customer")
    client_reference_id = session.get("client_reference_id")
    metadata = session.get("metadata", {})

    logger.info(f"Checkout session completed: {session.get('id')}")

    # Try to get facility_id or account_id from metadata or client_reference_id
    facility_id = metadata.get("facility_id") or client_reference_id
    account_id = metadata.get("account_id")

    # Activate Facility
    if facility_id:
        try:
            facility = Facility.objects.get(id=facility_id)
            facility.is_active = True
            facility.stripe_customer_id = customer_id
            facility.save()

            logger.info(f"Facility '{facility.name}' activated after checkout (customer: {customer_id})")

            # Send welcome email to facility managers
            managers = User.objects.filter(
                managed_facilities=facility,
                is_active=True
            )

            for manager in managers:
                if manager.email:
                    try:
                        send_welcome_email(manager.email, manager.get_full_name())
                        logger.info(f"Welcome email sent to {manager.email}")
                    except Exception as e:
                        logger.error(f"Failed to send welcome email to {manager.email}: {e}")

        except Facility.DoesNotExist:
            logger.error(f"Facility with id={facility_id} not found")
        except Exception as e:
            logger.error(f"Error activating facility: {e}")

    # Activate Account
    if account_id:
        try:
            account = Account.objects.get(id=account_id)
            account.is_active = True
            account.stripe_customer_id = customer_id
            account.save()

            logger.info(f"Account '{account.name}' activated after checkout (customer: {customer_id})")

            # Send welcome email to account owner
            if account.owner and account.owner.email:
                try:
                    send_welcome_email(account.owner.email, account.owner.get_full_name())
                    logger.info(f"Welcome email sent to account owner: {account.owner.email}")
                except Exception as e:
                    logger.error(f"Failed to send welcome email: {e}")

        except Account.DoesNotExist:
            logger.error(f"Account with id={account_id} not found")
        except Exception as e:
            logger.error(f"Error activating account: {e}")


@webhooks.handler("customer.subscription.created")
def handle_subscription_created(event, **kwargs):
    """
    Handle subscription creation.
    Activates the associated account or facility.

    Metadata should contain:
    - account_id or facility_id
    """
    subscription = event.data["object"]
    customer_id = subscription.get("customer")
    metadata = subscription.get("metadata", {})

    logger.info(f"Subscription created: {subscription.get('id')} for customer {customer_id}")

    # Get account or facility from metadata
    account_id = metadata.get("account_id")
    facility_id = metadata.get("facility_id")

    if account_id:
        try:
            account = Account.objects.get(id=account_id)
            account.is_active = True
            account.stripe_customer_id = customer_id
            account.save()
            logger.info(f"Account '{account.name}' activated via subscription")
        except Account.DoesNotExist:
            logger.error(f"Account {account_id} not found")
        except Exception as e:
            logger.error(f"Error activating account: {e}")

    if facility_id:
        try:
            facility = Facility.objects.get(id=facility_id)
            facility.is_active = True
            facility.stripe_customer_id = customer_id
            facility.save()
            logger.info(f"Facility '{facility.name}' activated via subscription")
        except Facility.DoesNotExist:
            logger.error(f"Facility {facility_id} not found")
        except Exception as e:
            logger.error(f"Error activating facility: {e}")


@webhooks.handler("customer.subscription.updated")
def handle_subscription_updated(event, **kwargs):
    """
    Handle subscription updates.
    Activate/deactivate based on subscription status.

    Status mapping:
    - active, trialing → activate
    - past_due, unpaid, canceled, incomplete_expired → deactivate
    """
    subscription = event.data["object"]
    customer_id = subscription.get("customer")
    status = subscription.get("status")

    logger.info(f"Subscription updated: {subscription.get('id')}, status: {status}")

    # Find accounts/facilities by customer_id
    accounts = Account.objects.filter(stripe_customer_id=customer_id)
    facilities = Facility.objects.filter(stripe_customer_id=customer_id)

    # Activate if subscription is active or trialing
    if status in ["active", "trialing"]:
        account_count = accounts.update(is_active=True)
        facility_count = facilities.update(is_active=True)
        logger.info(f"Activated {account_count} accounts and {facility_count} facilities")

    # Deactivate if subscription is problematic
    elif status in ["past_due", "unpaid", "canceled", "incomplete_expired"]:
        account_count = accounts.update(is_active=False)
        facility_count = facilities.update(is_active=False)
        logger.warning(
            f"Deactivated {account_count} accounts and {facility_count} facilities "
            f"due to status: {status}"
        )

        # TODO: Send notification email about deactivation


@webhooks.handler("customer.subscription.deleted")
def handle_subscription_deleted(event, **kwargs):
    """
    Handle subscription deletion/cancellation.
    Deactivates the associated account/facility.
    """
    subscription = event.data["object"]
    customer_id = subscription.get("customer")

    logger.info(f"Subscription deleted: {subscription.get('id')} for customer {customer_id}")

    # Deactivate all accounts/facilities with this customer_id
    accounts = Account.objects.filter(stripe_customer_id=customer_id)
    facilities = Facility.objects.filter(stripe_customer_id=customer_id)

    account_count = accounts.update(is_active=False)
    facility_count = facilities.update(is_active=False)

    logger.warning(
        f"Deactivated {account_count} accounts and {facility_count} facilities "
        f"due to subscription deletion"
    )

    # TODO: Send cancellation confirmation email


@webhooks.handler("invoice.payment_succeeded")
def handle_payment_succeeded(event, **kwargs):
    """
    Handle successful payment.
    Logs the payment and optionally sends receipt.
    """
    invoice = event.data["object"]
    customer_id = invoice.get("customer")
    amount_paid = invoice.get("amount_paid", 0) / 100  # Convert cents to dollars
    currency = invoice.get("currency", "usd").upper()

    logger.info(
        f"Payment succeeded: {currency} ${amount_paid:.2f} for customer {customer_id}"
    )

    # Optional: Ensure accounts/facilities are active after successful payment
    Account.objects.filter(stripe_customer_id=customer_id).update(is_active=True)
    Facility.objects.filter(stripe_customer_id=customer_id).update(is_active=True)

    # TODO: Send payment receipt email
    # TODO: Update payment history


@webhooks.handler("invoice.payment_failed")
def handle_payment_failed(event, **kwargs):
    """
    Handle failed payment.
    Deactivate account after multiple failures (3+ attempts).
    """
    invoice = event.data["object"]
    customer_id = invoice.get("customer")
    amount_due = invoice.get("amount_due", 0) / 100
    attempt_count = invoice.get("attempt_count", 0)
    currency = invoice.get("currency", "usd").upper()

    logger.warning(
        f"Payment failed (attempt {attempt_count}): {currency} ${amount_due:.2f} "
        f"for customer {customer_id}"
    )

    # After 3 failed attempts, deactivate accounts/facilities
    if attempt_count >= 3:
        accounts = Account.objects.filter(stripe_customer_id=customer_id)
        facilities = Facility.objects.filter(stripe_customer_id=customer_id)

        account_count = accounts.update(is_active=False)
        facility_count = facilities.update(is_active=False)

        logger.error(
            f"Deactivated {account_count} accounts and {facility_count} facilities "
            f"due to {attempt_count} payment failures"
        )

        # TODO: Send payment failure notification email
        # TODO: Notify account owners to update payment method


@webhooks.handler("customer.subscription.trial_will_end")
def handle_trial_will_end(event, **kwargs):
    """
    Handle trial ending notification (3 days before end).
    Send notification to customer to add payment method.
    """
    subscription = event.data["object"]
    customer_id = subscription.get("customer")
    trial_end = subscription.get("trial_end")

    logger.info(
        f"Trial ending soon for customer {customer_id}, "
        f"subscription {subscription.get('id')}"
    )

    # TODO: Send trial ending notification email
    # TODO: Prompt customer to add payment method


@webhooks.handler("charge.refunded")
def handle_charge_refunded(event, **kwargs):
    """
    Handle refund processing.
    Log refunds for accounting purposes.
    """
    charge = event.data["object"]
    customer_id = charge.get("customer")
    amount_refunded = charge.get("amount_refunded", 0) / 100
    currency = charge.get("currency", "usd").upper()

    logger.info(
        f"Charge refunded: {currency} ${amount_refunded:.2f} for customer {customer_id}"
    )

    # TODO: Send refund confirmation email
    # TODO: Update accounting records
