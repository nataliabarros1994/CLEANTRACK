"""
Celery tasks for billing and subscription management
"""
from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta


@shared_task
def check_subscription_status():
    """
    Check subscription status for all accounts
    Suspend accounts with expired subscriptions
    """
    from accounts.models import Account

    now = timezone.now()
    warning_threshold = timedelta(days=3)  # Warn 3 days before expiration

    accounts_suspended = 0
    warnings_sent = 0

    for account in Account.objects.filter(status='active'):
        if not account.subscription_end_date:
            continue

        # Check if subscription is expired
        if account.subscription_end_date < now:
            account.status = 'suspended'
            account.save()
            accounts_suspended += 1

            # Send suspension notification
            subject = f"Subscription Suspended - {account.name}"
            message = f"""
            Your CleanTrack subscription has been suspended due to expired payment.

            Account: {account.name}
            Expiration Date: {account.subscription_end_date.strftime('%Y-%m-%d')}

            Please update your payment information to restore access.

            Best regards,
            CleanTrack Team
            """

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [account.owner.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error sending suspension email to {account.name}: {e}")

        # Check if subscription is expiring soon
        elif account.subscription_end_date - now <= warning_threshold:
            days_left = (account.subscription_end_date - now).days

            subject = f"Subscription Expiring Soon - {account.name}"
            message = f"""
            Your CleanTrack subscription is expiring soon.

            Account: {account.name}
            Expiration Date: {account.subscription_end_date.strftime('%Y-%m-%d')}
            Days Remaining: {days_left}

            Please ensure your payment method is up to date to avoid service interruption.

            Best regards,
            CleanTrack Team
            """

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [account.owner.email],
                    fail_silently=False,
                )
                warnings_sent += 1
            except Exception as e:
                print(f"Error sending expiration warning to {account.name}: {e}")

    return {
        'accounts_suspended': accounts_suspended,
        'warnings_sent': warnings_sent
    }


@shared_task
def sync_stripe_subscriptions():
    """
    Sync subscription data from Stripe
    """
    import stripe
    from accounts.models import Account

    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

    synced = 0
    errors = 0

    for account in Account.objects.exclude(stripe_subscription_id__isnull=True):
        try:
            subscription = stripe.Subscription.retrieve(account.stripe_subscription_id)

            # Update account status based on Stripe subscription
            if subscription.status == 'active':
                account.status = 'active'
                account.subscription_end_date = timezone.datetime.fromtimestamp(
                    subscription.current_period_end,
                    tz=timezone.utc
                )
            elif subscription.status in ['canceled', 'unpaid']:
                account.status = 'suspended'
            elif subscription.status == 'past_due':
                account.status = 'suspended'

            account.save()
            synced += 1

        except stripe.error.StripeError as e:
            print(f"Error syncing subscription for {account.name}: {e}")
            errors += 1

    return {
        'synced': synced,
        'errors': errors
    }
