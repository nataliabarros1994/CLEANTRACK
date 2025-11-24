"""
Management command to send automated alerts for overdue equipment
Run with: python manage.py send_overdue_alerts
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.equipment.models import Equipment
from apps.accounts.models import User
from apps.notifications.services import send_cleaning_alert


class Command(BaseCommand):
    help = 'Send email alerts for equipment overdue for cleaning'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be sent without actually sending emails',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        self.stdout.write(self.style.WARNING('Checking for overdue equipment...'))

        # Get all active equipment
        equipment_list = Equipment.objects.filter(is_active=True).select_related('facility')

        overdue_count = 0
        alerts_sent = 0

        for equipment in equipment_list:
            if equipment.is_overdue:
                overdue_count += 1

                # Get managers and admins to notify
                managers = User.objects.filter(
                    role__in=['admin', 'manager'],
                    is_active=True
                )

                self.stdout.write(
                    self.style.WARNING(
                        f'  ⚠️  OVERDUE: {equipment.name} at {equipment.facility.name}'
                    )
                )

                for manager in managers:
                    if dry_run:
                        self.stdout.write(
                            f'      [DRY RUN] Would send alert to: {manager.email}'
                        )
                    else:
                        # Send actual email
                        result = send_cleaning_alert(
                            to_email=manager.email,
                            equipment_name=f"{equipment.name} ({equipment.facility.name})"
                        )

                        if result:
                            alerts_sent += 1
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'      ✓ Alert sent to: {manager.email}'
                                )
                            )
                        else:
                            self.stdout.write(
                                self.style.ERROR(
                                    f'      ✗ Failed to send alert to: {manager.email}'
                                )
                            )

        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== Summary ==='))
        self.stdout.write(f'Total equipment checked: {equipment_list.count()}')
        self.stdout.write(f'Overdue equipment found: {overdue_count}')

        if dry_run:
            self.stdout.write(self.style.WARNING('[DRY RUN MODE - No emails sent]'))
        else:
            self.stdout.write(f'Alerts sent: {alerts_sent}')
            self.stdout.write(self.style.SUCCESS('✓ Alert process completed'))
