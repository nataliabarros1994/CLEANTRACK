# CleanTrack - Quick Start Guide

Guia rápido para começar a usar o CleanTrack com todas as funcionalidades implementadas.

## 📦 O que está implementado

### ✅ Sistema de Notificações (Resend)
- Email de boas-vindas
- Alertas de limpeza atrasada (automático)
- Notificações de registro de limpeza (opcional)
- Resumo semanal de conformidade

### ✅ Webhooks do Stripe (dj-stripe)
- Ativação automática após checkout
- Gerenciamento de ciclo de vida de subscription
- Desativação após falha de pagamento (3 tentativas)
- Integração com sistema de notificações

### ✅ Gerenciamento de Facilities
- Gerentes específicos por facility
- Notificações direcionadas
- Status de ativação via Stripe

---

## 🚀 Setup Rápido

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

Crie/edite `.env` na raiz do projeto:

```bash
# Django
SECRET_KEY=sua-secret-key-aqui
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@localhost/cleantrack

# Resend (Notificações)
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxx

# Stripe (Billing)
STRIPE_TEST_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxx
STRIPE_LIVE_SECRET_KEY=sk_live_xxxxxxxxxxxxxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Aplicar migrations

```bash
python manage.py migrate
```

Isso criará:
- Campo `managed_facilities` no User
- Campos `is_active` e `stripe_customer_id` no Facility

### 4. Criar superusuário

```bash
python manage.py createsuperuser
```

### 5. Iniciar servidor

```bash
python manage.py runserver
```

---

## 🧪 Testar Funcionalidades

### Testar Notificações por Email

```bash
python apps/notifications/test_email.py
```

Ou via Django shell:

```python
python manage.py shell

from apps.notifications.services import send_welcome_email
send_welcome_email('seu-email@exemplo.com', 'Seu Nome')
```

### Testar Webhooks do Stripe

**Opção 1: Script de teste (sem Stripe)**

```bash
python apps/billing/test_webhooks.py
```

**Opção 2: Com Stripe CLI (recomendado)**

Terminal 1:
```bash
stripe listen --forward-to localhost:8000/billing/webhook/stripe/
```

Terminal 2:
```bash
stripe trigger checkout.session.completed
stripe trigger invoice.payment_failed
```

---

## 📊 Estrutura de URLs

```
Admin:
  /admin/                          → Django Admin

Billing:
  /billing/webhook/stripe/         → Stripe Webhooks (POST)

Notificações:
  (Serviços Python - não têm URLs)
```

---

## 👥 Configurar Gerentes e Facilities

### Via Django Admin

1. Acesse `/admin/`
2. Vá em **Accounts > Users**
3. Edite um usuário
4. Defina **role** como `manager` ou `admin`
5. Em **Managed facilities**, selecione as facilities
6. Salve

### Via Django Shell

```python
python manage.py shell

from apps.accounts.models import User
from apps.facilities.models import Facility

# Criar gerente
manager = User.objects.create_user(
    username='joao',
    email='joao@cleantrack.com',
    password='senha123',
    first_name='João',
    last_name='Silva',
    role='manager'
)

# Criar facility
facility = Facility.objects.create(
    name='Unidade Central',
    address='Rua Exemplo, 123'
)

# Atribuir gerente à facility
manager.managed_facilities.add(facility)

print(f"✅ {manager.get_full_name()} agora gerencia {facility.name}")
```

---

## 💳 Criar Checkout Session (Stripe)

```python
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def create_subscription_checkout(facility_id):
    """Cria checkout para uma facility"""

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_xxxxxxxxxxxxxx',  # Seu Price ID do Stripe
            'quantity': 1,
        }],
        mode='subscription',
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',

        # IMPORTANTE: Metadata para webhook
        client_reference_id=str(facility_id),
        metadata={
            'facility_id': str(facility_id),
        },
    )

    return session.url  # Redirecionar usuário para esta URL
```

---

## 🔍 Verificar Status

### Ver facilities ativas

```python
python manage.py shell

from apps.facilities.models import Facility

# Todas as facilities
for f in Facility.objects.all():
    print(f"{f.name}: {'✅ Ativa' if f.is_active else '❌ Inativa'}")

# Apenas ativas
active = Facility.objects.filter(is_active=True)
print(f"\n{active.count()} facilities ativas")
```

### Ver gerentes por facility

```python
from apps.facilities.models import Facility

facility = Facility.objects.get(name='Unidade Central')
managers = facility.managers.all()

print(f"Gerentes da {facility.name}:")
for manager in managers:
    print(f"  - {manager.get_full_name()} ({manager.email})")
```

### Ver logs de notificações

```bash
tail -f logs/cleantrack.log | grep "apps.notifications"
```

### Ver logs de billing

```bash
tail -f logs/cleantrack.log | grep "apps.billing"
```

---

## 📝 Cenários Comuns

### Cenário 1: Novo Cliente se Inscreve

1. Cliente clica em "Assinar"
2. Sistema cria checkout session com `facility_id` no metadata
3. Cliente paga no Stripe
4. Stripe envia webhook `checkout.session.completed`
5. Sistema ativa facility automaticamente
6. Email de boas-vindas é enviado para gerentes
7. ✅ Facility está ativa e pronta para uso

### Cenário 2: Pagamento Falha 3 Vezes

1. Stripe tenta cobrar cartão (falha)
2. Stripe retenta automaticamente (falha novamente)
3. Stripe faz última tentativa (falha pela 3ª vez)
4. Stripe envia webhook `invoice.payment_failed` com `attempt_count=3`
5. Sistema desativa facility automaticamente
6. ⚠️ Facility fica inativa até pagamento ser resolvido

### Cenário 3: Cliente Cancela Assinatura

1. Cliente cancela subscription no Stripe
2. Stripe envia webhook `customer.subscription.deleted`
3. Sistema desativa facility automaticamente
4. ❌ Facility fica inativa

### Cenário 4: Limpeza Atrasada

1. Equipamento não é limpo no prazo
2. Técnico registra limpeza atrasada
3. Sistema detecta `is_compliant=False` automaticamente
4. Email de alerta é enviado para todos managers/admins
5. 📧 Gerentes são notificados sobre o atraso

---

## 🔗 Links Úteis

### Documentação Detalhada:
- `SETUP_NOTIFICATIONS.md` - Setup completo de notificações
- `STRIPE_WEBHOOKS_SETUP.md` - Setup completo de webhooks Stripe
- `apps/notifications/README.md` - API de notificações

### Scripts de Teste:
- `apps/notifications/test_email.py` - Testar emails
- `apps/billing/test_webhooks.py` - Testar webhooks

### Stripe:
- [Dashboard](https://dashboard.stripe.com)
- [Webhooks](https://dashboard.stripe.com/webhooks)
- [Documentação](https://stripe.com/docs)

### Resend:
- [Dashboard](https://resend.com/overview)
- [API Keys](https://resend.com/api-keys)
- [Documentação](https://resend.com/docs)

---

## 🆘 Troubleshooting Rápido

### Problema: Email não está sendo enviado

```python
# Verificar configuração
python manage.py shell

from django.conf import settings
print(settings.RESEND_API_KEY)  # Deve começar com 're_'

# Testar manualmente
from apps.notifications.services import send_welcome_email
send_welcome_email('seu-email@teste.com', 'Teste')
```

### Problema: Webhook não está funcionando

```bash
# 1. Verificar se webhook secret está configurado
echo $STRIPE_WEBHOOK_SECRET

# 2. Testar com Stripe CLI
stripe listen --forward-to localhost:8000/billing/webhook/stripe/

# 3. Ver logs
tail -f logs/cleantrack.log | grep billing
```

### Problema: Facility não ativou após pagamento

```python
# Verificar metadata no Stripe Dashboard
# Deve ter: client_reference_id ou metadata.facility_id

# Verificar logs
tail -f logs/cleantrack.log | grep "checkout.session.completed"

# Verificar manualmente
from apps.facilities.models import Facility
facility = Facility.objects.get(id=1)
print(f"Active: {facility.is_active}")
print(f"Customer ID: {facility.stripe_customer_id}")
```

---

## ✅ Checklist de Produção

Antes de ir para produção:

- [ ] Aplicar todas as migrations
- [ ] Configurar `.env` com chaves de produção
- [ ] Configurar webhook endpoint no Stripe (produção)
- [ ] Testar fluxo completo de checkout
- [ ] Testar fluxo de falha de pagamento
- [ ] Configurar logging em arquivo
- [ ] Configurar domínio verificado no Resend
- [ ] Testar emails de notificação
- [ ] Configurar monitoramento de erros (Sentry)
- [ ] Backup do banco de dados
- [ ] Documentar processo de rollback

---

**Pronto para começar!** 🚀

Para dúvidas, consulte a documentação detalhada em cada módulo.
