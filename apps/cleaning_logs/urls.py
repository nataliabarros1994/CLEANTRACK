from django.urls import path
from . import views

app_name = "cleaning_logs"

urlpatterns = [
    # Authenticated cleaning registration
    path("register/<int:equipment_id>/", views.register_cleaning, name="register_cleaning"),
    path("success/<int:equipment_id>/", views.cleaning_success, name="cleaning_success"),

    # Public QR code cleaning registration (permanent tokens)
    path('log/<str:token>/', views.public_log_form, name='public_log_form'),
    path('log/<str:token>/submit/', views.public_log_submit, name='public_log_submit'),

    # Expirable tokens (5 minutes)
    path('temp-log/<str:token>/', views.temp_log_form, name='temp_log_form'),
    path('temp-log/<str:token>/submit/', views.temp_log_submit, name='temp_log_submit'),

    # Admin API endpoints
    path('admin-api/equipment/<int:equipment_id>/qr-token/', views.get_equipment_qr_token, name='get_equipment_qr_token'),
    path('admin-api/equipment/<int:equipment_id>/generate-temp-token/', views.generate_expirable_token_view, name='generate_expirable_token'),
    path('admin-api/equipment/generate-labels-pdf/', views.generate_equipment_labels_pdf, name='generate_labels_pdf'),
]
