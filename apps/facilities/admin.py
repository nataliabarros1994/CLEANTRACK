from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Facility


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'is_active', 'equipment_count', 'generate_pdf_button', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'address']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'address', 'is_active')
        }),
        ('Billing', {
            'fields': ('stripe_customer_id',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

    def equipment_count(self, obj):
        """Display count of active equipment in this facility"""
        count = obj.equipment_set.filter(is_active=True).count()
        return f"{count} equipamento(s)"
    equipment_count.short_description = "Equipamentos Ativos"

    def generate_pdf_button(self, obj):
        """Generate PDF button in list view"""
        if obj.pk:
            url = reverse('equipment:generate_labels_pdf', args=[obj.pk])
            return format_html(
                '<a class="button" href="{}" target="_blank" '
                'style="background: #28a745; color: white; padding: 5px 10px; '
                'border-radius: 4px; text-decoration: none; font-size: 12px; '
                'display: inline-block;">'
                '🖨️ PDF</a>',
                url
            )
        return "-"
    generate_pdf_button.short_description = "PDF Etiquetas"

    def get_queryset(self, request):
        """
        Filter facilities based on user role:
        - Superusers see everything
        - Managers/Technicians see only their assigned facilities
        """
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        # Managers and technicians see only their facilities
        return qs.filter(managers=request.user)

    def has_change_permission(self, request, obj=None):
        """
        Managers can edit their facilities
        Technicians have read-only access
        """
        if request.user.is_superuser:
            return True

        if obj is None:
            return request.user.role == 'manager'

        # Check if user manages this facility
        if request.user.role == 'manager':
            return obj.managers.filter(id=request.user.id).exists()

        return False

    def has_delete_permission(self, request, obj=None):
        """Only superusers and managers can delete their own facilities"""
        if request.user.is_superuser:
            return True

        if obj is None:
            return request.user.role == 'manager'

        if request.user.role == 'manager':
            return obj.managers.filter(id=request.user.id).exists()

        return False

    def has_add_permission(self, request):
        """Only superusers and managers can add facilities"""
        return request.user.is_superuser or request.user.role == 'manager'
