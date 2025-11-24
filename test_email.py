#!/usr/bin/env python
"""
Script to test email sending via Resend
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cleantrack.settings')
django.setup()

from apps.notifications.services import (
    send_welcome_email,
    send_cleaning_alert,
    send_compliance_summary
)
from django.conf import settings


def test_welcome_email():
    """Test welcome email"""
    print("=" * 70)
    print("  TESTE DE E-MAIL - Welcome Email")
    print("=" * 70)
    print()

    # Resend only allows sending to verified email in test mode
    test_email = "natyssis23@gmail.com"  # Your email from settings

    print(f"📧 Enviando e-mail de boas-vindas para: {test_email}")
    print()

    try:
        response = send_welcome_email(test_email, "Natália Barros")

        if response:
            print("✅ E-mail enviado com sucesso!")
            print(f"   Response: {response}")
        else:
            print("❌ Falha ao enviar e-mail")

    except Exception as e:
        print(f"❌ Erro: {e}")

    print()


def test_cleaning_alert():
    """Test cleaning alert email"""
    print("=" * 70)
    print("  TESTE DE E-MAIL - Cleaning Alert")
    print("=" * 70)
    print()

    test_email = "natyssis23@gmail.com"

    print(f"📧 Enviando alerta de limpeza para: {test_email}")
    print()

    try:
        response = send_cleaning_alert(test_email, "Ultrassom GE LOGIQ P9")

        if response:
            print("✅ Alerta enviado com sucesso!")
            print(f"   Response: {response}")
        else:
            print("❌ Falha ao enviar alerta")

    except Exception as e:
        print(f"❌ Erro: {e}")

    print()


def test_compliance_summary():
    """Test compliance summary email"""
    print("=" * 70)
    print("  TESTE DE E-MAIL - Compliance Summary")
    print("=" * 70)
    print()

    test_email = "natyssis23@gmail.com"

    summary_data = {
        'total_equipment': 5,
        'cleanings_completed': 12,
        'overdue_count': 2,
        'compliance_rate': 85.5
    }

    print(f"📧 Enviando resumo de conformidade para: {test_email}")
    print(f"   Dados: {summary_data}")
    print()

    try:
        response = send_compliance_summary(test_email, summary_data)

        if response:
            print("✅ Resumo enviado com sucesso!")
            print(f"   Response: {response}")
        else:
            print("❌ Falha ao enviar resumo")

    except Exception as e:
        print(f"❌ Erro: {e}")

    print()


def main():
    """Run all email tests"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║                                                                      ║")
    print("║                  📧 TESTES DE E-MAIL - RESEND API                   ║")
    print("║                                                                      ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print("\n")

    print("⚠️  NOTA IMPORTANTE:")
    print("   No modo de teste do Resend, e-mails só podem ser enviados para:")
    print("   natyssis23@gmail.com (seu e-mail verificado)")
    print()
    print("   Para enviar para outros destinatários, verifique um domínio em:")
    print("   https://resend.com/domains")
    print()
    print("=" * 70)
    print()

    # Run tests
    test_welcome_email()
    test_cleaning_alert()
    test_compliance_summary()

    print()
    print("=" * 70)
    print("  TESTES CONCLUÍDOS")
    print("=" * 70)
    print()
    print("📬 Verifique sua caixa de entrada: natyssis23@gmail.com")
    print("   Você deve ter recebido 3 e-mails:")
    print("   1. Bem-vindo ao CleanTrack!")
    print("   2. ⚠️ Limpeza atrasada")
    print("   3. 📊 Resumo Semanal de Conformidade")
    print()


if __name__ == '__main__':
    main()
