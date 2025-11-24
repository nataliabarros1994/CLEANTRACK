from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Equipment
import qrcode
from io import BytesIO
import base64


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'serial_number', 'facility', 'is_active', 'qr_code_preview', 'token_status']
    list_filter = ['is_active', 'facility', 'category', 'created_at']
    search_fields = ['name', 'serial_number', 'description', 'location']
    raw_id_fields = ['facility']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Dados Básicos', {
            'fields': ('name', 'serial_number', 'facility', 'category', 'location', 'description', 'cleaning_frequency_hours', 'is_active')
        }),
        ('QR Code (Token Público)', {
            'fields': ('qr_code_full', 'public_token', 'token_created_at'),
            'description': 'Use este QR code para registrar limpezas rapidamente. O token expira em 5 minutos após ser gerado.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['qr_code_full', 'public_token', 'token_created_at', 'created_at', 'updated_at']

    def qr_code_preview(self, obj):
        """Small QR code preview for list view"""
        if obj.public_token:
            qr = qrcode.QRCode(version=1, box_size=3, border=2)
            full_url = f"http://localhost:8000/log/{obj.public_token}/"
            qr.add_data(full_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode()
            return format_html('<img src="data:image/png;base64,{}" width="60" height="60" />', img_str)
        return "Sem token"
    qr_code_preview.short_description = "QR Code"

    def qr_code_full(self, obj):
        """Full QR code display for detail view"""
        if obj.public_token:
            # Regenerate token when accessing this page
            obj._generate_new_token()
            obj.save(update_fields=['public_token', 'token_created_at'])

            qr = qrcode.QRCode(version=1, box_size=8, border=4)
            full_url = f"http://localhost:8000/log/{obj.public_token}/"
            qr.add_data(full_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode()
            return format_html(
                '<div style="text-align:center;"><img src="data:image/png;base64,{}" /><br/>'
                '<small>Link: {}</small><br/>'
                '<small style="color:green;">✅ Token válido por 5 minutos a partir de {}</small></div>',
                img_str,
                full_url,
                obj.token_created_at.strftime("%H:%M:%S") if obj.token_created_at else "—"
            )
        return "Clique em 'Salvar' para gerar um novo QR Code"
    qr_code_full.short_description = "QR Code para Impressão"

    def token_status(self, obj):
        """Display token validity status"""
        if obj.is_token_valid():
            from datetime import timedelta
            remaining = (obj.token_created_at + timedelta(minutes=5) - timezone.now()).total_seconds() // 60
            return format_html('<span style="color:green;">✅ Válido (~{} min)</span>', int(remaining) + 1)
        return format_html('<span style="color:orange;">⏳ Expirado</span>')
    token_status.short_description = "Status do Token"

    def get_queryset(self, request):
        """
        Filter equipment based on user's assigned facilities
        """
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        # Filter by user's managed facilities
        return qs.filter(facility__managers=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Limit facility choices to user's managed facilities
        """
        if db_field.name == "facility" and not request.user.is_superuser:
            kwargs["queryset"] = request.user.managed_facilities.all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        """Managers can edit, technicians have read-only"""
        if request.user.is_superuser:
            return True

        if obj is None:
            return request.user.role == 'manager'

        # Check if user has access to this equipment's facility
        if request.user.role == 'manager':
            return obj.facility.managers.filter(id=request.user.id).exists()

        return False

    def has_delete_permission(self, request, obj=None):
        """Only managers can delete equipment in their facilities"""
        if request.user.is_superuser:
            return True

        if obj is None:
            return request.user.role == 'manager'

        if request.user.role == 'manager':
            return obj.facility.managers.filter(id=request.user.id).exists()

        return False

    def has_add_permission(self, request):
        """Only superusers and managers can add equipment"""
        return request.user.is_superuser or request.user.role == 'manager'

    qr_code_preview.short_description = 'QR Code Preview'

    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue?'

    actions = ['regenerate_qr_codes', 'generate_pdf_labels']

    def regenerate_qr_codes(self, request, queryset):
        """Admin action to regenerate QR codes for selected equipment"""
        count = 0
        for equipment in queryset:
            equipment.generate_qr_code()
            equipment.save(update_fields=['qr_code'])
            count += 1
        self.message_user(request, f'✅ {count} QR codes regenerados com sucesso!')
    regenerate_qr_codes.short_description = '🔄 Regenerar QR Codes selecionados'

    def generate_pdf_labels(self, request, queryset):
        """Admin action to generate PDF labels for selected equipment"""
        from django.http import HttpResponse
        from io import BytesIO
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader
        import qrcode
        from django.utils import timezone

        equipment_list = queryset.select_related('facility').order_by('facility__name', 'name')

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
            # Regenerate token for fresh QR code
            equipment._generate_new_token()
            equipment.save(update_fields=['public_token', 'token_created_at'])

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

            # Token validity warning
            p.setFont("Helvetica", 7)
            p.setFillColorRGB(0.8, 0, 0)
            text_y -= 3.5*mm
            p.drawCentredString(
                x + label_width/2 - padding,
                text_y,
                "⏱ Válido por 5 minutos"
            )
            p.setFillColorRGB(0, 0, 0)

            # Instructions
            p.setFont("Helvetica", 7)
            p.setFillColorRGB(0.3, 0.3, 0.3)
            text_y -= 3*mm
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

        return response

    generate_pdf_labels.short_description = '📄 Gerar PDF com Etiquetas QR Code'
