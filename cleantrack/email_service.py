"""
Email service using Resend API

This module provides helper functions for sending emails via Resend
with HTML templates.
"""
import resend
import logging
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

# Configure Resend
resend.api_key = settings.RESEND_API_KEY if hasattr(settings, 'RESEND_API_KEY') else None


def send_template_email(to_email, subject, template_name, context, from_email=None):
    """
    Send an email using an HTML template

    Args:
        to_email (str or list): Recipient email address(es)
        subject (str): Email subject line
        template_name (str): Path to HTML template (e.g., 'emails/welcome.html')
        context (dict): Context data for template rendering
        from_email (str, optional): Sender email address

    Returns:
        dict: Response from Resend API or None if failed

    Example:
        send_template_email(
            to_email='user@example.com',
            subject='Welcome to CleanTrack!',
            template_name='emails/welcome.html',
            context={
                'user_name': 'John Doe',
                'account_name': 'Demo Hospital',
                'dashboard_url': 'https://cleantrack.app/dashboard',
            }
        )
    """
    if not resend.api_key:
        logger.error("Resend API key not configured")
        return None

    # Ensure to_email is a list
    if isinstance(to_email, str):
        to_email = [to_email]

    # Set default from email
    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL

    try:
        # Render HTML template
        html_content = render_to_string(template_name, context)

        # Create plain text version (strip HTML tags)
        text_content = strip_tags(html_content)

        # Send email via Resend
        response = resend.Emails.send({
            "from": from_email,
            "to": to_email,
            "subject": subject,
            "html": html_content,
            "text": text_content,
        })

        logger.info(f"Email sent successfully to {to_email}: {subject}")
        return response

    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}", exc_info=True)
        return None


def send_welcome_email(user, account):
    """
    Send welcome email to new user

    Args:
        user: User instance
        account: Account instance
    """
    context = {
        'user_name': user.get_full_name() or user.email,
        'account_name': account.name,
        'plan_name': account.get_plan_display(),
        'subscription_end_date': account.subscription_end_date.strftime('%B %d, %Y') if account.subscription_end_date else 'N/A',
        'max_locations': account.max_locations,
        'max_users': account.max_users,
        'dashboard_url': f"{settings.SITE_URL}/dashboard",
        'help_url': f"{settings.SITE_URL}/help",
    }

    return send_template_email(
        to_email=user.email,
        subject=f"Welcome to CleanTrack - {account.get_plan_display()} Plan",
        template_name='emails/welcome.html',
        context=context
    )


def send_overdue_alert_email(alert, user):
    """
    Send overdue cleaning alert email

    Args:
        alert: ComplianceAlert instance
        user: User instance to notify
    """
    equipment = alert.equipment
    protocol = equipment.protocol

    context = {
        'user_name': user.get_full_name() or user.email,
        'equipment_name': equipment.name,
        'serial_number': equipment.serial_number,
        'location_name': equipment.location.name,
        'last_cleaned_date': equipment.last_cleaned_at.strftime('%B %d, %Y at %I:%M %p') if equipment.last_cleaned_at else 'Never',
        'overdue_hours': alert.due_by,  # Calculate actual overdue hours
        'protocol_name': protocol.name if protocol else 'N/A',
        'protocol_steps': protocol.steps if protocol else [],
        'estimated_duration': protocol.estimated_duration if protocol else 'N/A',
        'required_chemicals': protocol.required_chemicals if protocol else [],
        'equipment_url': f"{settings.SITE_URL}/equipment/{equipment.id}",
        'alert_id': alert.id,
        'timestamp': alert.created_at.strftime('%B %d, %Y at %I:%M %p'),
    }

    return send_template_email(
        to_email=user.email,
        subject=f"🔴 Cleaning Overdue: {equipment.name}",
        template_name='emails/cleaning_overdue_alert.html',
        context=context
    )


def send_payment_failed_email(account, amount_due, next_attempt=None):
    """
    Send payment failed notification

    Args:
        account: Account instance
        amount_due: Amount that failed to charge
        next_attempt: Timestamp of next retry (optional)
    """
    context = {
        'user_name': account.owner.get_full_name() or account.owner.email,
        'account_name': account.name,
        'plan_name': account.get_plan_display(),
        'amount_due': f"{amount_due:.2f}",
        'next_attempt_date': next_attempt.strftime('%B %d, %Y') if next_attempt else None,
        'payment_update_url': f"{settings.SITE_URL}/billing/payment-method",
        'support_url': f"{settings.SITE_URL}/support",
        'invoice_id': 'INV-XXX',  # Get from Stripe
        'timestamp': timezone.now().strftime('%B %d, %Y'),
    }

    return send_template_email(
        to_email=account.owner.email,
        subject="Payment Failed - Action Required",
        template_name='emails/payment_failed.html',
        context=context
    )


def send_weekly_compliance_summary(account, summary_data):
    """
    Send weekly compliance summary report

    Args:
        account: Account instance
        summary_data: Dictionary with compliance metrics
    """
    context = {
        'user_name': account.owner.get_full_name() or account.owner.email,
        'account_name': account.name,
        'start_date': summary_data['start_date'].strftime('%B %d, %Y'),
        'end_date': summary_data['end_date'].strftime('%B %d, %Y'),
        'total_equipment': summary_data['total_equipment'],
        'cleanings_completed': summary_data['cleanings_completed'],
        'active_alerts': summary_data['active_alerts'],
        'compliance_rate': summary_data['compliance_rate'],
        'top_locations': summary_data.get('top_locations', []),
        'alerts': summary_data.get('alerts', []),
        'dashboard_url': f"{settings.SITE_URL}/dashboard",
        'report_download_url': f"{settings.SITE_URL}/reports/weekly",
        'timestamp': timezone.now().strftime('%B %d, %Y at %I:%M %p'),
    }

    return send_template_email(
        to_email=account.owner.email,
        subject=f"Weekly Compliance Summary - {account.name}",
        template_name='emails/weekly_compliance_summary.html',
        context=context
    )


# Fallback to Django's email backend if Resend is not configured
def send_email_fallback(to_email, subject, message):
    """
    Fallback to Django's default email backend

    Args:
        to_email (str or list): Recipient email address(es)
        subject (str): Email subject
        message (str): Email body (plain text)
    """
    from django.core.mail import send_mail

    if isinstance(to_email, str):
        to_email = [to_email]

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            to_email,
            fail_silently=False,
        )
        logger.info(f"Fallback email sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send fallback email: {e}")
        return False
