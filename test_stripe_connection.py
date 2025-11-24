#!/usr/bin/env python
"""
Script de teste da conexão com Stripe
Verifica se as credenciais estão configuradas corretamente
"""

import os
import sys
from decouple import config

def check_stripe_config():
    """Verifica configuração do Stripe"""

    print("=" * 60)
    print("   🔍 TESTE DE CONFIGURAÇÃO DO STRIPE")
    print("=" * 60)
    print()

    # Verificar variáveis de ambiente
    checks = {
        'STRIPE_TEST_PUBLIC_KEY': None,
        'STRIPE_TEST_SECRET_KEY': None,
        'STRIPE_WEBHOOK_SECRET': None
    }

    all_ok = True

    for key in checks:
        try:
            value = config(key, default=None)
            if value and value != 'whsec_...':
                checks[key] = True
                masked = value[:15] + '...' + value[-4:] if len(value) > 20 else value
                print(f"✅ {key}: {masked}")
            else:
                checks[key] = False
                print(f"❌ {key}: NÃO CONFIGURADO")
                all_ok = False
        except Exception as e:
            checks[key] = False
            print(f"❌ {key}: ERRO - {e}")
            all_ok = False

    print()
    print("-" * 60)

    if all_ok:
        print("✅ TODAS AS CHAVES ESTÃO CONFIGURADAS!")
        print()
        print("Próximos passos:")
        print("  1. Inicie o servidor: docker-compose up")
        print("  2. Inicie o listener: stripe listen --forward-to localhost:8000/billing/webhook/stripe/")
        print("  3. Teste: stripe trigger checkout.session.completed")
    else:
        print("⚠️  ALGUMAS CHAVES ESTÃO FALTANDO!")
        print()

        if not checks['STRIPE_WEBHOOK_SECRET']:
            print("Para configurar o STRIPE_WEBHOOK_SECRET:")
            print("  1. Execute: stripe listen --forward-to localhost:8000/billing/webhook/stripe/")
            print("  2. Copie o 'whsec_...' que aparecer")
            print("  3. Cole no .env: STRIPE_WEBHOOK_SECRET=whsec_...")
            print()

        if not checks['STRIPE_TEST_PUBLIC_KEY'] or not checks['STRIPE_TEST_SECRET_KEY']:
            print("Para configurar as chaves do Stripe:")
            print("  1. Acesse: https://dashboard.stripe.com/test/apikeys")
            print("  2. Copie as chaves de teste")
            print("  3. Cole no .env:")
            print("     STRIPE_TEST_PUBLIC_KEY=pk_test_...")
            print("     STRIPE_TEST_SECRET_KEY=sk_test_...")
            print()

    print("=" * 60)
    print()

    return all_ok


def test_stripe_api():
    """Testa conexão com API do Stripe"""

    print()
    print("=" * 60)
    print("   🔗 TESTE DE CONEXÃO COM API DO STRIPE")
    print("=" * 60)
    print()

    try:
        import stripe

        secret_key = config('STRIPE_TEST_SECRET_KEY', default=None)

        if not secret_key:
            print("❌ STRIPE_TEST_SECRET_KEY não configurado")
            return False

        stripe.api_key = secret_key

        print("Testando conexão com Stripe API...")

        # Tentar listar os últimos 3 customers
        customers = stripe.Customer.list(limit=3)

        print(f"✅ Conexão bem-sucedida!")
        print(f"   Encontrados {len(customers.data)} customer(s) na sua conta")

        if customers.data:
            print()
            print("Últimos customers:")
            for customer in customers.data:
                print(f"  - {customer.id}: {customer.email or '(sem email)'}")

        print()
        print("=" * 60)
        return True

    except ImportError:
        print("⚠️  Pacote 'stripe' não instalado")
        print("   Execute: pip install stripe")
        return False

    except stripe.error.AuthenticationError:
        print("❌ Erro de autenticação!")
        print("   Verifique se STRIPE_TEST_SECRET_KEY está correto")
        return False

    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False


def check_django_settings():
    """Verifica se as configurações do Django estão corretas"""

    print()
    print("=" * 60)
    print("   ⚙️  VERIFICAÇÃO DAS CONFIGURAÇÕES DO DJANGO")
    print("=" * 60)
    print()

    try:
        # Adicionar o diretório do projeto ao path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cleantrack.settings')

        import django
        django.setup()

        from django.conf import settings

        # Verificar apps instalados
        if 'apps.billing' in settings.INSTALLED_APPS:
            print("✅ apps.billing está em INSTALLED_APPS")
        else:
            print("❌ apps.billing NÃO está em INSTALLED_APPS")
            return False

        if 'djstripe' in settings.INSTALLED_APPS:
            print("✅ djstripe está em INSTALLED_APPS")
        else:
            print("❌ djstripe NÃO está em INSTALLED_APPS")
            return False

        # Verificar se as chaves do Stripe estão carregadas
        if hasattr(settings, 'STRIPE_TEST_SECRET_KEY'):
            print("✅ STRIPE_TEST_SECRET_KEY carregado no Django")
        else:
            print("⚠️  STRIPE_TEST_SECRET_KEY não encontrado nas settings")

        if hasattr(settings, 'STRIPE_WEBHOOK_SECRET'):
            webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
            if webhook_secret and webhook_secret != 'whsec_...':
                print("✅ STRIPE_WEBHOOK_SECRET carregado no Django")
            else:
                print("⚠️  STRIPE_WEBHOOK_SECRET não configurado")
        else:
            print("⚠️  STRIPE_WEBHOOK_SECRET não encontrado nas settings")

        print()
        print("=" * 60)
        return True

    except ImportError as e:
        print(f"⚠️  Não foi possível importar Django: {e}")
        print("   (Isso é normal se você não estiver no ambiente virtual)")
        return False

    except Exception as e:
        print(f"⚠️  Erro ao verificar Django: {e}")
        return False


def main():
    """Função principal"""

    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         TESTE DE CONFIGURAÇÃO DO STRIPE - CLEANTRACK       ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()

    # Teste 1: Verificar variáveis de ambiente
    config_ok = check_stripe_config()

    # Teste 2: Testar API do Stripe
    if config_ok:
        api_ok = test_stripe_api()
    else:
        api_ok = False

    # Teste 3: Verificar Django settings
    django_ok = check_django_settings()

    # Resumo final
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                      RESUMO FINAL                          ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()

    if config_ok and api_ok and django_ok:
        print("🎉 TUDO CONFIGURADO CORRETAMENTE!")
        print()
        print("Você está pronto para usar webhooks do Stripe!")
        print()
        print("Execute agora:")
        print("  ./activate_stripe_webhook.sh")
        print()
        return 0
    else:
        print("⚠️  ALGUMAS CONFIGURAÇÕES PRECISAM DE AJUSTES")
        print()
        print("Revise os erros acima e corrija antes de prosseguir.")
        print()
        print("Consulte:")
        print("  - STRIPE_WEBHOOK_ACTIVATION.md")
        print("  - WEBHOOK_QUICK_START.md")
        print()
        return 1


if __name__ == '__main__':
    sys.exit(main())
