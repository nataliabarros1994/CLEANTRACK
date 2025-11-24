"""
Views for Equipment app
"""
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.utils import timezone
from functools import wraps
from .models import Equipment
from apps.facilities.models import Facility

# PDF generation imports
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from django.conf import settings
import os
import qrcode


def facility_manager_or_admin(user, facility_id):
    """
    Verifica se o usuário pode gerenciar esta facility específica

    Args:
        user: Usuario autenticado
        facility_id: ID da facility a verificar

    Returns:
        bool: True se usuario pode acessar, False caso contrário
    """
    if not user.is_authenticated:
        return False

    # Admins têm acesso total
    if hasattr(user, 'role') and user.role == 'admin':
        return True

    # Managers só acessam facilities que gerenciam
    if hasattr(user, 'role') and user.role == 'manager':
        return user.managed_facilities.filter(id=facility_id).exists()

    return False


def manager_required(view_func):
    """
    Decorator para proteger views que precisam verificar acesso à facility

    Redireciona para login se não autenticado ou não autorizado
    """
    @wraps(view_func)
    def wrapper(request, facility_id, *args, **kwargs):
        if not facility_manager_or_admin(request.user, facility_id):
            # Redireciona para login do admin com 'next' parameter
            login_url = reverse('admin:login')
            return redirect(f"{login_url}?next={request.path}")
        return view_func(request, facility_id, *args, **kwargs)
    return wrapper


@require_http_methods(["GET"])
@manager_required
def generate_labels_pdf(request, facility_id):
    """
    Generate PDF with table of equipment QR code labels - LANDSCAPE MODE

    URL: /equipment/labels/pdf/<facility_id>/

    Generates A4 Landscape PDF with customized branding:
    - CleanTrack logo header (if available)
    - Custom colors (blue header, green QR codes)
    - Equipment | Serial | QR Code for Cleaning
    - Professional footer with system info

    Returns:
        PDF file download
    """
    # Get facility
    facility = get_object_or_404(Facility, id=facility_id)

    # Get all active equipment in facility
    equipment_list = Equipment.objects.filter(
        facility=facility,
        is_active=True
    ).order_by('name')

    if not equipment_list.exists():
        return HttpResponse("Nenhum equipamento ativo encontrado.", status=404)

    # Create PDF buffer - LANDSCAPE MODE
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        topMargin=30,
        bottomMargin=30,
        leftMargin=30,
        rightMargin=30
    )
    elements = []

    # 🖼️ Header with logo (optional)
    logo_path = os.path.join(settings.STATIC_ROOT or 'static', 'logo', 'cleantrack-logo.png')
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=120, height=40)
        elements.append(logo)
        elements.append(Spacer(1, 10))

    # 📝 Styled title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=getSampleStyleSheet()['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.HexColor("#2c3e50")
    )
    title = Paragraph(f"Etiquetas de Conformidade – {facility.name}", title_style)
    elements.append(title)

    # 📊 Table data
    data = [["Equipamento", "Serial", "QR Code para Limpeza"]]

    # Generate table rows
    for eq in equipment_list:
        # Regenerate token for fresh QR code (valid for 5 minutes)
        eq._generate_new_token()
        eq.save(update_fields=['public_token', 'token_created_at'])

        # Create QR code with absolute URL (production-ready) - GREEN COLOR
        qr_url = request.build_absolute_uri(f"/log/{eq.public_token}/")
        qr = qrcode.QRCode(version=1, box_size=2.5, border=1)
        qr.add_data(qr_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#27ae60", back_color="white")

        # Convert to ReportLab Image
        qr_buffer = BytesIO()
        img.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)

        # Create Image object for table
        qr_image = Image(qr_buffer, width=1.2*inch, height=1.2*inch)

        # Add row to table
        data.append([
            eq.name[:50],  # More space in landscape
            eq.serial_number[:30],
            qr_image
        ])

    # 🎨 Table with custom CleanTrack colors
    table = Table(data, colWidths=[3*inch, 2*inch, 2*inch])
    table.setStyle(TableStyle([
        # Header styling - BLUE
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#3498db")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        # Body styling - LIGHT GRAY
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f8f9fa")),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#bdc3c7")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))

    elements.append(table)

    # 📝 Professional footer
    elements.append(Spacer(1, 20))
    footer_style = ParagraphStyle(
        'Footer',
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    footer = Paragraph(
        "CleanTrack • Sistema Automatizado de Conformidade Médica • Tokens válidos por 5 minutos",
        footer_style
    )
    elements.append(footer)

    # Build PDF
    doc.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="etiquetas_cleantrack_{facility.name.replace(" ", "_")}.pdf"'
    return response
