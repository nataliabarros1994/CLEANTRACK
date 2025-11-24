# Configuração de Webhooks do Stripe - CleanTrack

Este guia mostra como configurar webhooks do Stripe para ativar/desativar contas automaticamente com base em pagamentos e assinaturas.

## 📋 O que foi implementado

### Novos campos no modelo Facility:
- `is_active`: Indica se a facility tem assinatura ativa
- `stripe_customer_id`: ID do cliente no Stripe

### Webhook handlers usando dj-stripe:
1. **checkout.session.completed** - Ativa facility/account após checkout
2. **customer.subscription.created** - Ativa na criação de assinatura
3. **customer.subscription.updated** - Atualiza status baseado na assinatura
4. **customer.subscription.deleted** - Desativa ao cancelar
5. **invoice.payment_succeeded** - Confirma pagamento bem-sucedido
6. **invoice.payment_failed** - Desativa após 3 falhas
7. **customer.subscription.trial_will_end** - Notifica fim de trial
8. **charge.refunded** - Registra reembolsos

---

## 🚀 Setup Inicial

### 1. Aplicar Migrations

```bash
python manage.py migrate facilities
python manage.py migrate accounts  # Se ainda não aplicou
```

### 2. Importar Webhook Handlers

Adicione ao final de `apps/billing/__init__.py`:

```python
# Importa os webhook handlers para registrá-los
from . import webhook_handlers
```

Ou crie `apps/billing/apps.py`:

```python
from django.apps import AppConfig


class BillingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.billing'

    def ready(self):
        # Importa os webhook handlers
        from . import webhook_handlers
```

E atualize `apps/billing/__init__.py`:

```python
default_app_config = 'apps.billing.apps.BillingConfig'
```

### 3. Verificar URLs

Certifique-se de que as URLs do billing estão incluídas em `cleantrack/urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # ... outras URLs ...
    path('billing/', include('apps.billing.urls')),
]
```

---

## 🔧 Configuração no Stripe Dashboard

### 1. Criar Webhook Endpoint

1. Acesse [Stripe Dashboard](https://dashboard.stripe.com)
2. Vá em **Developers > Webhooks**
3. Clique em **Add endpoint**

### 2. Configurar URL do Endpoint

**Para desenvolvimento local com Stripe CLI:**
```bash
stripe listen --forward-to localhost:8000/billing/webhook/stripe/
```

**Para produção:**
```
https://seu-dominio.com/billing/webhook/stripe/
```

### 3. Selecionar Eventos

Marque os seguintes eventos:

#### Checkout:
- ✅ `checkout.session.completed`

#### Assinaturas:
- ✅ `customer.subscription.created`
- ✅ `customer.subscription.updated`
- ✅ `customer.subscription.deleted`
- ✅ `customer.subscription.trial_will_end`

#### Pagamentos:
- ✅ `invoice.payment_succeeded`
- ✅ `invoice.payment_failed`

#### Reembolsos:
- ✅ `charge.refunded`

### 4. Obter Webhook Secret

Após criar o endpoint, copie o **Signing secret** (começa com `whsec_`)

### 5. Adicionar ao `.env`

```bash
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 💻 Criar Checkout Session com Metadata

Quando criar uma sessão de checkout, inclua metadata para identificar a facility/account:

### Exemplo 1: Usando Stripe Checkout (Python)

```python
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def create_checkout_session(facility_id, user_email):
    """
    Cria uma sessão de checkout do Stripe para uma facility
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_xxxxxxxxxxxx',  # ID do preço no Stripe
                'quantity': 1,
            }],
            mode='subscription',  # ou 'payment' para pagamento único
            success_url='https://seu-dominio.com/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://seu-dominio.com/cancel',

            # IMPORTANTE: Passar metadata para identificar a facility
            client_reference_id=str(facility_id),  # Usado como facility_id
            metadata={
                'facility_id': str(facility_id),
                'facility_name': 'Nome da Facility'  # Opcional
            },
            customer_email=user_email,
        )

        return session.url

    except Exception as e:
        print(f"Erro ao criar checkout session: {e}")
        return None
```

### Exemplo 2: View Django para Checkout

```python
# apps/billing/views.py

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from apps.facilities.models import Facility

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@login_required
def create_facility_subscription(request, facility_id):
    """
    Cria uma subscrição para uma facility
    """
    try:
        facility = Facility.objects.get(id=facility_id)

        # Criar sessão de checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_xxxxxxxxxxxx',  # Seu Price ID
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.build_absolute_uri('/billing/success/'),
            cancel_url=request.build_absolute_uri('/billing/cancel/'),
            client_reference_id=str(facility.id),
            metadata={
                'facility_id': str(facility.id),
            },
            customer_email=request.user.email,
        )

        return redirect(session.url)

    except Facility.DoesNotExist:
        return redirect('error')
    except Exception as e:
        print(f"Erro: {e}")
        return redirect('error')
```

### Exemplo 3: Criar Subscription Diretamente

```python
def create_subscription_directly(customer_id, facility_id, price_id):
    """
    Cria uma subscription diretamente (sem checkout)
    """
    subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[{'price': price_id}],
        metadata={
            'facility_id': str(facility_id),
        }
    )

    return subscription
```

---

## 🧪 Testar Webhooks Localmente

### 1. Instalar Stripe CLI

```bash
# macOS
brew install stripe/stripe-cli/stripe

# Linux
wget https://github.com/stripe/stripe-cli/releases/download/v1.19.0/stripe_1.19.0_linux_x86_64.tar.gz
tar -xvf stripe_1.19.0_linux_x86_64.tar.gz
sudo mv stripe /usr/local/bin/
```

### 2. Login no Stripe CLI

```bash
stripe login
```

### 3. Encaminhar Webhooks para Localhost

```bash
stripe listen --forward-to localhost:8000/billing/webhook/stripe/
```

Isso exibirá um **webhook signing secret** temporário. Use-o no `.env`:
```
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
```

### 4. Testar Eventos

Em outro terminal, dispare eventos de teste:

```bash
# Testar checkout completado
stripe trigger checkout.session.completed

# Testar subscription criada
stripe trigger customer.subscription.created

# Testar pagamento falhado
stripe trigger invoice.payment_failed

# Testar subscription deletada
stripe trigger customer.subscription.deleted
```

### 5. Ver Logs

O terminal com `stripe listen` mostrará todos os webhooks recebidos.

---

## 📊 Fluxo de Ativação/Desativação

### Cenário 1: Novo Cliente Completa Checkout

```
Cliente completa checkout no Stripe
        ↓
Stripe envia webhook: checkout.session.completed
        ↓
handle_checkout_session_completed() é chamado
        ↓
Facility/Account é ativado (is_active=True)
        ↓
stripe_customer_id é salvo
        ↓
Email de boas-vindas é enviado aos gerentes
```

### Cenário 2: Subscription é Criada

```
Subscription é criada no Stripe
        ↓
Stripe envia webhook: customer.subscription.created
        ↓
handle_subscription_created() é chamado
        ↓
Facility/Account é ativado
```

### Cenário 3: Pagamento Falha

```
Pagamento falha (1ª tentativa)
        ↓
Stripe tenta novamente automaticamente
        ↓
Pagamento falha (2ª tentativa)
        ↓
Stripe tenta novamente
        ↓
Pagamento falha (3ª tentativa)
        ↓
Stripe envia webhook: invoice.payment_failed (attempt_count=3)
        ↓
handle_payment_failed() é chamado
        ↓
Facility/Account é DESATIVADO
        ↓
Log de erro é registrado
        ↓
TODO: Email de notificação é enviado
```

### Cenário 4: Subscription é Cancelada

```
Cliente cancela subscription no Stripe
        ↓
Stripe envia webhook: customer.subscription.deleted
        ↓
handle_subscription_deleted() é chamado
        ↓
Facility/Account é DESATIVADO
        ↓
Log de aviso é registrado
```

---

## 🔍 Debugging e Logs

### Ver Logs de Webhook

```bash
# Ver todos os logs
tail -f logs/cleantrack.log

# Ver apenas logs de billing
grep "apps.billing" logs/cleantrack.log

# Ver erros
grep ERROR logs/cleantrack.log
```

### Configurar Logging

Em `cleantrack/settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/cleantrack.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'apps.billing': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### Ver Webhooks no Stripe Dashboard

1. Acesse [Dashboard > Developers > Webhooks](https://dashboard.stripe.com/webhooks)
2. Clique no seu endpoint
3. Ver **Recent deliveries** para ver status de cada webhook

---

## ⚠️ Troubleshooting

### Problema: Webhook não está sendo recebido

**Solução:**
1. Verifique se a URL está acessível publicamente (use ngrok para local)
2. Verifique se `STRIPE_WEBHOOK_SECRET` está correto no `.env`
3. Veja logs do Stripe Dashboard > Webhooks

### Problema: Signature verification failed

**Solução:**
1. Certifique-se de que `DJSTRIPE_WEBHOOK_SECRET` no settings está correto
2. Não modifique o payload do webhook antes de verificar
3. Use o webhook secret correto (produção vs teste)

### Problema: Facility não está sendo ativada

**Solução:**
1. Verifique se você está passando `client_reference_id` ou `metadata.facility_id`
2. Veja os logs: `tail -f logs/cleantrack.log`
3. Verifique se o webhook handler está sendo chamado
4. Confirme que a facility existe no banco de dados

### Problema: Email de boas-vindas não é enviado

**Solução:**
1. Verifique se o gerente tem `managed_facilities` atribuídas
2. Verifique se o email do gerente está preenchido
3. Veja logs de notificações: `grep "apps.notifications" logs/cleantrack.log`
4. Teste o serviço de email separadamente

---

## 🔐 Segurança

### Verificação de Assinatura

O dj-stripe verifica automaticamente a assinatura do webhook usando o `DJSTRIPE_WEBHOOK_SECRET`.

**NUNCA:**
- Compartilhe o webhook secret publicamente
- Commit o webhook secret no git
- Use o mesmo secret para teste e produção

### CSRF Exemption

O endpoint de webhook usa `@csrf_exempt` porque o Stripe não pode enviar tokens CSRF. Isso é seguro porque a assinatura do webhook garante autenticidade.

---

## 📚 Referências

- [Stripe Webhooks Guide](https://stripe.com/docs/webhooks)
- [dj-stripe Documentation](https://dj-stripe.readthedocs.io/)
- [Stripe CLI](https://stripe.com/docs/stripe-cli)
- [Testing Webhooks](https://stripe.com/docs/webhooks/test)

---

## ✅ Checklist de Produção

Antes de ir para produção:

- [ ] Aplicar migrations: `python manage.py migrate`
- [ ] Configurar webhook endpoint no Stripe Dashboard
- [ ] Adicionar `STRIPE_WEBHOOK_SECRET` ao `.env` de produção
- [ ] Configurar logging adequado
- [ ] Testar todos os eventos críticos
- [ ] Implementar notificações por email para eventos importantes
- [ ] Configurar monitoramento de webhooks falhados
- [ ] Documentar processo de rollback se necessário
- [ ] Adicionar alertas para desativações de conta

---

**Dúvidas?** Consulte os logs em `apps/billing/webhook_handlers.py` para ver todos os handlers disponíveis.
