# 🧪 Guia Completo de Testes - Webhooks do Stripe

## 🎯 Objetivo

Testar todos os 8 eventos de webhook implementados e verificar se estão funcionando corretamente.

---

## ⚡ Quick Start - Teste Rápido

Execute este comando para testar a ativação automática de facility:

```bash
stripe trigger checkout.session.completed
```

**O que vai acontecer:**
1. ✅ Stripe enviará evento `checkout.session.completed`
2. ✅ Handler criará/ativará uma facility
3. ✅ Email de boas-vindas será enviado (via Resend)
4. ✅ Logs mostrarão o processamento

---

## 🚀 Setup - Preparação para Testes

### Passo 1: Certifique-se de que os containers estão rodando

```bash
docker-compose ps
```

**Resultado esperado:**
```
Name                   State   Ports
cleantrack_web_1       Up      0.0.0.0:8000->8000/tcp
cleantrack_db_1        Up      0.0.0.0:5432->5432/tcp
```

Se não estiverem rodando:
```bash
docker-compose up -d
```

### Passo 2: Inicie o Stripe Listener

**Terminal dedicado (mantenha aberto):**
```bash
stripe listen --forward-to localhost:8000/billing/webhook/stripe/
```

**Você verá:**
```
> Ready! Your webhook signing secret is whsec_abc123...
```

### Passo 3: Configure o Webhook Secret (primeira vez)

Se ainda não configurou:

```bash
# 1. Copie o whsec_... do terminal acima

# 2. Edite o .env
nano .env

# 3. Atualize a linha:
STRIPE_WEBHOOK_SECRET=whsec_COLE_AQUI_O_SECRET

# 4. Reinicie o container
docker-compose restart web
```

### Passo 4: Abra um terminal para logs (opcional, mas recomendado)

```bash
# Terminal adicional
docker-compose logs -f web | grep billing
```

---

## 🧪 Testes dos 8 Eventos

### Teste 1: Checkout Session Completed ⭐ **MAIS IMPORTANTE**

**Comando:**
```bash
stripe trigger checkout.session.completed
```

**O que acontece:**
1. Cria/obtém um customer no Stripe
2. Cria uma facility no banco de dados
3. Ativa a facility (`is_active = True`)
4. Associa `stripe_customer_id` à facility
5. Envia email de boas-vindas

**Verificar:**

✅ **No terminal do listener:**
```
[200] POST /billing/webhook/stripe/ [evt_xxxx]
```

✅ **Nos logs do Django:**
```
INFO apps.billing.webhook_handlers: Handling checkout.session.completed for session cs_test_xxxxx
INFO apps.billing.webhook_handlers: Facility activated after successful checkout
INFO apps.notifications.services: Welcome email sent to user@example.com
```

✅ **No Admin Django:**
```bash
# Abra: http://localhost:8000/admin/facilities/facility/
```

Deve ter uma facility com:
- `is_active = True` ✅
- `stripe_customer_id` preenchido (ex: `cus_xxxxx`)

---

### Teste 2: Customer Subscription Created

**Comando:**
```bash
stripe trigger customer.subscription.created
```

**O que acontece:**
1. Obtém ou cria facility pelo customer_id
2. Ativa a facility

**Verificar:**

✅ **Logs:**
```
INFO apps.billing.webhook_handlers: Handling customer.subscription.created for subscription sub_xxxxx
INFO apps.billing.webhook_handlers: Facility activated after subscription creation
```

---

### Teste 3: Customer Subscription Updated

**Comando:**
```bash
stripe trigger customer.subscription.updated
```

**O que acontece:**
1. Atualiza status da facility baseado no status da subscription
2. Ativa se status = `active`
3. Desativa se status = `canceled`, `incomplete_expired`, ou `unpaid`

**Verificar:**

✅ **Logs:**
```
INFO apps.billing.webhook_handlers: Handling customer.subscription.updated for subscription sub_xxxxx
INFO apps.billing.webhook_handlers: Facility status updated based on subscription status: active
```

---

### Teste 4: Customer Subscription Deleted

**Comando:**
```bash
stripe trigger customer.subscription.deleted
```

**O que acontece:**
1. Encontra facility pelo customer_id
2. Desativa a facility (`is_active = False`)
3. TODO: Email de cancelamento (implementar)

**Verificar:**

✅ **Logs:**
```
INFO apps.billing.webhook_handlers: Handling customer.subscription.deleted for subscription sub_xxxxx
INFO apps.billing.webhook_handlers: Facility deactivated after subscription cancellation
```

✅ **No Admin:**
A facility deve estar com `is_active = False`

---

### Teste 5: Invoice Payment Succeeded

**Comando:**
```bash
stripe trigger invoice.payment_succeeded
```

**O que acontece:**
1. Encontra facility pelo customer_id
2. Garante que está ativa
3. Reseta contador de falhas de pagamento

**Verificar:**

✅ **Logs:**
```
INFO apps.billing.webhook_handlers: Handling invoice.payment_succeeded for invoice in_xxxxx
INFO apps.billing.webhook_handlers: Payment succeeded for customer cus_xxxxx
```

---

### Teste 6: Invoice Payment Failed

**Comando:**
```bash
stripe trigger invoice.payment_failed
```

**O que acontece:**
1. Incrementa contador de falhas
2. Se atingir 3 falhas, desativa a facility
3. TODO: Email de falha (implementar)

**Verificar:**

✅ **Logs (primeira falha):**
```
INFO apps.billing.webhook_handlers: Handling invoice.payment_failed for invoice in_xxxxx
INFO apps.billing.webhook_handlers: Payment failed for customer cus_xxxxx (attempt 1/3)
```

✅ **Logs (terceira falha):**
```
INFO apps.billing.webhook_handlers: Payment failed for customer cus_xxxxx (attempt 3/3)
INFO apps.billing.webhook_handlers: Facility deactivated after 3 failed payment attempts
```

**Testar 3 falhas consecutivas:**
```bash
# Execute 3 vezes
stripe trigger invoice.payment_failed
stripe trigger invoice.payment_failed
stripe trigger invoice.payment_failed
```

Após a 3ª, a facility deve ser desativada.

---

### Teste 7: Customer Subscription Trial Will End

**Comando:**
```bash
stripe trigger customer.subscription.trial_will_end
```

**O que acontece:**
1. Registra log de aviso
2. TODO: Email de alerta (implementar)

**Verificar:**

✅ **Logs:**
```
INFO apps.billing.webhook_handlers: Handling customer.subscription.trial_will_end for subscription sub_xxxxx
INFO apps.billing.webhook_handlers: Trial will end in 3 days for customer cus_xxxxx
```

---

### Teste 8: Charge Refunded

**Comando:**
```bash
stripe trigger charge.refunded
```

**O que acontece:**
1. Registra log de reembolso
2. TODO: Email de confirmação (implementar)

**Verificar:**

✅ **Logs:**
```
INFO apps.billing.webhook_handlers: Handling charge.refunded for charge ch_xxxxx
INFO apps.billing.webhook_handlers: Charge refunded: $XX.XX for customer cus_xxxxx
```

---

## 🔥 Teste Completo - Todos os Eventos de Uma Vez

Execute este script para testar todos os 8 eventos sequencialmente:

```bash
#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║        TESTE COMPLETO - 8 EVENTOS DE WEBHOOK                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

eventos=(
  "checkout.session.completed"
  "customer.subscription.created"
  "customer.subscription.updated"
  "customer.subscription.deleted"
  "invoice.payment_succeeded"
  "invoice.payment_failed"
  "customer.subscription.trial_will_end"
  "charge.refunded"
)

for i in "${!eventos[@]}"; do
  numero=$((i + 1))
  evento="${eventos[$i]}"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Teste $numero/8: $evento"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  stripe trigger "$evento"
  echo ""
  sleep 2
done

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                  ✅ TODOS OS TESTES COMPLETOS!              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Verifique:"
echo "  1. Terminal do listener (deve ter 8x [200])"
echo "  2. Logs do Django (eventos processados)"
echo "  3. Admin: http://localhost:8000/admin/facilities/facility/"
echo ""
```

**Como usar:**

```bash
# Salvar em arquivo
nano test_all_webhooks.sh

# Colar o script acima

# Dar permissão
chmod +x test_all_webhooks.sh

# Executar
./test_all_webhooks.sh
```

---

## 📊 Checklist de Verificação

Após executar os testes, verifique:

### Terminal do Stripe Listener

```
[200] POST /billing/webhook/stripe/ [evt_1xxx] checkout.session.completed
[200] POST /billing/webhook/stripe/ [evt_2xxx] customer.subscription.created
[200] POST /billing/webhook/stripe/ [evt_3xxx] customer.subscription.updated
[200] POST /billing/webhook/stripe/ [evt_4xxx] customer.subscription.deleted
[200] POST /billing/webhook/stripe/ [evt_5xxx] invoice.payment_succeeded
[200] POST /billing/webhook/stripe/ [evt_6xxx] invoice.payment_failed
[200] POST /billing/webhook/stripe/ [evt_7xxx] customer.subscription.trial_will_end
[200] POST /billing/webhook/stripe/ [evt_8xxx] charge.refunded
```

**✅ Todos devem mostrar `[200]`**

---

### Logs do Django

```bash
grep "Handling" logs/cleantrack.log | tail -10
```

Deve mostrar algo como:
```
INFO apps.billing.webhook_handlers: Handling checkout.session.completed
INFO apps.billing.webhook_handlers: Handling customer.subscription.created
INFO apps.billing.webhook_handlers: Handling customer.subscription.updated
...
```

**✅ Deve ter 8 linhas "Handling ..."**

---

### Admin Django

Acesse: http://localhost:8000/admin/facilities/facility/

**Verificar:**

✅ **Facilities criadas:**
- Pelo menos 1 facility deve existir
- Deve ter `stripe_customer_id` preenchido
- Status `is_active` pode variar dependendo dos testes

✅ **No Django shell:**
```bash
docker-compose exec web python manage.py shell
```

```python
from apps.facilities.models import Facility

# Contar facilities
print(f"Total de facilities: {Facility.objects.count()}")

# Ver todas
for f in Facility.objects.all():
    print(f"{f.id}: {f.name} - Active: {f.is_active} - Customer: {f.stripe_customer_id}")

# Ver facilities ativas
print(f"Facilities ativas: {Facility.objects.filter(is_active=True).count()}")

# Ver facilities com Stripe customer
print(f"Com Stripe customer: {Facility.objects.exclude(stripe_customer_id='').count()}")
```

---

### Verificar Handlers Registrados

```bash
grep "Registering Stripe webhook handler" logs/cleantrack.log | wc -l
```

**Resultado esperado:** `8`

Se retornar menos, verifique:
```bash
docker-compose logs web | grep "Registering Stripe webhook handler"
```

Deve aparecer:
```
INFO apps.billing.apps: Registering Stripe webhook handler for: checkout.session.completed
INFO apps.billing.apps: Registering Stripe webhook handler for: customer.subscription.created
...
```

---

## 🆘 Troubleshooting

### Problema: [400] Bad Request

**Causa:** Webhook secret incorreto ou não configurado

**Solução:**
```bash
# 1. Verifique o .env
grep STRIPE_WEBHOOK_SECRET .env

# 2. Deve ter um whsec_... válido
# Se não, copie do terminal do stripe listen e atualize

# 3. Reinicie
docker-compose restart web
```

---

### Problema: [404] Not Found

**Causa:** Rota não existe ou não está registrada

**Solução:**
```bash
# Verificar URLs configuradas
docker-compose exec web python manage.py show_urls | grep billing

# Ou testar manualmente
curl -X POST http://localhost:8000/billing/webhook/stripe/
```

Deve retornar erro de assinatura, mas não 404.

---

### Problema: [500] Internal Server Error

**Causa:** Erro no código do handler

**Solução:**
```bash
# Ver erro completo nos logs
docker-compose logs web | tail -50
```

Procure por stack trace e corrija o erro.

---

### Problema: Evento recebido mas nada acontece

**Causa:** Handler não registrado ou erro silencioso

**Solução:**
```bash
# 1. Verificar se handlers foram registrados
docker-compose logs web | grep "Registering Stripe webhook handler"

# 2. Ver logs de erro
docker-compose logs web | grep ERROR

# 3. Verificar se o evento está sendo recebido
docker-compose logs web | grep "Stripe webhook received"
```

---

### Problema: Email não é enviado

**Causa:** Resend API key incorreta ou limite atingido

**Solução:**
```bash
# 1. Verificar key
grep RESEND_API_KEY .env

# 2. Testar diretamente
docker-compose exec web python manage.py shell

from apps.notifications.services import send_welcome_email
send_welcome_email('seu@email.com', 'Test User')

# 3. Ver logs de email
docker-compose logs web | grep notifications
```

---

## 📝 Cenários de Teste Reais

### Cenário 1: Novo Cliente Assina Plano

```bash
# 1. Cliente completa checkout
stripe trigger checkout.session.completed

# 2. Subscription é criada
stripe trigger customer.subscription.created

# Verificar: Facility ativa com stripe_customer_id
```

---

### Cenário 2: Pagamento Mensal Bem-Sucedido

```bash
# 1. Invoice é paga
stripe trigger invoice.payment_succeeded

# Verificar: Facility continua ativa
```

---

### Cenário 3: Falha de Pagamento e Recuperação

```bash
# 1. Primeira falha
stripe trigger invoice.payment_failed

# 2. Segunda falha
stripe trigger invoice.payment_failed

# 3. Pagamento bem-sucedido (recuperação)
stripe trigger invoice.payment_succeeded

# Verificar: Facility continua ativa, contador resetado
```

---

### Cenário 4: Cliente Cancela Assinatura

```bash
# 1. Subscription é deletada
stripe trigger customer.subscription.deleted

# Verificar: Facility desativada (is_active = False)
```

---

### Cenário 5: Trial Expirando

```bash
# 1. Aviso de trial expirando
stripe trigger customer.subscription.trial_will_end

# 2. Cliente não converte, subscription deleta
stripe trigger customer.subscription.deleted

# Verificar: Logs registrados, facility desativada
```

---

## 🎯 Comandos Úteis para Testes

### Limpar todas as facilities (resetar testes)

```bash
docker-compose exec web python manage.py shell
```

```python
from apps.facilities.models import Facility
Facility.objects.all().delete()
print("Todas as facilities foram removidas")
```

---

### Ver últimos eventos recebidos

```bash
docker-compose logs web | grep "Handling" | tail -20
```

---

### Ver status de todas as facilities

```bash
docker-compose exec web python manage.py shell
```

```python
from apps.facilities.models import Facility

for f in Facility.objects.all():
    status = "✅ ATIVA" if f.is_active else "❌ INATIVA"
    print(f"{status} | {f.name} | Customer: {f.stripe_customer_id or 'N/A'}")
```

---

### Monitorar logs em tempo real

```bash
# Terminal 1: Listener
stripe listen --forward-to localhost:8000/billing/webhook/stripe/

# Terminal 2: Logs do Django
docker-compose logs -f web | grep -E "(billing|notifications)"

# Terminal 3: Executar testes
stripe trigger checkout.session.completed
```

---

## ✅ Checklist Final de Testes

- [ ] Stripe listener rodando
- [ ] Webhook secret configurado no .env
- [ ] Container web reiniciado após configurar secret
- [ ] Teste 1: checkout.session.completed → [200] ✅
- [ ] Teste 2: customer.subscription.created → [200] ✅
- [ ] Teste 3: customer.subscription.updated → [200] ✅
- [ ] Teste 4: customer.subscription.deleted → [200] ✅
- [ ] Teste 5: invoice.payment_succeeded → [200] ✅
- [ ] Teste 6: invoice.payment_failed → [200] ✅
- [ ] Teste 7: customer.subscription.trial_will_end → [200] ✅
- [ ] Teste 8: charge.refunded → [200] ✅
- [ ] Facilities criadas no banco de dados ✅
- [ ] stripe_customer_id preenchido ✅
- [ ] Facility ativada/desativada conforme eventos ✅
- [ ] Email de boas-vindas enviado (checkout) ✅
- [ ] Logs registrando todos os eventos ✅

---

## 🎊 Testes Completos!

Se você marcou todos os itens acima, seus webhooks estão **100% funcionais**! 🎉

**Próximos passos:**
1. Implementar TODOs (emails de cancelamento, falha, etc.)
2. Configurar webhooks em produção (Stripe Dashboard)
3. Monitorar eventos reais de clientes

---

**Dica:** Salve este arquivo para referência futura ao adicionar novos eventos!

**Última atualização:** 2025-01-21
