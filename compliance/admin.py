from django.contrib import admin
from .models import CleaningLog, ComplianceAlert, AuditReport


@admin.register(CleaningLog)
class CleaningLogAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'performed_by', 'completed_at', 'duration', 'validation_status', 'source']
    list_filter = ['validation_status', 'source', 'completed_at', 'equipment__location__account']
    search_fields = ['equipment__name', 'performed_by__email']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'completed_at'

    fieldsets = (
        (None, {'fields': ('equipment', 'performed_by', 'source')}),
        ('Timing', {'fields': ('started_at', 'completed_at', 'duration')}),
        ('Protocol', {'fields': ('protocol_version', 'chemicals_used', 'steps_completed')}),
        ('Validation', {'fields': ('contact_time_met', 'all_steps_completed', 'validation_status', 'validated_by', 'validated_at')}),
        ('Evidence', {'fields': ('photo_before', 'photo_after')}),
        ('IoT', {'fields': ('iot_sensor_data',)}),
        ('Notes', {'fields': ('notes', 'issues_found')}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(ComplianceAlert)
class ComplianceAlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'equipment', 'alert_type', 'severity', 'status', 'created_at']
    list_filter = ['alert_type', 'severity', 'status', 'created_at']
    search_fields = ['title', 'equipment__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {'fields': ('equipment', 'alert_type', 'severity', 'status')}),
        ('Details', {'fields': ('title', 'message', 'suggested_action', 'due_by')}),
        ('Assignment', {'fields': ('assigned_to', 'acknowledged_by', 'acknowledged_at')}),
        ('Resolution', {'fields': ('resolved_by', 'resolved_at', 'resolution_notes')}),
        ('Related', {'fields': ('related_cleaning_log',)}),
        ('Notifications', {'fields': ('email_sent', 'email_sent_at')}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(AuditReport)
class AuditReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'location', 'start_date', 'end_date', 'generated_by', 'created_at']
    list_filter = ['report_type', 'created_at', 'location__account']
    search_fields = ['title', 'location__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
