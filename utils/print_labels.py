#!/usr/bin/env python
"""
Script para Impressão de Etiquetas Térmicas - CleanTrack
Compatível com Brother QL-800/810/820

Uso:
    python utils/print_labels.py <equipment_id>

Instalação:
    pip install brother-ql pillow qrcode
    sudo usermod -a -G lp $USER  # Linux - permissão USB

Exemplo:
    python utils/print_labels.py 1
    python utils/print_labels.py 5 --printer usb://0x04f9:0x2015
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cleantrack.settings')
django.setup()

from brother_ql import BrotherQLRaster, create_label
from brother_ql.backends import backend_factory
from brother_ql.devicedependent import models, label_type_specs
from PIL import Image, ImageDraw, ImageFont
import qrcode
from apps.equipment.models import Equipment


def print_equipment_label(
    equipment_id,
    printer_id='usb://0x04f9:0x2015',
    model='QL-800',
    label_size='29',
    base_url='http://app.cleantrack.com'
):
    """
    Imprime etiqueta térmica para um equipamento

    Args:
        equipment_id (int): ID do equipamento
        printer_id (str): URI da impressora (usb://VID:PID ou file://path)
        model (str): Modelo da impressora (QL-800, QL-810, QL-820)
        label_size (str): Tamanho da etiqueta ('29', '38', '62')
        base_url (str): URL base do sistema

    Returns:
        bool: True se impressão bem-sucedida

    Raises:
        Equipment.DoesNotExist: Se equipamento não for encontrado
        Exception: Erros de impressão
    """
    # Buscar equipamento
    try:
        equipment = Equipment.objects.get(id=equipment_id)
    except Equipment.DoesNotExist:
        print(f"❌ Equipamento {equipment_id} não encontrado")
        return False

    # Gerar novo token (válido por 5 minutos)
    equipment._generate_new_token()
    equipment.save(update_fields=['public_token', 'token_created_at'])

    # Gerar QR code
    qr_url = f"{base_url}/log/{equipment.public_token}/"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=2
    )
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Dimensões da etiqueta (29mm x 90mm)
    # Brother QL-800: 300 DPI
    # 29mm = 342 pixels, 90mm = 1063 pixels
    label_width = 342
    label_height = 1063

    # Criar imagem da etiqueta
    label = Image.new('RGB', (label_width, label_height), 'white')
    draw = ImageDraw.Draw(label)

    # Colar QR code no centro superior
    qr_size = 280
    qr_resized = qr_img.resize((qr_size, qr_size))
    qr_x = (label_width - qr_size) // 2
    qr_y = 30
    label.paste(qr_resized, (qr_x, qr_y))

    # Carregar fonte
    try:
        font_name = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_serial = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        font_facility = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        font_instructions = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except IOError:
        # Fallback para fonte padrão
        font_name = ImageFont.load_default()
        font_serial = ImageFont.load_default()
        font_facility = ImageFont.load_default()
        font_instructions = ImageFont.load_default()

    # Posição Y atual
    y_pos = qr_y + qr_size + 20

    # Nome do equipamento (centralizado, max 20 caracteres)
    name_text = equipment.name[:20] if len(equipment.name) > 20 else equipment.name
    # Calcular largura do texto para centralizar
    try:
        name_bbox = draw.textbbox((0, 0), name_text, font=font_name)
        name_width = name_bbox[2] - name_bbox[0]
    except AttributeError:
        # Fallback para versões antigas de Pillow
        name_width = draw.textsize(name_text, font=font_name)[0]

    name_x = (label_width - name_width) // 2
    draw.text((name_x, y_pos), name_text, fill="black", font=font_name)
    y_pos += 40

    # Serial number (centralizado)
    serial_text = f"SN: {equipment.serial_number[:15]}"
    try:
        serial_bbox = draw.textbbox((0, 0), serial_text, font=font_serial)
        serial_width = serial_bbox[2] - serial_bbox[0]
    except AttributeError:
        serial_width = draw.textsize(serial_text, font=font_serial)[0]

    serial_x = (label_width - serial_width) // 2
    draw.text((serial_x, y_pos), serial_text, fill="black", font=font_serial)
    y_pos += 30

    # Facility (centralizado)
    facility_text = equipment.facility.name[:22] if len(equipment.facility.name) > 22 else equipment.facility.name
    try:
        facility_bbox = draw.textbbox((0, 0), facility_text, font=font_facility)
        facility_width = facility_bbox[2] - facility_bbox[0]
    except AttributeError:
        facility_width = draw.textsize(facility_text, font=font_facility)[0]

    facility_x = (label_width - facility_width) // 2
    draw.text((facility_x, y_pos), facility_text, fill="black", font=font_facility)
    y_pos += 30

    # Instruções (centralizado)
    instructions_text = "Escaneie para registrar"
    try:
        inst_bbox = draw.textbbox((0, 0), instructions_text, font=font_instructions)
        inst_width = inst_bbox[2] - inst_bbox[0]
    except AttributeError:
        inst_width = draw.textsize(instructions_text, font=font_instructions)[0]

    inst_x = (label_width - inst_width) // 2
    draw.text((inst_x, y_pos), instructions_text, fill="gray", font=font_instructions)

    # Linha separadora no rodapé
    draw.line([(20, label_height - 50), (label_width - 20, label_height - 50)], fill="lightgray", width=2)

    # Logo CleanTrack (se existir)
    logo_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'static', 'logo', 'cleantrack-logo-thermal.png'
    )
    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path)
            logo_resized = logo.resize((100, 30))
            logo_x = (label_width - 100) // 2
            label.paste(logo_resized, (logo_x, label_height - 40), logo_resized if logo.mode == 'RGBA' else None)
        except Exception as e:
            print(f"⚠️  Aviso: Não foi possível adicionar logo: {e}")

    # Configurar impressora
    try:
        # Detectar backend (pyusb ou network)
        if printer_id.startswith('usb://'):
            backend_name = 'pyusb'
        elif printer_id.startswith('tcp://'):
            backend_name = 'network'
        else:
            backend_name = 'linux_kernel'

        backend = backend_factory(backend_name)
        qlr = BrotherQLRaster(model)
        qlr.exception_on_warning = True

        # Gerar instruções
        instructions = create_label(
            qlr,
            [label],
            label_size,
            rotate='90',  # Rotacionar para impressão correta
            threshold=70.0,
            dither=False,
            compress=False,
            red=False,
            dpi_600=False,
            hq=True  # Alta qualidade
        )

        # Enviar para impressora
        backend.write(instructions, printer_id)

        print(f"✅ Etiqueta impressa com sucesso!")
        print(f"   Equipamento: {equipment.name}")
        print(f"   Serial: {equipment.serial_number}")
        print(f"   Facility: {equipment.facility.name}")
        print(f"   QR URL: {qr_url}")
        print(f"   Token válido por: 5 minutos")

        return True

    except Exception as e:
        print(f"❌ Erro ao imprimir etiqueta: {e}")
        print(f"   Verifique se a impressora está conectada e ligada")
        print(f"   Printer ID: {printer_id}")
        print(f"   Model: {model}")
        return False


def list_printers():
    """Lista impressoras Brother QL disponíveis"""
    try:
        from brother_ql.backends.helpers import discover
        printers = discover(backend_identifier='pyusb')

        if printers:
            print("🖨️  Impressoras Brother QL encontradas:")
            for i, printer in enumerate(printers, 1):
                print(f"   {i}. {printer}")
        else:
            print("❌ Nenhuma impressora Brother QL encontrada")
            print("   Verifique conexão USB e drivers")

        return printers
    except Exception as e:
        print(f"❌ Erro ao listar impressoras: {e}")
        return []


def save_preview(equipment_id, output_path='label_preview.png'):
    """Salva preview da etiqueta sem imprimir"""
    try:
        equipment = Equipment.objects.get(id=equipment_id)
    except Equipment.DoesNotExist:
        print(f"❌ Equipamento {equipment_id} não encontrado")
        return False

    # Gerar token
    equipment._generate_new_token()
    equipment.save(update_fields=['public_token', 'token_created_at'])

    # Gerar QR code
    qr_url = f"http://app.cleantrack.com/log/{equipment.public_token}/"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=2)
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Criar imagem
    label_width = 342
    label_height = 1063
    label = Image.new('RGB', (label_width, label_height), 'white')
    draw = ImageDraw.Draw(label)

    # QR code
    qr_size = 280
    qr_resized = qr_img.resize((qr_size, qr_size))
    qr_x = (label_width - qr_size) // 2
    qr_y = 30
    label.paste(qr_resized, (qr_x, qr_y))

    # Texto (simplificado para preview)
    y_pos = qr_y + qr_size + 20

    try:
        font_name = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_serial = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        font_name = ImageFont.load_default()
        font_serial = ImageFont.load_default()

    # Nome
    name_text = equipment.name[:20]
    draw.text((20, y_pos), name_text, fill="black", font=font_name)
    y_pos += 40

    # Serial
    serial_text = f"SN: {equipment.serial_number[:15]}"
    draw.text((20, y_pos), serial_text, fill="black", font=font_serial)
    y_pos += 30

    # Facility
    facility_text = equipment.facility.name[:22]
    draw.text((20, y_pos), facility_text, fill="black", font=font_serial)

    # Salvar
    label.save(output_path)
    print(f"✅ Preview salvo em: {output_path}")
    print(f"   Equipamento: {equipment.name}")
    print(f"   Tamanho: {label_width}x{label_height}px (29x90mm)")

    return True


def main():
    """Função principal do script"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Impressão de Etiquetas Térmicas CleanTrack',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python utils/print_labels.py 1
  python utils/print_labels.py 5 --printer usb://0x04f9:0x2015
  python utils/print_labels.py 3 --preview label_3.png
  python utils/print_labels.py --list
        """
    )

    parser.add_argument('equipment_id', type=int, nargs='?', help='ID do equipamento')
    parser.add_argument('--printer', default='usb://0x04f9:0x2015', help='URI da impressora')
    parser.add_argument('--model', default='QL-800', choices=['QL-800', 'QL-810', 'QL-820'], help='Modelo da impressora')
    parser.add_argument('--size', default='29', choices=['29', '38', '62'], help='Tamanho da etiqueta (mm)')
    parser.add_argument('--url', default='http://app.cleantrack.com', help='URL base do sistema')
    parser.add_argument('--list', action='store_true', help='Listar impressoras disponíveis')
    parser.add_argument('--preview', metavar='FILE', help='Salvar preview sem imprimir')

    args = parser.parse_args()

    # Listar impressoras
    if args.list:
        list_printers()
        return

    # Validar equipment_id
    if not args.equipment_id:
        parser.print_help()
        sys.exit(1)

    # Preview ou impressão
    if args.preview:
        save_preview(args.equipment_id, args.preview)
    else:
        print_equipment_label(
            args.equipment_id,
            printer_id=args.printer,
            model=args.model,
            label_size=args.size,
            base_url=args.url
        )


if __name__ == "__main__":
    main()
