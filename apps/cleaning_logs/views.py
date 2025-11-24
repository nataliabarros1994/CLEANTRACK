"""
Views for cleaning log registration
- Authenticated cleaning registration (existing)
- Public QR code-based registration (new)
"""

import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.utils import timezone
from apps.equipment.models import Equipment
from .models import CleaningLog
from .forms import PublicCleaningLogForm

logger = logging.getLogger(__name__)


# Token signer for QR codes (deprecated - using permanent tokens now)
from django.core.signing import Signer, BadSignature
signer = Signer()


# ============================================================================
# AUTHENTICATED VIEWS (existing functionality)
# ============================================================================

@login_required
def register_cleaning(request, equipment_id):
    """Authenticated cleaning registration"""
    equipment = get_object_or_404(Equipment, id=equipment_id)

    if request.method == "POST":
        notes = request.POST.get("notes", "")
        photo = request.FILES.get("photo")

        CleaningLog.objects.create(
            equipment=equipment,
            cleaned_by=request.user,
            cleaned_at=timezone.now(),
            notes=notes,
            photo=photo,
            is_compliant=True
        )
        return redirect("cleaning_success", equipment_id=equipment.id)

    return render(request, "cleaning_logs/register.html", {"equipment": equipment})


@login_required
def cleaning_success(request, equipment_id):
    """Cleaning success page"""
    equipment = get_object_or_404(Equipment, id=equipment_id)
    return render(request, "cleaning_logs/success.html", {"equipment": equipment})


# ============================================================================
# PUBLIC QR CODE VIEWS (new functionality)
# ============================================================================

def public_log_form(request, token):
    """
    Display public cleaning log form with optional technician authentication

    - If technician is logged in, automatically link cleaning to their account
    - Otherwise, allow anonymous cleaning submission via QR code
    - Token must be valid (5-minute expiry)
    """
    equipment = get_object_or_404(Equipment, public_token=token, is_active=True)

    # Check if token is still valid
    if not equipment.is_token_valid():
        return HttpResponse('''
            <div class="alert alert-warning m-3">
                ⏳ Este link expirou. Solicite um novo QR code.
            </div>
            <a href="javascript:history.back()" class="btn btn-secondary ms-3">Voltar</a>
        ''', status=410)

    # Check if user is logged in as technician (optional authentication)
    cleaned_by = None
    if request.user.is_authenticated:
        if hasattr(request.user, 'role') and request.user.role == 'technician':
            cleaned_by = request.user
            logger.info(f"Technician {request.user.id} accessing QR code for equipment {equipment.id}")

    return render(request, 'cleaning_logs/public_log_form.html', {
        'equipment': equipment,
        'form': PublicCleaningLogForm(),
        'logged_in_user': cleaned_by,
        'is_technician_authenticated': cleaned_by is not None
    })


@csrf_exempt
@require_http_methods(["POST"])
def public_log_submit(request, token):
    """
    Submit public cleaning log with optional technician authentication

    - If technician is logged in, links cleaning to their account
    - Otherwise, creates anonymous cleaning log
    - Validates token expiry (5 minutes)
    """
    equipment = get_object_or_404(Equipment, public_token=token, is_active=True)

    # Check if token is still valid
    if not equipment.is_token_valid():
        return HttpResponse('<div class="alert alert-danger">❌ Link expirado.</div>', status=410)

    # Check if user is authenticated technician
    cleaned_by = None
    if request.user.is_authenticated:
        if hasattr(request.user, 'role') and request.user.role == 'technician':
            cleaned_by = request.user

    form = PublicCleaningLogForm(request.POST, request.FILES)

    if form.is_valid():
        try:
            log = CleaningLog.objects.create(
                equipment=equipment,
                cleaned_by=cleaned_by,  # Link to technician if authenticated
                cleaned_at=timezone.now(),
                notes=form.cleaned_data['notes'],
                photo=form.cleaned_data['photo'],
                is_compliant=True  # assumimos conformidade inicial
            )

            # Log with appropriate message
            if cleaned_by:
                logger.info(f"Authenticated cleaning log created: {log.id} by technician {cleaned_by.id} for equipment {equipment.id}")
                user_msg = f"✅ Limpeza registrada por {cleaned_by.get_full_name() or cleaned_by.email}!"
            else:
                logger.info(f"Anonymous cleaning log created: {log.id} for equipment {equipment.id}")
                user_msg = "✅ Limpeza registrada com sucesso!"

            return HttpResponse(f'''
                <div class="alert alert-success">{user_msg}</div>
                <button class="btn btn-primary" hx-get="/log/{token}" hx-target="body">Registrar outra</button>
            ''')
        except Exception as e:
            logger.error(f"Error creating cleaning log: {e}")
            return HttpResponse('<div class="alert alert-danger">❌ Erro ao salvar. Tente novamente.</div>')
    else:
        return HttpResponse(f'<div class="alert alert-warning">⚠️ {form.errors}</div>')


@require_http_methods(["GET"])
@login_required
def get_equipment_qr_token(request, equipment_id):
    """
    Admin endpoint to get permanent QR token for equipment

    Requires authentication and permission check

    URL: /admin-api/equipment/<id>/qr-token/
    """
    equipment = get_object_or_404(Equipment, id=equipment_id)

    # Check permissions
    if not request.user.is_superuser:
        if not equipment.facility.managers.filter(id=request.user.id).exists():
            return JsonResponse({'error': 'Permission denied'}, status=403)

    # Get permanent token
    token = equipment.public_token

    # Generate full URL
    protocol = 'https' if request.is_secure() else 'http'
    host = request.get_host()
    url = f"{protocol}://{host}/log/{token}/"

    return JsonResponse({
        'token': token,
        'url': url,
        'equipment_id': equipment_id,
        'equipment_name': equipment.name,
        'serial_number': equipment.serial_number,
        'facility': equipment.facility.name,
        'permanent': True,
        'qr_code_url': f"/admin-api/equipment/{equipment_id}/qr-code/"
    })


# ============================================================================
# EXPIRABLE TOKEN VIEWS (5 minute tokens)
# ============================================================================

@require_http_methods(["GET"])
@login_required
def generate_expirable_token_view(request, equipment_id):
    """
    Generate a temporary token (expires in 5 minutes)

    URL: /admin-api/equipment/<id>/generate-temp-token/
    """
    from .tokens import generate_expirable_token
    from .models import TemporaryTokenLog

    equipment = get_object_or_404(Equipment, id=equipment_id)

    # Check permissions
    if not request.user.is_superuser:
        if not equipment.facility.managers.filter(id=request.user.id).exists():
            return JsonResponse({'error': 'Permission denied'}, status=403)

    # Generate expirable token
    expiry_minutes = 5
    token = generate_expirable_token(equipment_id, expiry_minutes=expiry_minutes)

    # Log token generation (optional - for audit)
    from datetime import timedelta
    expires_at = timezone.now() + timedelta(minutes=expiry_minutes)

    # Get client IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    TemporaryTokenLog.objects.create(
        equipment=equipment,
        token=token,
        created_by=request.user,
        expires_at=expires_at,
        expiry_minutes=expiry_minutes,
        generated_from_ip=ip
    )

    # Generate full URL
    protocol = 'https' if request.is_secure() else 'http'
    host = request.get_host()
    url = f"{protocol}://{host}/temp-log/{token}/"

    logger.info(f"Temporary token generated for equipment {equipment_id} by user {request.user.id}")

    return JsonResponse({
        'token': token,
        'url': url,
        'equipment_id': equipment_id,
        'equipment_name': equipment.name,
        'serial_number': equipment.serial_number,
        'facility': equipment.facility.name,
        'expires_in_minutes': expiry_minutes,
        'expires_at': expires_at.isoformat(),
        'temporary': True,
        'message': f'Token válido por {expiry_minutes} minutos'
    })


def temp_log_form(request, token):
    """
    Display form with expirable token and optional technician authentication

    - If technician is logged in, links cleaning to their account
    - Otherwise, allows anonymous submission
    - Token must be valid (5-minute expiry)
    """
    from .tokens import validate_expirable_token, get_token_expiry_info
    from .models import TemporaryTokenLog

    # Validate token
    equipment_id = validate_expirable_token(token)

    if equipment_id is None:
        # Token expired or invalid
        expiry_info = get_token_expiry_info(token)
        context = {
            'error': 'Token Expirado ou Inválido',
            'message': 'Este link expirou (válido por 5 minutos). Solicite um novo link ao administrador.',
            'expiry_info': expiry_info
        }
        return render(request, 'cleaning_logs/token_expired.html', context, status=403)

    # Get equipment
    equipment = get_object_or_404(Equipment, id=equipment_id, is_active=True)

    # Get expiry info
    expiry_info = get_token_expiry_info(token)

    # Check if user is authenticated technician
    cleaned_by = None
    if request.user.is_authenticated:
        if hasattr(request.user, 'role') and request.user.role == 'technician':
            cleaned_by = request.user
            logger.info(f"Technician {request.user.id} accessing temporary token for equipment {equipment.id}")

    # Track token access (optional)
    try:
        token_log = TemporaryTokenLog.objects.filter(token=token).first()
        if token_log:
            token_log.increment_access()
    except Exception as e:
        logger.warning(f"Failed to track token access: {e}")

    return render(request, 'cleaning_logs/public_log_form.html', {
        'equipment': equipment,
        'form': PublicCleaningLogForm(),
        'token': token,
        'expiry_info': expiry_info,
        'is_temporary': True,
        'logged_in_user': cleaned_by,
        'is_technician_authenticated': cleaned_by is not None
    })


@csrf_exempt
@require_http_methods(["POST"])
def temp_log_submit(request, token):
    """
    Submit cleaning log with expirable token and optional technician authentication

    - If technician is logged in, links cleaning to their account
    - Otherwise, creates anonymous cleaning log
    - Validates token expiry and marks as used
    """
    from .tokens import validate_expirable_token
    from .models import TemporaryTokenLog

    # Validate token
    equipment_id = validate_expirable_token(token)

    if equipment_id is None:
        return HttpResponse(
            '<div class="alert alert-danger">❌ Token expirado ou inválido. '
            'Solicite um novo link ao administrador.</div>',
            status=403
        )

    # Get equipment
    equipment = get_object_or_404(Equipment, id=equipment_id, is_active=True)

    # Check if user is authenticated technician
    cleaned_by = None
    if request.user.is_authenticated:
        if hasattr(request.user, 'role') and request.user.role == 'technician':
            cleaned_by = request.user

    # Process form
    form = PublicCleaningLogForm(request.POST, request.FILES)

    if form.is_valid():
        try:
            log = CleaningLog.objects.create(
                equipment=equipment,
                cleaned_by=cleaned_by,  # Link to technician if authenticated
                cleaned_at=timezone.now(),
                notes=form.cleaned_data['notes'],
                photo=form.cleaned_data['photo'],
                is_compliant=True
            )

            # Mark token as used (optional)
            try:
                token_log = TemporaryTokenLog.objects.filter(token=token).first()
                if token_log:
                    token_log.mark_as_used()
            except Exception as e:
                logger.warning(f"Failed to mark token as used: {e}")

            # Log with appropriate message
            if cleaned_by:
                logger.info(f"Authenticated temp token cleaning log created: {log.id} by technician {cleaned_by.id} for equipment {equipment.id}")
                user_msg = f"✅ Limpeza registrada por {cleaned_by.get_full_name() or cleaned_by.email}!"
            else:
                logger.info(f"Anonymous temp token cleaning log created: {log.id} for equipment {equipment.id}")
                user_msg = "✅ Limpeza registrada com sucesso!"

            return HttpResponse(f'''
                <div class="alert alert-success">{user_msg}</div>
                <p class="text-muted">Este link temporário expirou. Para registrar outra limpeza,
                solicite um novo link ao administrador.</p>
            ''')
        except Exception as e:
            logger.error(f"Error creating cleaning log: {e}")
            return HttpResponse('<div class="alert alert-danger">❌ Erro ao salvar. Tente novamente.</div>')
    else:
        return HttpResponse(f'<div class="alert alert-warning">⚠️ {form.errors}</div>')


# ============================================================================
# PDF GENERATION
# ============================================================================

@require_http_methods(["GET"])
@login_required
def generate_equipment_labels_pdf(request):
    """
    Generate PDF with printable labels for equipment QR codes

    URL: /admin-api/equipment/generate-labels-pdf/
    Query params:
        - equipment_ids: comma-separated list of equipment IDs (optional)
        - facility_id: filter by facility (optional)
    """
    from io import BytesIO
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.units import inch, mm
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    import qrcode
    from django.conf import settings
    import os

    # Get equipment to print
    equipment_ids = request.GET.get('equipment_ids')
    facility_id = request.GET.get('facility_id')

    # Build queryset
    qs = Equipment.objects.filter(is_active=True)

    # Permission check
    if not request.user.is_superuser:
        qs = qs.filter(facility__managers=request.user)

    if equipment_ids:
        ids = [int(id.strip()) for id in equipment_ids.split(',')]
        qs = qs.filter(id__in=ids)

    if facility_id:
        qs = qs.filter(facility_id=facility_id)

    equipment_list = qs.select_related('facility').order_by('facility__name', 'name')

    if not equipment_list.exists():
        return JsonResponse({'error': 'No equipment found'}, status=404)

    # Create PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Label dimensions (A4 with 2 columns, 4 rows per page)
    label_width = width / 2
    label_height = height / 4
    padding = 10 * mm

    # Current position
    col = 0
    row = 0

    for equipment in equipment_list:
        # Calculate position
        x = col * label_width + padding
        y = height - ((row + 1) * label_height) + padding

        # Generate QR code in memory
        protocol = 'https' if request.is_secure() else 'http'
        host = request.get_host()
        qr_url = f"{protocol}://{host}/log/{equipment.public_token}/"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(qr_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Save QR to BytesIO
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        qr_reader = ImageReader(qr_buffer)

        # Draw label border
        p.setStrokeColorRGB(0.8, 0.8, 0.8)
        p.rect(x, y, label_width - 2*padding, label_height - 2*padding)

        # Draw QR code
        qr_size = 60 * mm
        qr_x = x + (label_width - 2*padding - qr_size) / 2
        qr_y = y + label_height - 2*padding - qr_size - 5*mm
        p.drawImage(qr_reader, qr_x, qr_y, width=qr_size, height=qr_size)

        # Draw equipment info
        text_y = qr_y - 5*mm

        # Equipment name (bold)
        p.setFont("Helvetica-Bold", 12)
        p.drawCentredString(
            x + label_width/2 - padding,
            text_y,
            equipment.name[:35]
        )

        # Serial number
        p.setFont("Helvetica", 10)
        text_y -= 4*mm
        p.drawCentredString(
            x + label_width/2 - padding,
            text_y,
            f"SN: {equipment.serial_number[:30]}"
        )

        # Facility
        p.setFont("Helvetica", 9)
        text_y -= 4*mm
        p.drawCentredString(
            x + label_width/2 - padding,
            text_y,
            equipment.facility.name[:35]
        )

        # Location (if available)
        if equipment.location:
            p.setFont("Helvetica", 8)
            p.setFillColorRGB(0.4, 0.4, 0.4)
            text_y -= 3.5*mm
            p.drawCentredString(
                x + label_width/2 - padding,
                text_y,
                f"Local: {equipment.location[:30]}"
            )
            p.setFillColorRGB(0, 0, 0)

        # Instructions
        p.setFont("Helvetica", 7)
        p.setFillColorRGB(0.3, 0.3, 0.3)
        text_y -= 3.5*mm
        p.drawCentredString(
            x + label_width/2 - padding,
            text_y,
            "Escaneie para registrar limpeza"
        )
        p.setFillColorRGB(0, 0, 0)

        # Move to next position
        col += 1
        if col >= 2:  # 2 columns
            col = 0
            row += 1
            if row >= 4:  # 4 rows per page
                row = 0
                p.showPage()  # New page

    # Save PDF
    p.save()
    buffer.seek(0)

    # Return PDF response
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="equipment_labels_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf"'

    logger.info(f"Generated PDF labels for {equipment_list.count()} equipment by user {request.user.id}")

    return response
