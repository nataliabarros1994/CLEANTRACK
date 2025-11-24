"""
Management command to import features from CSV file
"""
import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.documentation.models import FeatureCategory, Feature


class Command(BaseCommand):
    help = 'Import features from CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to CSV file with features'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before import'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        clear = options['clear']

        if clear:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Feature.objects.all().delete()
            FeatureCategory.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Data cleared'))

        # Map category names to icons
        category_icons = {
            'Equipamentos': '🔧',
            'QR Code': '📱',
            'Registro de Limpeza': '🧹',
            'Instalações': '🏥',
            'Usuários': '👥',
            'Dashboard': '📊',
            'Cobrança': '💳',
            'Notificações': '📧',
            'PDF': '📄',
            'API': '🔌',
            'Comandos': '⚙️',
            'Segurança': '🔒',
            'Validação': '✅',
            'Configuração': '⚙️',
            'Database': '💾',
            'Templates': '🎨',
            'Produção': '🚀',
            'Logs': '📝',
        }

        # Map to badge types
        badge_mapping = {
            'Admin': 'admin',
            'Manager': 'manager',
            'Technician': 'technician',
            'Público': 'public',
            'Public': 'public',
            'Segurança': 'security',
            'Security': 'security',
            'API': 'api',
            'Command': 'command',
            'Webhook': 'webhook',
        }

        categories = {}
        features_created = 0
        features_updated = 0

        self.stdout.write(f'Reading CSV file: {csv_file}')

        try:
            with open(csv_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    category_name = row['Categoria']
                    feature_name = row['Funcionalidade']
                    how_to_use = row['Como Usar']
                    endpoint = row['Endpoint/Comando']

                    # Get or create category
                    if category_name not in categories:
                        # Extract main category (before " - ")
                        main_category = category_name.split(' - ')[0]

                        category, created = FeatureCategory.objects.get_or_create(
                            name=main_category,
                            defaults={
                                'slug': slugify(main_category),
                                'icon': category_icons.get(main_category, '📌'),
                                'order': len(categories),
                            }
                        )
                        categories[category_name] = category

                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(f'  ✓ Created category: {category.icon} {category.name}')
                            )

                    category = categories[category_name]

                    # Determine badge
                    badge = 'none'
                    for keyword, badge_type in badge_mapping.items():
                        if keyword.lower() in feature_name.lower() or keyword.lower() in how_to_use.lower():
                            badge = badge_type
                            break

                    # Determine if requires auth
                    requires_auth = any(keyword in how_to_use.lower() for keyword in [
                        'login', 'autenticação', 'gestor', 'admin', 'manager'
                    ])

                    # Determine permission
                    requires_permission = ''
                    if 'admin' in how_to_use.lower() and 'gestor' not in how_to_use.lower():
                        requires_permission = 'admin'
                    elif 'gestor' in how_to_use.lower() or 'manager' in how_to_use.lower():
                        requires_permission = 'manager_or_admin'

                    # Create or update feature
                    feature, created = Feature.objects.update_or_create(
                        category=category,
                        name=feature_name,
                        defaults={
                            'description': how_to_use,
                            'endpoint': endpoint,
                            'badge': badge,
                            'requires_auth': requires_auth,
                            'requires_permission': requires_permission,
                            'order': features_created + features_updated,
                        }
                    )

                    if created:
                        features_created += 1
                    else:
                        features_updated += 1

            self.stdout.write(self.style.SUCCESS('\n' + '='*60))
            self.stdout.write(self.style.SUCCESS('✓ Import completed successfully!'))
            self.stdout.write(self.style.SUCCESS('='*60))
            self.stdout.write(self.style.SUCCESS(f'Categories created: {len(categories)}'))
            self.stdout.write(self.style.SUCCESS(f'Features created: {features_created}'))
            self.stdout.write(self.style.SUCCESS(f'Features updated: {features_updated}'))
            self.stdout.write(self.style.SUCCESS(f'Total features: {Feature.objects.count()}'))
            self.stdout.write(self.style.SUCCESS('='*60 + '\n'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Error: CSV file not found: {csv_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing CSV: {str(e)}'))
            raise
