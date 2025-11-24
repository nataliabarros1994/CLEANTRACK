#!/usr/bin/env python
"""
Script simples para gerar QR codes para equipamentos
Pode ser executado diretamente ou via Django management command

Usage:
    python generate_qr_codes_simple.py
    python manage.py generate_qr_codes
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cleantrack.settings')
django.setup()

import qrcode
from apps.equipment.models import Equipment
from apps.cleaning_logs.views import generate_cleaning_token


def generate_qr_for_equipment(equipment, output_dir='qr_codes', base_url='https://app.cleantrack.com'):
    """
    Generate QR code for a single equipment

    Args:
        equipment: Equipment instance
        output_dir: Directory to save QR codes
        base_url: Base URL for the application

    Returns:
        Filepath of generated QR code
    """
    # Generate token
    token = generate_cleaning_token(equipment.id)

    # Generate URL
    url = f"{base_url}/log/{token}/"

    # Create QR code
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

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename
    safe_name = equipment.serial_number.replace('/', '_').replace(' ', '_')
    filename = f"{safe_name}_QR.png"
    filepath = os.path.join(output_dir, filename)

    # Save image
    img.save(filepath)

    return filepath, url


def main():
    """Generate QR codes for all active equipment"""
    print("=" * 70)
    print("  CLEANTRACK - GERADOR DE QR CODES")
    print("=" * 70)
    print()

    # Get all active equipment
    equipment_list = Equipment.objects.filter(is_active=True).select_related('facility')

    if not equipment_list.exists():
        print("❌ Nenhum equipamento ativo encontrado!")
        return

    total = equipment_list.count()
    print(f"📦 Encontrados {total} equipamentos ativos\n")

    # Configuration
    base_url = input("🌐 URL base (default: https://app.cleantrack.com): ").strip() or "https://app.cleantrack.com"
    output_dir = input("📁 Diretório de saída (default: qr_codes): ").strip() or "qr_codes"

    print(f"\n🚀 Gerando QR codes...\n")

    success_count = 0
    for i, equipment in enumerate(equipment_list, 1):
        try:
            filepath, url = generate_qr_for_equipment(equipment, output_dir, base_url)

            print(f"✅ [{i}/{total}] {equipment.name}")
            print(f"   📍 Facility: {equipment.facility.name}")
            print(f"   🔢 Serial: {equipment.serial_number}")
            print(f"   📄 Arquivo: {filepath}")
            print(f"   🔗 URL: {url}")
            print()

            success_count += 1

        except Exception as e:
            print(f"❌ [{i}/{total}] Erro ao gerar QR para {equipment.name}: {e}\n")

    print("=" * 70)
    print(f"\n✅ Gerados {success_count}/{total} QR codes com sucesso!")
    print(f"📁 Diretório: {os.path.abspath(output_dir)}\n")

    print("⚠️  NOTAS IMPORTANTES:")
    print("  • QR codes expiram após 24 horas")
    print("  • Regenere os QR codes diariamente ou semanalmente")
    print("  • Imprima e cole os QR codes nos equipamentos")
    print("  • Teste cada QR code com um celular antes de colar")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
