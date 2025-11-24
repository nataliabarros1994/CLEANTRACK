# utils/generate_qr.py
"""
Utility script for generating QR codes for equipment
"""
import os
import qrcode
from django.conf import settings
from apps.equipment.models import Equipment


def generate_qr_for_equipment(equipment_id, base_url="http://localhost:8000"):
    """
    Generate a QR code for a specific equipment

    Args:
        equipment_id: ID of the equipment
        base_url: Base URL for the QR code (default: http://localhost:8000)

    Returns:
        str: Path to the generated QR code image

    Example:
        >>> from utils.generate_qr import generate_qr_for_equipment
        >>> generate_qr_for_equipment(1)
        '/path/to/media/qrcodes/eq_1.png'
    """
    equipment = Equipment.objects.get(id=equipment_id)
    url = f"{base_url}/log/{equipment.public_token}/"

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=5
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Generate image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save to file
    filepath = os.path.join(settings.MEDIA_ROOT, 'qrcodes', f'eq_{equipment.id}.png')
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)

    print(f"✅ QR code gerado para: {equipment.name}")
    print(f"   URL: {url}")
    print(f"   Arquivo: {filepath}")

    return filepath


def generate_qr_for_all_equipment(base_url="http://localhost:8000"):
    """
    Generate QR codes for all active equipment

    Args:
        base_url: Base URL for the QR codes (default: http://localhost:8000)

    Returns:
        list: List of generated file paths

    Example:
        >>> from utils.generate_qr import generate_qr_for_all_equipment
        >>> paths = generate_qr_for_all_equipment()
        >>> print(f"{len(paths)} QR codes gerados")
    """
    equipment_list = Equipment.objects.filter(is_active=True)
    paths = []

    print(f"Gerando QR codes para {equipment_list.count()} equipamentos...")
    print("=" * 70)

    for equipment in equipment_list:
        try:
            filepath = generate_qr_for_equipment(equipment.id, base_url)
            paths.append(filepath)
            print()
        except Exception as e:
            print(f"❌ Erro ao gerar QR para {equipment.name}: {e}")
            print()

    print("=" * 70)
    print(f"✅ Total: {len(paths)} QR codes gerados com sucesso!")

    return paths


def generate_qr_with_custom_settings(equipment_id, base_url="http://localhost:8000",
                                     size=10, border=5, error_correction='H'):
    """
    Generate a QR code with custom settings

    Args:
        equipment_id: ID of the equipment
        base_url: Base URL for the QR code
        size: Box size (default: 10)
        border: Border size (default: 5)
        error_correction: Error correction level ('L', 'M', 'Q', 'H')

    Returns:
        str: Path to the generated QR code image

    Example:
        >>> from utils.generate_qr import generate_qr_with_custom_settings
        >>> # Gerar QR grande com alta correção
        >>> generate_qr_with_custom_settings(1, size=15, error_correction='H')
    """
    equipment = Equipment.objects.get(id=equipment_id)
    url = f"{base_url}/log/{equipment.public_token}/"

    # Map error correction levels
    error_levels = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H,
    }
    error_level = error_levels.get(error_correction, qrcode.constants.ERROR_CORRECT_H)

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_level,
        box_size=size,
        border=border
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Generate image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save to file
    filepath = os.path.join(
        settings.MEDIA_ROOT,
        'qrcodes',
        f'eq_{equipment.id}_size{size}_border{border}_{error_correction}.png'
    )
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)

    print(f"✅ QR code customizado gerado para: {equipment.name}")
    print(f"   Configurações: size={size}, border={border}, error={error_correction}")
    print(f"   URL: {url}")
    print(f"   Arquivo: {filepath}")

    return filepath


def get_qr_info(equipment_id):
    """
    Get QR code information for an equipment

    Args:
        equipment_id: ID of the equipment

    Returns:
        dict: QR code information

    Example:
        >>> from utils.generate_qr import get_qr_info
        >>> info = get_qr_info(1)
        >>> print(info['url'])
    """
    equipment = Equipment.objects.get(id=equipment_id)

    info = {
        'equipment_id': equipment.id,
        'equipment_name': equipment.name,
        'serial_number': equipment.serial_number,
        'facility': equipment.facility.name,
        'token': equipment.public_token,
        'url': f"http://localhost:8000/log/{equipment.public_token}/",
        'qr_file': os.path.join(settings.MEDIA_ROOT, 'qrcodes', f'eq_{equipment.id}.png')
    }

    return info
