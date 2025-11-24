#!/usr/bin/env python
"""
Script para testar webhook handlers do Stripe localmente

Uso:
    python manage.py shell < apps/billing/test_webhooks.py

Ou diretamente:
    python apps/billing/test_webhooks.py
"""

import os
import django
import json

# Setup Django (caso rode diretamente)
if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cleantrack.settings')
    django.setup()

from apps.billing.webhook_handlers import (
    handle_checkout_session_completed,
    handle_subscription_created,
    handle_subscription_updated,
    handle_subscription_deleted,
    handle_payment_succeeded,
    handle_payment_failed,
)
from apps.facilities.models import Facility
from apps.accounts.models import Account, User


class MockEvent:
    """Mock Stripe event for testing"""
    def __init__(self, event_type, data):
        self.type = event_type
        self.data = {"object": data}


def test_checkout_completed():
    """Test checkout.session.completed webhook"""
    print("\n" + "="*60)
    print("Testing checkout.session.completed webhook")
    print("="*60)

    # Create or get a test facility
    facility, created = Facility.objects.get_or_create(
        name="Test Facility",
        defaults={'address': 'Test Address'}
    )
    print(f"Using facility: {facility.name} (ID: {facility.id})")

    # Mock checkout session data
    session_data = {
        "id": "cs_test_123",
        "customer": "cus_test_123",
        "client_reference_id": str(facility.id),
        "metadata": {
            "facility_id": str(facility.id)
        }
    }

    # Create mock event
    event = MockEvent("checkout.session.completed", session_data)

    # Call handler
    print("Calling handle_checkout_session_completed...")
    try:
        handle_checkout_session_completed(event)
        print("\n✅ Handler executed successfully")

        # Verify facility was activated
        facility.refresh_from_db()
        print(f"Facility is_active: {facility.is_active}")
        print(f"Facility stripe_customer_id: {facility.stripe_customer_id}")

    except Exception as e:
        print(f"\n❌ Error: {e}")


def test_subscription_created():
    """Test customer.subscription.created webhook"""
    print("\n" + "="*60)
    print("Testing customer.subscription.created webhook")
    print("="*60)

    facility = Facility.objects.first()
    if not facility:
        print("❌ No facility found. Create one first.")
        return

    print(f"Using facility: {facility.name} (ID: {facility.id})")

    # Mock subscription data
    subscription_data = {
        "id": "sub_test_123",
        "customer": "cus_test_456",
        "status": "active",
        "metadata": {
            "facility_id": str(facility.id)
        }
    }

    event = MockEvent("customer.subscription.created", subscription_data)

    print("Calling handle_subscription_created...")
    try:
        handle_subscription_created(event)
        print("\n✅ Handler executed successfully")

        facility.refresh_from_db()
        print(f"Facility is_active: {facility.is_active}")
        print(f"Facility stripe_customer_id: {facility.stripe_customer_id}")

    except Exception as e:
        print(f"\n❌ Error: {e}")


def test_subscription_updated():
    """Test customer.subscription.updated webhook"""
    print("\n" + "="*60)
    print("Testing customer.subscription.updated webhook")
    print("="*60)

    # Create facility with customer_id
    facility, _ = Facility.objects.get_or_create(
        name="Test Facility for Update",
        defaults={
            'address': 'Test Address',
            'stripe_customer_id': 'cus_test_update'
        }
    )

    print(f"Using facility: {facility.name}")
    print(f"Initial is_active: {facility.is_active}")

    # Test 1: Update to 'active' status
    print("\nTest 1: Update to 'active' status")
    subscription_data = {
        "id": "sub_test_update",
        "customer": "cus_test_update",
        "status": "active"
    }

    event = MockEvent("customer.subscription.updated", subscription_data)
    handle_subscription_updated(event)

    facility.refresh_from_db()
    print(f"After 'active' update - is_active: {facility.is_active}")

    # Test 2: Update to 'canceled' status
    print("\nTest 2: Update to 'canceled' status")
    subscription_data["status"] = "canceled"
    event = MockEvent("customer.subscription.updated", subscription_data)
    handle_subscription_updated(event)

    facility.refresh_from_db()
    print(f"After 'canceled' update - is_active: {facility.is_active}")


def test_payment_failed():
    """Test invoice.payment_failed webhook"""
    print("\n" + "="*60)
    print("Testing invoice.payment_failed webhook")
    print("="*60)

    facility, _ = Facility.objects.get_or_create(
        name="Test Facility for Payment",
        defaults={
            'address': 'Test Address',
            'stripe_customer_id': 'cus_test_payment',
            'is_active': True
        }
    )

    print(f"Using facility: {facility.name}")
    print(f"Initial is_active: {facility.is_active}")

    # Test with 3 failed attempts (should deactivate)
    print("\nSimulating 3 failed payment attempts...")
    invoice_data = {
        "id": "in_test_failed",
        "customer": "cus_test_payment",
        "amount_due": 4999,  # $49.99
        "attempt_count": 3,
        "currency": "usd"
    }

    event = MockEvent("invoice.payment_failed", invoice_data)
    handle_payment_failed(event)

    facility.refresh_from_db()
    print(f"After 3 failed attempts - is_active: {facility.is_active}")


def main():
    """Menu principal"""
    while True:
        print("\n" + "="*60)
        print("STRIPE WEBHOOK TESTING MENU")
        print("="*60)
        print("1. Test checkout.session.completed")
        print("2. Test customer.subscription.created")
        print("3. Test customer.subscription.updated")
        print("4. Test invoice.payment_failed")
        print("5. Run all tests")
        print("0. Exit")
        print("="*60)

        choice = input("Choose an option: ").strip()

        if choice == '1':
            test_checkout_completed()
        elif choice == '2':
            test_subscription_created()
        elif choice == '3':
            test_subscription_updated()
        elif choice == '4':
            test_payment_failed()
        elif choice == '5':
            test_checkout_completed()
            test_subscription_created()
            test_subscription_updated()
            test_payment_failed()
        elif choice == '0':
            print("\nExiting...")
            break
        else:
            print("\n❌ Invalid option!")

        input("\nPress ENTER to continue...")


if __name__ == "__main__":
    main()
