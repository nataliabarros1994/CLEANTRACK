from django.contrib import admin
from .models import EquipmentType, CleaningProtocol, Equipment


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'requires_fda_compliance', 'requires_daily_cleaning', 'default_cleaning_frequency']
    list_filter = ['requires_fda_compliance', 'requires_daily_cleaning']
    search_fields = ['name']


@admin.register(CleaningProtocol)
class CleaningProtocolAdmin(admin.ModelAdmin):
    list_display = ['name', 'equipment_type', 'version', 'is_active', 'estimated_duration']
    list_filter = ['equipment_type', 'is_active']
    search_fields = ['name', 'equipment_type__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'serial_number', 'equipment_type', 'location', 'status', 'last_cleaned_at', 'next_cleaning_due']
    list_filter = ['status', 'equipment_type', 'location__account', 'is_iot_enabled']
    search_fields = ['name', 'serial_number', 'asset_tag', 'qr_code']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {'fields': ('location', 'equipment_type', 'protocol', 'name', 'status')}),
        ('Identification', {'fields': ('serial_number', 'asset_tag', 'qr_code')}),
        ('Details', {'fields': ('manufacturer', 'model_number', 'purchase_date')}),
        ('Cleaning Schedule', {'fields': ('cleaning_frequency', 'last_cleaned_at', 'next_cleaning_due')}),
        ('IoT', {'fields': ('is_iot_enabled', 'iot_device_id')}),
        ('Notes', {'fields': ('notes',)}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )
