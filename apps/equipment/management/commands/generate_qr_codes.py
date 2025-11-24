"""
Django management command to generate QR codes for all equipment

Usage:
    python manage.py generate_qr_codes
    python manage.py generate_qr_codes --equipment-id 1
    python manage.py generate_qr_codes --facility-id 2
    python manage.py generate_qr_codes --output-dir /path/to/qr_codes
"""

import os
import qrcode
from io import BytesIO
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.equipment.models import Equipment
from apps.cleaning_logs.views import generate_cleaning_token


class Command(BaseCommand):
    help = 'Generate QR codes for equipment cleaning registration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--equipment-id',
            type=int,
            help='Generate QR code for specific equipment ID'
        )
        parser.add_argument(
            '--facility-id',
            type=int,
            help='Generate QR codes for all equipment in a facility'
        )
        parser.add_argument(
            '--output-dir',
            type=str,
            default='qr_codes',
            help='Output directory for QR code images (default: qr_codes/)'
        )
        parser.add_argument(
            '--base-url',
            type=str,
            default='https://app.cleantrack.com',
            help='Base URL for QR codes (default: https://app.cleantrack.com)'
        )
        parser.add_argument(
            '--size',
            type=int,
            default=300,
            help='QR code size in pixels (default: 300)'
        )

    def handle(self, *args, **options):
        equipment_id = options.get('equipment_id')
        facility_id = options.get('facility_id')
        output_dir = options.get('output_dir')
        base_url = options.get('base_url').rstrip('/')
        size = options.get('size')

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Get equipment queryset
        if equipment_id:
            equipment_list = Equipment.objects.filter(id=equipment_id, is_active=True)
            if not equipment_list.exists():
                self.stdout.write(self.style.ERROR(f'Equipment ID {equipment_id} not found or inactive'))
                return
        elif facility_id:
            equipment_list = Equipment.objects.filter(facility_id=facility_id, is_active=True)
            if not equipment_list.exists():
                self.stdout.write(self.style.ERROR(f'No active equipment found in facility ID {facility_id}'))
                return
        else:
            equipment_list = Equipment.objects.filter(is_active=True)

        total = equipment_list.count()
        self.stdout.write(f'Generating QR codes for {total} equipment(s)...\n')

        success_count = 0
        for equipment in equipment_list:
            try:
                # Generate token
                token = generate_cleaning_token(equipment.id)

                # Generate URL
                url = f"{base_url}/log/{token}/"

                # Generate QR code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=10,
                    border=4,
                )
                qr.add_data(url)
                qr.make(fit=True)

                # Create image
                img = qr.make_image(fill_color="black", back_color="white")

                # Resize if needed
                if size != 300:
                    img = img.resize((size, size))

                # Generate filename
                safe_name = equipment.serial_number.replace('/', '_').replace(' ', '_')
                filename = f"{safe_name}_QR.png"
                filepath = os.path.join(output_dir, filename)

                # Save image
                img.save(filepath)

                success_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ [{success_count}/{total}] {equipment.name} ({equipment.serial_number})'
                    )
                )
                self.stdout.write(f'  File: {filepath}')
                self.stdout.write(f'  URL: {url}\n')

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'✗ Error generating QR for {equipment.name}: {str(e)}'
                    )
                )

        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully generated {success_count}/{total} QR codes'))
        self.stdout.write(f'  Output directory: {os.path.abspath(output_dir)}\n')

        # Print summary
        self.stdout.write('\n' + self.style.WARNING('IMPORTANT NOTES:'))
        self.stdout.write('  • QR codes expire after 24 hours')
        self.stdout.write('  • Regenerate QR codes daily or weekly')
        self.stdout.write('  • Print and attach QR codes to equipment')
        self.stdout.write('  • Test each QR code with a mobile device\n')
