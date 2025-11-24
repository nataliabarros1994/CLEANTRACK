"""
URL configuration for Equipment app
"""
from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns = [
    # PDF generation for equipment labels
    path('labels/pdf/<int:facility_id>/', views.generate_labels_pdf, name='generate_labels_pdf'),
]
