"""
Admin configuration for Documentation app
"""
from django.contrib import admin
from .models import FeatureCategory, Feature


@admin.register(FeatureCategory)
class FeatureCategoryAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'slug', 'order', 'is_active', 'feature_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']

    def feature_count(self, obj):
        """Display count of features in this category"""
        return obj.features.count()
    feature_count.short_description = 'Funcionalidades'


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'badge', 'requires_auth', 'is_featured', 'is_active', 'order']
    list_filter = ['category', 'badge', 'requires_auth', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'endpoint', 'code_example']
    list_editable = ['is_featured', 'is_active', 'order']
    ordering = ['category', 'order', 'name']

    fieldsets = [
        ('Informações Básicas', {
            'fields': ['category', 'name', 'description']
        }),
        ('Detalhes Técnicos', {
            'fields': ['endpoint', 'code_example']
        }),
        ('Classificação', {
            'fields': ['badge', 'is_featured', 'requires_auth', 'requires_permission']
        }),
        ('Exibição', {
            'fields': ['order', 'is_active']
        }),
    ]
