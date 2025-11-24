from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Account, Location, AccountMembership


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'owner', 'plan', 'status', 'created_at']
    list_filter = ['plan', 'status', 'created_at']
    search_fields = ['name', 'slug', 'owner__email']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {'fields': ('name', 'slug', 'owner', 'plan', 'status')}),
        ('Subscription', {'fields': ('stripe_customer_id', 'stripe_subscription_id', 'subscription_end_date')}),
        ('Limits', {'fields': ('max_locations', 'max_users')}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'account', 'city', 'state', 'is_active', 'created_at']
    list_filter = ['is_active', 'account', 'state']
    search_fields = ['name', 'city', 'account__name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {'fields': ('account', 'name', 'is_active')}),
        ('Address', {'fields': ('address', 'city', 'state', 'zip_code', 'country')}),
        ('Contact', {'fields': ('contact_name', 'contact_email', 'contact_phone')}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(AccountMembership)
class AccountMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'account', 'role', 'created_at']
    list_filter = ['role', 'account']
    search_fields = ['user__email', 'account__name']
    filter_horizontal = ['locations']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {'fields': ('user', 'account', 'role')}),
        ('Locations', {'fields': ('locations',)}),
        ('Permissions', {'fields': (
            'can_manage_users',
            'can_manage_equipment',
            'can_log_cleaning',
            'can_view_reports',
            'can_export_data',
        )}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )
