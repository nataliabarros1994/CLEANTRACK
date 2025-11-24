#!/usr/bin/env python
"""
Script to test Stripe webhook handling locally
Simulates a checkout.session.completed event
"""

import os
import sys
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cleantrack.settings')
django.setup()

from apps.facilities.models import Facility
from apps.billing.views import handle_checkout_completed


def test_checkout_completed():
    """
    Test checkout.session.completed webhook handler
    """
    print("=" * 70)
    print("  TESTE DE WEBHOOK - checkout.session.completed")
    print("=" * 70)
    print()

    # Get a test facility
    facility = Facility.objects.first()

    if not facility:
        print("❌ Nenhuma facility encontrada para teste")
        return

    print(f"📦 Facility de teste: {facility.name}")
    print(f"   ID: {facility.id}")
    print(f"   Status atual: {'Ativa' if facility.is_active else 'Inativa'}")
    print()

    # Create mock checkout session data
    mock_session = {
        'id': 'cs_test_123456',
        'object': 'checkout.session',
        'customer': 'cus_test_123456',
        'customer_details': {
            'email': 'teste@cleantrack.com',
            'name': 'Usuário Teste'
        },
        'metadata': {
            'facility_id': str(facility.id)
        },
        'payment_status': 'paid',
        'status': 'complete'
    }

    print("📨 Simulando evento checkout.session.completed...")
    print(f"   Email: {mock_session['customer_details']['email']}")
    print(f"   Facility ID: {mock_session['metadata']['facility_id']}")
    print()

    # Call the handler
    try:
        handle_checkout_completed(mock_session)

        # Verify facility was activated
        facility.refresh_from_db()

        print()
        print("=" * 70)
        print("  RESULTADO DO TESTE")
        print("=" * 70)
        print()

        if facility.is_active:
            print("✅ SUCESSO! Facility foi ativada")
            print(f"   Nome: {facility.name}")
            print(f"   Status: Ativa")
            print(f"   Stripe Customer ID: {facility.stripe_customer_id}")
        else:
            print("❌ FALHA! Facility não foi ativada")

        print()
        print("📧 Verifique se o e-mail de boas-vindas foi enviado")
        print(f"   Destinatário: {mock_session['customer_details']['email']}")

    except Exception as e:
        print(f"❌ ERRO ao processar webhook: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_checkout_completed()
