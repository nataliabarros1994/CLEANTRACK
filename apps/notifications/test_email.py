#!/usr/bin/env python
"""
Script de teste para serviço de notificações por email

Uso:
    python manage.py shell < apps/notifications/test_email.py

Ou diretamente:
    python apps/notifications/test_email.py
"""

import os
import django

# Setup Django (caso rode diretamente)
if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cleantrack.settings')
    django.setup()

from apps.notifications.services import (
    send_welcome_email,
    send_cleaning_alert,
    send_compliance_summary,
    notify_cleaning_registered
)
from apps.cleaning_logs.models import CleaningLog


def test_welcome_email():
    """Testa envio de email de boas-vindas"""
    print("\n" + "="*60)
    print("Testando envio de email de boas-vindas...")
    print("="*60)

    email = input("Digite seu email para teste: ").strip()
    name = input("Digite seu nome: ").strip()

    if not email or not name:
        print("Email e nome são obrigatórios!")
        return

    result = send_welcome_email(email, name)

    if result:
        print(f"\n✅ Email enviado com sucesso!")
        print(f"Response: {result}")
    else:
        print("\n❌ Erro ao enviar email. Verifique os logs.")


def test_cleaning_alert():
    """Testa envio de alerta de limpeza atrasada"""
    print("\n" + "="*60)
    print("Testando envio de alerta de limpeza...")
    print("="*60)

    email = input("Digite seu email para teste: ").strip()

    if not email:
        print("Email é obrigatório!")
        return

    result = send_cleaning_alert(
        to_email=email,
        equipment_name="Autoclave 123 (Unidade Central) - LIMPEZA FORA DO PRAZO"
    )

    if result:
        print(f"\n✅ Alerta enviado com sucesso!")
        print(f"Response: {result}")
    else:
        print("\n❌ Erro ao enviar alerta. Verifique os logs.")


def test_compliance_summary():
    """Testa envio de resumo de conformidade"""
    print("\n" + "="*60)
    print("Testando envio de resumo de conformidade...")
    print("="*60)

    email = input("Digite seu email para teste: ").strip()

    if not email:
        print("Email é obrigatório!")
        return

    summary_data = {
        'total_equipment': 50,
        'cleanings_completed': 120,
        'overdue_count': 3,
        'compliance_rate': 94.0
    }

    result = send_compliance_summary(email, summary_data)

    if result:
        print(f"\n✅ Resumo enviado com sucesso!")
        print(f"Response: {result}")
    else:
        print("\n❌ Erro ao enviar resumo. Verifique os logs.")


def test_cleaning_registered():
    """Testa notificação de limpeza registrada"""
    print("\n" + "="*60)
    print("Testando notificação de limpeza registrada...")
    print("="*60)

    # Buscar último registro de limpeza
    last_cleaning = CleaningLog.objects.order_by('-created_at').first()

    if not last_cleaning:
        print("❌ Nenhum registro de limpeza encontrado no banco de dados.")
        print("Crie um registro primeiro através do admin Django.")
        return

    print(f"Usando registro de limpeza:")
    print(f"  - Equipamento: {last_cleaning.equipment.name}")
    print(f"  - Data: {last_cleaning.cleaned_at}")
    print(f"  - Conformidade: {'Sim' if last_cleaning.is_compliant else 'Não'}")

    confirm = input("\nDeseja enviar notificação para os gerentes? (s/n): ").strip().lower()

    if confirm != 's':
        print("Cancelado.")
        return

    result = notify_cleaning_registered(last_cleaning)

    if result:
        print(f"\n✅ Notificação enviada com sucesso!")
        print(f"Response: {result}")
    else:
        print("\n❌ Erro ao enviar notificação. Verifique os logs.")


def main():
    """Menu principal"""
    while True:
        print("\n" + "="*60)
        print("MENU DE TESTES - SERVIÇO DE NOTIFICAÇÕES")
        print("="*60)
        print("1. Testar email de boas-vindas")
        print("2. Testar alerta de limpeza atrasada")
        print("3. Testar resumo de conformidade")
        print("4. Testar notificação de limpeza registrada")
        print("0. Sair")
        print("="*60)

        choice = input("Escolha uma opção: ").strip()

        if choice == '1':
            test_welcome_email()
        elif choice == '2':
            test_cleaning_alert()
        elif choice == '3':
            test_compliance_summary()
        elif choice == '4':
            test_cleaning_registered()
        elif choice == '0':
            print("\nSaindo...")
            break
        else:
            print("\n❌ Opção inválida!")

        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()
