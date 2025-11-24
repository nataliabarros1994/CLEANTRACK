# ⚡ Webhook Stripe - Quick Start (3 Comandos)

## 🎯 Objetivo

Configurar o webhook do Stripe para receber eventos de pagamento em tempo real.

---

## 🚀 Opção A: Script Automatizado (Recomendado)

Execute o script que faz tudo automaticamente:

```bash
./activate_stripe_webhook.sh
```

O script vai:
1. Verificar se você está logado no Stripe CLI
2. Obter o webhook secret automaticamente
3. Atualizar o arquivo `.env`
4. Te guiar nos próximos passos

---

## 🔧 Opção B: Manual (3 Passos)

### **Terminal 1** - Servidor Django

```bash
# Com Docker
docker-compose up

# OU sem Docker
python manage.py runserver
```

### **Terminal 2** - Stripe Listener

```bash
# Login no Stripe (primeira vez)
stripe login

# Iniciar listener
stripe listen --forward-to localhost:8000/billing/webhook/stripe/
```

**📋 Você verá algo assim:**
```
> Ready! You are using Stripe API Version [2024-XX-XX]
> Your webhook signing secret is whsec_abc123def456ghi789jkl012mno345pqr678stu901
```

**📝 COPIE o `whsec_...`**

### **Atualizar .env**

Abra o arquivo `.env` e adicione/atualize:

```bash
STRIPE_WEBHOOK_SECRET=whsec_abc123def456ghi789jkl012mno345pqr678stu901
```

### **Reiniciar Servidor**

No **Terminal 1**:

```bash
# Com Docker
Ctrl+C
docker-compose restart web

# OU sem Docker
Ctrl+C
python manage.py runserver
```

### **Terminal 3** - Testar Webhooks

```bash
# Teste 1: Checkout completo
stripe trigger checkout.session.completed

# Teste 2: Pagamento bem-sucedido
stripe trigger invoice.payment_succeeded

# Teste 3: Subscription cancelada
stripe trigger customer.subscription.deleted
```

---

## ✅ Como Saber que Funcionou?

### 1. No Terminal 2 (Stripe Listener)

Você verá:
```
[200] POST /billing/webhook/stripe/ [evt_xxxx]
```

### 2. Nos Logs do Django

```bash
tail -f logs/cleantrack.log | grep billing
```

Você verá:
```
INFO apps.billing.webhook_handlers: Handling checkout.session.completed for session cs_test_xxxxx
INFO apps.billing.webhook_handlers: Facility activated after successful checkout
INFO apps.notifications.services: Welcome email sent to user@example.com
```

### 3. No Admin Django

Acesse: http://localhost:8000/admin/facilities/facility/

- A facility criada deve estar com `is_active = True`
- O campo `stripe_customer_id` deve estar preenchido

---

## 🎯 Eventos Configurados (8 total)

| Evento | O que acontece |
|--------|----------------|
| `checkout.session.completed` | ✅ Ativa facility + envia email |
| `customer.subscription.created` | ✅ Ativa facility |
| `customer.subscription.updated` | ✅ Atualiza status |
| `customer.subscription.deleted` | ⚠️ Desativa facility |
| `invoice.payment_succeeded` | ✅ Garante facility ativa |
| `invoice.payment_failed` | ⚠️ Desativa após 3 falhas |
| `customer.subscription.trial_will_end` | 📝 Log de aviso |
| `charge.refunded` | 📝 Log de reembolso |

---

## 🛠️ Troubleshooting

### ❌ "Webhook signing secret not found"

**Solução:** Verifique se o `.env` foi atualizado e o servidor reiniciado.

```bash
# Verificar se está carregado
docker-compose exec web python manage.py shell
>>> from django.conf import settings
>>> print(settings.STRIPE_WEBHOOK_SECRET)
whsec_abc123...
```

### ❌ "Connection refused" no listener

**Solução:** Certifique-se de que o servidor Django está rodando antes de iniciar o listener.

### ❌ Eventos não aparecem nos logs

**Solução:** Verifique se `apps.billing` está registrado.

```bash
docker-compose exec web python manage.py shell
>>> from django.conf import settings
>>> 'apps.billing' in settings.INSTALLED_APPS
True
```

---

## 📊 Status dos Handlers

Verifique se os 8 handlers foram registrados:

```bash
grep "Registering Stripe webhook handler" logs/cleantrack.log | wc -l
```

Deve retornar: **8**

---

## 🎉 Pronto!

Agora você está recebendo eventos do Stripe em tempo real!

**Deixe o Terminal 2 (listener) rodando enquanto desenvolve.**

Para documentação completa, veja: `STRIPE_WEBHOOK_ACTIVATION.md`
