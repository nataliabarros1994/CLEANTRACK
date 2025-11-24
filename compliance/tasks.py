"""
Celery tasks for compliance monitoring and alerts
"""
from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from .models import ComplianceAlert, CleaningLog, AuditReport
from equipment.models import Equipment


@shared_task
def check_overdue_cleanings():
    """
    Check all active equipment for overdue or soon-to-be-overdue cleanings
    Creates alerts and sends notifications
    """
    now = timezone.now()
    warning_threshold = timedelta(hours=4)  # Alert 4 hours before due

    # Get all active equipment
    equipment_list = Equipment.objects.filter(status='active')

    alerts_created = 0
    emails_sent = 0

    for equipment in equipment_list:
        # Skip if no next cleaning due date
        if not equipment.next_cleaning_due:
            continue

        # Check if overdue
        if equipment.is_overdue:
            # Check if alert already exists
            existing_alert = ComplianceAlert.objects.filter(
                equipment=equipment,
                alert_type='overdue',
                status__in=['active', 'acknowledged']
            ).first()

            if not existing_alert:
                alert = ComplianceAlert.objects.create(
                    equipment=equipment,
                    alert_type='overdue',
                    severity='high',
                    title=f"Overdue Cleaning: {equipment.name}",
                    message=f"Equipment {equipment.name} (S/N: {equipment.serial_number}) "
                            f"is overdue for cleaning. Last cleaned: {equipment.last_cleaned_at}",
                    suggested_action="Schedule immediate cleaning to maintain compliance.",
                    due_by=now + timedelta(hours=24)
                )

                # Send email notification
                if _send_alert_email(alert):
                    alert.email_sent = True
                    alert.email_sent_at = now
                    alert.save()
                    emails_sent += 1

                alerts_created += 1

        # Check if due soon
        elif equipment.next_cleaning_due - now <= warning_threshold:
            existing_alert = ComplianceAlert.objects.filter(
                equipment=equipment,
                alert_type='due_soon',
                status__in=['active', 'acknowledged']
            ).first()

            if not existing_alert:
                alert = ComplianceAlert.objects.create(
                    equipment=equipment,
                    alert_type='due_soon',
                    severity='medium',
                    title=f"Cleaning Due Soon: {equipment.name}",
                    message=f"Equipment {equipment.name} (S/N: {equipment.serial_number}) "
                            f"requires cleaning soon. Due: {equipment.next_cleaning_due}",
                    suggested_action="Schedule cleaning within the next 4 hours.",
                    due_by=equipment.next_cleaning_due
                )

                if _send_alert_email(alert):
                    alert.email_sent = True
                    alert.email_sent_at = now
                    alert.save()
                    emails_sent += 1

                alerts_created += 1

    return {
        'checked': equipment_list.count(),
        'alerts_created': alerts_created,
        'emails_sent': emails_sent
    }


@shared_task
def generate_daily_compliance_report():
    """
    Generate daily compliance report for all accounts
    """
    from accounts.models import Account

    now = timezone.now()
    yesterday = now - timedelta(days=1)

    reports_created = 0

    for account in Account.objects.filter(status='active'):
        for location in account.locations.filter(is_active=True):
            # Get cleaning logs for yesterday
            cleanings = CleaningLog.objects.filter(
                equipment__location=location,
                completed_at__gte=yesterday,
                completed_at__lt=now
            )

            # Get active alerts
            alerts = ComplianceAlert.objects.filter(
                equipment__location=location,
                status='active'
            )

            # Calculate summary
            summary = {
                'total_equipment': location.equipment.filter(status='active').count(),
                'cleanings_completed': cleanings.filter(validation_status='approved').count(),
                'cleanings_pending': cleanings.filter(validation_status='pending').count(),
                'active_alerts': alerts.count(),
                'overdue_cleanings': alerts.filter(alert_type='overdue').count(),
                'compliance_rate': 0.0
            }

            if summary['total_equipment'] > 0:
                compliant_equipment = location.equipment.filter(
                    status='active'
                ).exclude(
                    alerts__alert_type='overdue',
                    alerts__status='active'
                ).count()
                summary['compliance_rate'] = (compliant_equipment / summary['total_equipment']) * 100

            # Create report
            report = AuditReport.objects.create(
                title=f"Daily Compliance Report - {location.name}",
                report_type='daily',
                location=location,
                start_date=yesterday,
                end_date=now,
                summary=summary,
                findings=[]
            )

            reports_created += 1

    return {'reports_created': reports_created}


@shared_task
def send_weekly_compliance_summary():
    """
    Send weekly compliance summary email to account owners and managers
    """
    from accounts.models import Account, AccountMembership

    now = timezone.now()
    week_ago = now - timedelta(days=7)

    emails_sent = 0

    for account in Account.objects.filter(status='active'):
        # Get all locations
        total_equipment = 0
        total_cleanings = 0
        total_alerts = 0

        for location in account.locations.filter(is_active=True):
            total_equipment += location.equipment.filter(status='active').count()
            total_cleanings += CleaningLog.objects.filter(
                equipment__location=location,
                completed_at__gte=week_ago,
                validation_status='approved'
            ).count()
            total_alerts += ComplianceAlert.objects.filter(
                equipment__location=location,
                status='active'
            ).count()

        # Send email to owner and admins
        recipients = [account.owner.email]

        # Add admins and managers
        memberships = AccountMembership.objects.filter(
            account=account,
            role__in=['admin', 'manager']
        )
        recipients.extend([m.user.email for m in memberships])

        subject = f"Weekly Compliance Summary - {account.name}"
        message = f"""
        Weekly Compliance Summary for {account.name}

        Period: {week_ago.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}

        Summary:
        - Total Equipment: {total_equipment}
        - Cleanings Completed: {total_cleanings}
        - Active Alerts: {total_alerts}

        Please log in to view detailed reports and take necessary actions.

        Best regards,
        CleanTrack Team
        """

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipients,
                fail_silently=False,
            )
            emails_sent += len(recipients)
        except Exception as e:
            print(f"Error sending email to {account.name}: {e}")

    return {'emails_sent': emails_sent}


def _send_alert_email(alert):
    """
    Helper function to send alert email
    """
    # Determine recipients
    recipients = []

    # Add assigned user
    if alert.assigned_to:
        recipients.append(alert.assigned_to.email)

    # Add location managers
    from accounts.models import AccountMembership
    memberships = AccountMembership.objects.filter(
        account=alert.equipment.location.account,
        role__in=['admin', 'manager'],
        locations=alert.equipment.location
    )
    recipients.extend([m.user.email for m in memberships])

    # Add account owner
    recipients.append(alert.equipment.location.account.owner.email)

    # Remove duplicates
    recipients = list(set(recipients))

    if not recipients:
        return False

    subject = f"[{alert.get_severity_display()}] {alert.title}"
    message = f"""
    Compliance Alert

    Type: {alert.get_alert_type_display()}
    Severity: {alert.get_severity_display()}
    Equipment: {alert.equipment.name} (S/N: {alert.equipment.serial_number})
    Location: {alert.equipment.location.name}

    {alert.message}

    Suggested Action:
    {alert.suggested_action}

    Due By: {alert.due_by.strftime('%Y-%m-%d %H:%M') if alert.due_by else 'N/A'}

    Please log in to CleanTrack to view details and take action.

    Best regards,
    CleanTrack Team
    """

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending alert email: {e}")
        return False
