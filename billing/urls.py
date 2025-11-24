"""
Billing URL Configuration
"""
from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    # Stripe webhook endpoint
    path('webhooks/stripe/', views.stripe_webhook, name='stripe_webhook'),
]
