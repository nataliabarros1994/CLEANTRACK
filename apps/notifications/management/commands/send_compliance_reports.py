"""
Management command to send weekly compliance reports
Run with: python manage.py send_compliance_reports
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.equipment.models import Equipment
from apps.cleaning_logs.models import CleaningLog
from apps.accounts.models import User
from apps.notifications.services import send_compliance_summary


class Command(BaseCommand):
    help = 'Send weekly compliance summary reports to managers and admins'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be sent without actually sending emails',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        self.stdout.write(self.style.WARNING('Generating compliance report...'))

        # Calculate statistics
        total_equipment = Equipment.objects.filter(is_active=True).count()

        # Count overdue equipment
        overdue_count = sum(
            1 for eq in Equipment.objects.filter(is_active=True) if eq.is_overdue
        )

        # Count cleanings in the last 7 days
        week_ago = timezone.now() - timedelta(days=7)
        cleanings_completed = CleaningLog.objects.filter(
            cleaned_at__gte=week_ago
        ).count()

        # Calculate compliance rate
        if total_equipment > 0:
            compliance_rate = ((total_equipment - overdue_count) / total_equipment) * 100
        else:
            compliance_rate = 100.0

        summary_data = {
            'total_equipment': total_equipment,
            'cleanings_completed': cleanings_completed,
            'overdue_count': overdue_count,
            'compliance_rate': compliance_rate,
        }

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== Compliance Summary ==='))
        self.stdout.write(f'Total Equipment: {total_equipment}')
        self.stdout.write(f'Cleanings This Week: {cleanings_completed}')
        self.stdout.write(f'Overdue Equipment: {overdue_count}')
        self.stdout.write(f'Compliance Rate: {compliance_rate:.1f}%')
        self.stdout.write('')

        # Get managers and admins to notify
        recipients = User.objects.filter(
            role__in=['admin', 'manager'],
            is_active=True
        )

        reports_sent = 0

        for user in recipients:
            if dry_run:
                self.stdout.write(
                    f'[DRY RUN] Would send report to: {user.email}'
                )
            else:
                # Send actual email
                result = send_compliance_summary(
                    to_email=user.email,
                    summary_data=summary_data
                )

                if result:
                    reports_sent += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Report sent to: {user.email}')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Failed to send report to: {user.email}')
                    )

        # Summary
        self.stdout.write('')
        if dry_run:
            self.stdout.write(self.style.WARNING('[DRY RUN MODE - No emails sent]'))
        else:
            self.stdout.write(f'Reports sent: {reports_sent}')
            self.stdout.write(self.style.SUCCESS('✓ Compliance report process completed'))
