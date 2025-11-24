"""
URL patterns for billing webhooks
"""
from django.urls import path
from . import views

app_name = "billing"

urlpatterns = [
    # Stripe webhook endpoint
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]
