"""
Management command to create demo data for testing CleanTrack
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from accounts.models import User, Account, Location, AccountMembership
from equipment.models import EquipmentType, CleaningProtocol, Equipment
from compliance.models import CleaningLog, ComplianceAlert


class Command(BaseCommand):
    help = 'Creates demo data for CleanTrack testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Delete existing demo data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clean']:
            self.stdout.write('Cleaning existing demo data...')
            Account.objects.filter(slug__startswith='demo-').delete()
            User.objects.filter(email__startswith='demo').delete()
            self.stdout.write(self.style.SUCCESS('✓ Existing demo data cleaned'))

        self.stdout.write('Creating demo data...')

        # Create demo users
        admin_user = User.objects.create_user(
            email='demo.admin@cleantrack.app',
            password='demo123',
            first_name='Demo',
            last_name='Admin'
        )

        technician_user = User.objects.create_user(
            email='demo.technician@cleantrack.app',
            password='demo123',
            first_name='Demo',
            last_name='Technician'
        )

        self.stdout.write(self.style.SUCCESS('✓ Created demo users'))

        # Create demo account
        account = Account.objects.create(
            name='Demo Hospital',
            slug='demo-hospital',
            owner=admin_user,
            plan='trial',
            status='active',
            max_locations=5,
            max_users=10
        )

        self.stdout.write(self.style.SUCCESS('✓ Created demo account'))

        # Create locations
        main_building = Location.objects.create(
            account=account,
            name='Main Building',
            address='123 Healthcare Ave',
            city='San Francisco',
            state='CA',
            zip_code='94102',
            contact_name='John Doe',
            contact_email='contact@demohospital.com',
            is_active=True
        )

        icu_wing = Location.objects.create(
            account=account,
            name='ICU Wing',
            address='123 Healthcare Ave, Wing B',
            city='San Francisco',
            state='CA',
            zip_code='94102',
            is_active=True
        )

        self.stdout.write(self.style.SUCCESS('✓ Created locations'))

        # Create memberships
        AccountMembership.objects.create(
            user=admin_user,
            account=account,
            role='admin'
        )

        tech_membership = AccountMembership.objects.create(
            user=technician_user,
            account=account,
            role='technician'
        )
        tech_membership.locations.add(main_building, icu_wing)

        self.stdout.write(self.style.SUCCESS('✓ Created account memberships'))

        # Create equipment types
        ultrasound = EquipmentType.objects.create(
            name='Ultrasound Machine',
            description='Medical ultrasound imaging device',
            requires_fda_compliance=True,
            requires_daily_cleaning=True,
            default_cleaning_frequency=24
        )

        ventilator = EquipmentType.objects.create(
            name='Ventilator',
            description='Medical ventilator for respiratory support',
            requires_fda_compliance=True,
            requires_daily_cleaning=True,
            default_cleaning_frequency=12
        )

        xray = EquipmentType.objects.create(
            name='X-Ray Machine',
            description='Medical X-ray imaging equipment',
            requires_fda_compliance=True,
            requires_daily_cleaning=False,
            default_cleaning_frequency=48
        )

        self.stdout.write(self.style.SUCCESS('✓ Created equipment types'))

        # Create cleaning protocols
        ultrasound_protocol = CleaningProtocol.objects.create(
            name='Standard Ultrasound Cleaning',
            equipment_type=ultrasound,
            version='1.0',
            description='Standard protocol for cleaning ultrasound transducers and equipment',
            steps=[
                'Power off the equipment',
                'Disconnect transducer',
                'Apply disinfectant spray',
                'Wait for contact time (60 seconds)',
                'Wipe with clean cloth',
                'Allow to air dry',
                'Reconnect and test'
            ],
            required_chemicals=['EPA-approved disinfectant', 'Lint-free cloth'],
            required_equipment=['Spray bottle', 'Gloves'],
            estimated_duration=15,
            contact_time=60,
            is_active=True
        )

        ventilator_protocol = CleaningProtocol.objects.create(
            name='Ventilator Cleaning Protocol',
            equipment_type=ventilator,
            version='1.0',
            description='Critical cleaning protocol for ventilators',
            steps=[
                'Don PPE',
                'Disconnect patient circuit',
                'Remove and replace filters',
                'Clean external surfaces',
                'Disinfect touchscreen',
                'Check for damage',
                'Reassemble and test'
            ],
            required_chemicals=['Medical-grade disinfectant', 'Filter replacements'],
            required_equipment=['PPE', 'Clean cloths'],
            estimated_duration=20,
            contact_time=120,
            is_active=True
        )

        self.stdout.write(self.style.SUCCESS('✓ Created cleaning protocols'))

        # Create equipment
        now = timezone.now()

        # Equipment 1: Recently cleaned (compliant)
        eq1 = Equipment.objects.create(
            location=main_building,
            equipment_type=ultrasound,
            protocol=ultrasound_protocol,
            name='GE Ultrasound Unit 1',
            serial_number='US-001-DEMO',
            asset_tag='AST-001',
            manufacturer='GE Healthcare',
            model_number='LOGIQ E9',
            cleaning_frequency=24,
            last_cleaned_at=now - timedelta(hours=2),
            status='active'
        )
        eq1.update_next_cleaning_due()

        # Equipment 2: Overdue (non-compliant)
        eq2 = Equipment.objects.create(
            location=icu_wing,
            equipment_type=ventilator,
            protocol=ventilator_protocol,
            name='Ventilator Unit A',
            serial_number='VENT-001-DEMO',
            asset_tag='AST-002',
            manufacturer='Philips',
            model_number='Respironics V60',
            cleaning_frequency=12,
            last_cleaned_at=now - timedelta(hours=20),
            status='active'
        )
        eq2.update_next_cleaning_due()

        # Equipment 3: Due soon
        eq3 = Equipment.objects.create(
            location=main_building,
            equipment_type=xray,
            name='X-Ray Machine Room 1',
            serial_number='XRAY-001-DEMO',
            asset_tag='AST-003',
            manufacturer='Siemens',
            model_number='YSIO Max',
            cleaning_frequency=48,
            last_cleaned_at=now - timedelta(hours=44),
            status='active'
        )
        eq3.update_next_cleaning_due()

        # Equipment 4: Never cleaned
        eq4 = Equipment.objects.create(
            location=icu_wing,
            equipment_type=ultrasound,
            protocol=ultrasound_protocol,
            name='Portable Ultrasound',
            serial_number='US-002-DEMO',
            asset_tag='AST-004',
            manufacturer='Mindray',
            model_number='M9',
            cleaning_frequency=24,
            status='active'
        )

        self.stdout.write(self.style.SUCCESS('✓ Created equipment'))

        # Create cleaning logs
        CleaningLog.objects.create(
            equipment=eq1,
            performed_by=technician_user,
            started_at=now - timedelta(hours=2, minutes=15),
            completed_at=now - timedelta(hours=2),
            duration=15,
            protocol_version='1.0',
            chemicals_used=['EPA-approved disinfectant'],
            steps_completed=ultrasound_protocol.steps,
            contact_time_met=True,
            all_steps_completed=True,
            validation_status='approved',
            source='manual',
            notes='Routine cleaning completed successfully'
        )

        CleaningLog.objects.create(
            equipment=eq2,
            performed_by=technician_user,
            started_at=now - timedelta(hours=20, minutes=20),
            completed_at=now - timedelta(hours=20),
            duration=20,
            protocol_version='1.0',
            chemicals_used=['Medical-grade disinfectant'],
            steps_completed=ventilator_protocol.steps,
            contact_time_met=True,
            all_steps_completed=True,
            validation_status='approved',
            source='manual'
        )

        self.stdout.write(self.style.SUCCESS('✓ Created cleaning logs'))

        # Create alerts
        ComplianceAlert.objects.create(
            equipment=eq2,
            alert_type='overdue',
            severity='high',
            title=f'Overdue Cleaning: {eq2.name}',
            message=f'Equipment {eq2.name} (S/N: {eq2.serial_number}) is overdue for cleaning.',
            suggested_action='Schedule immediate cleaning to maintain compliance.',
            status='active',
            due_by=now + timedelta(hours=2)
        )

        ComplianceAlert.objects.create(
            equipment=eq3,
            alert_type='due_soon',
            severity='medium',
            title=f'Cleaning Due Soon: {eq3.name}',
            message=f'Equipment {eq3.name} requires cleaning within 4 hours.',
            suggested_action='Schedule cleaning to avoid compliance issues.',
            status='active',
            due_by=eq3.next_cleaning_due
        )

        ComplianceAlert.objects.create(
            equipment=eq4,
            alert_type='overdue',
            severity='critical',
            title=f'Never Cleaned: {eq4.name}',
            message=f'Equipment {eq4.name} has no cleaning records.',
            suggested_action='Perform initial cleaning and establish cleaning schedule.',
            status='active',
            due_by=now
        )

        self.stdout.write(self.style.SUCCESS('✓ Created compliance alerts'))

        # Print summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('========================================'))
        self.stdout.write(self.style.SUCCESS('Demo Data Created Successfully!'))
        self.stdout.write(self.style.SUCCESS('========================================'))
        self.stdout.write('')
        self.stdout.write('Demo Login Credentials:')
        self.stdout.write('  Admin:      demo.admin@cleantrack.app / demo123')
        self.stdout.write('  Technician: demo.technician@cleantrack.app / demo123')
        self.stdout.write('')
        self.stdout.write('Demo Account: Demo Hospital')
        self.stdout.write(f'  Locations: {Location.objects.filter(account=account).count()}')
        self.stdout.write(f'  Equipment: {Equipment.objects.filter(location__account=account).count()}')
        self.stdout.write(f'  Cleaning Logs: {CleaningLog.objects.filter(equipment__location__account=account).count()}')
        self.stdout.write(f'  Active Alerts: {ComplianceAlert.objects.filter(equipment__location__account=account, status="active").count()}')
        self.stdout.write('')
        self.stdout.write('Access the admin at: http://localhost:8000/admin')
        self.stdout.write('')
