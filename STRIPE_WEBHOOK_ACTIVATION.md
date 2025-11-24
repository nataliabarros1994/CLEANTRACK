# 🔔 Ativação do Webhook do Stripe - Guia Completo

## ✅ Status Atual

- ✅ Stripe CLI instalado: **v1.32.0**
- ✅ 8 webhook handlers implementados em `apps/billing/webhook_handlers.py`
- ✅ Endpoint configurado: `/billing/webhook/stripe/`
- ✅ Chaves do Stripe configuradas no `.env`
- ⚠️ **FALTA:** Webhook secret no `.env`

---

## 🚀 Opção 1: Teste Local com Stripe CLI (Desenvolvimento)

### Passo 1: Login no Stripe CLI

```bash
stripe login
```

Isso abrirá o navegador para autenticar. Pressione Enter após autorizar.

### Passo 2: Iniciar o Servidor Django

Em um terminal:

```bash
cd /home/nataliabarros1994/Desktop/CleanTrack
docker-compose up
```

OU sem Docker:

```bash
source venv/bin/activate
python manage.py runserver
```

### Passo 3: Iniciar o Stripe Webhook Listener

Em um **segundo terminal**:

```bash
cd /home/nataliabarros1994/Desktop/CleanTrack
stripe listen --forward-to localhost:8000/billing/webhook/stripe/
```

**Resultado esperado:**
```
> Ready! You are using Stripe API Version [2024-XX-XX]. Your webhook signing secret is whsec_xxxxxxxxxxxxx (^C to quit)
```

### Passo 4: Copiar o Webhook Secret

O comando acima mostrará um secret como:
```
whsec_1234567890abcdefghijklmnopqrstuvwxyz
```

Copie esse valor!

### Passo 5: Atualizar o .env

```bash
nano .env
```

Ou edite manualmente e atualize:
```bash
STRIPE_WEBHOOK_SECRET=whsec_1234567890abcdefghijklmnopqrstuvwxyz
```

### Passo 6: Reiniciar o Servidor Django

```bash
# Se usando Docker
docker-compose restart web

# Se local
# Ctrl+C no terminal do runserver e rodar novamente
python manage.py runserver
```

### Passo 7: Testar os Webhooks

Em um **terceiro terminal**:

```bash
# Testar checkout completo
stripe trigger checkout.session.completed

# Testar subscription criada
stripe trigger customer.subscription.created

# Testar subscription atualizada
stripe trigger customer.subscription.updated

# Testar subscription deletada
stripe trigger customer.subscription.deleted

# Testar pagamento bem-sucedido
stripe trigger invoice.payment_succeeded

# Testar pagamento falhado
stripe trigger invoice.payment_failed

# Testar trial expirando
stripe trigger customer.subscription.trial_will_end

# Testar reembolso
stripe trigger charge.refunded
```

### Passo 8: Verificar Logs

Verifique nos logs se os eventos foram recebidos:

```bash
# Ver logs em tempo real
tail -f logs/cleantrack.log | grep billing

# Ou logs do Docker
docker-compose logs -f web | grep billing
```

**Você deve ver algo como:**
```
INFO apps.billing.webhook_handlers: Handling checkout.session.completed for session cs_test_xxxxx
INFO apps.billing.webhook_handlers: Facility activated after successful checkout
```

---

## 🌐 Opção 2: Webhook em Produção (Stripe Dashboard)

### Passo 1: Fazer Deploy da Aplicação

Primeiro, coloque seu servidor em produção (ex: Render, Fly.io, AWS).

Exemplo de URL: `https://cleantrack.onrender.com`

### Passo 2: Acessar o Stripe Dashboard

1. Acesse: https://dashboard.stripe.com/
2. Faça login com sua conta
3. Vá para **Developers** → **Webhooks**

### Passo 3: Adicionar Endpoint

1. Clique em **Add endpoint**
2. Cole a URL do seu servidor + `/billing/webhook/stripe/`

   Exemplo:
   ```
   https://cleantrack.onrender.com/billing/webhook/stripe/
   ```

3. Em **Events to send**, selecione:
   - ✅ `checkout.session.completed`
   - ✅ `customer.subscription.created`
   - ✅ `customer.subscription.updated`
   - ✅ `customer.subscription.deleted`
   - ✅ `invoice.payment_succeeded`
   - ✅ `invoice.payment_failed`
   - ✅ `customer.subscription.trial_will_end`
   - ✅ `charge.refunded`

4. Clique em **Add endpoint**

### Passo 4: Copiar o Webhook Secret

Após criar o endpoint:

1. Clique no endpoint criado
2. Clique em **Reveal** na seção "Signing secret"
3. Copie o secret (formato: `whsec_...`)

### Passo 5: Adicionar ao .env em Produção

Dependendo da plataforma:

**Render:**
```
Dashboard → Environment → Add Variable
Key: STRIPE_WEBHOOK_SECRET
Value: whsec_xxxxxxxxxxxxx
```

**Fly.io:**
```bash
fly secrets set STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
```

**Heroku:**
```bash
heroku config:set STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
```

**AWS ECS:**
Adicione na Task Definition como variável de ambiente.

### Passo 6: Fazer Redeploy

Reinicie a aplicação para carregar a nova variável.

### Passo 7: Testar em Produção

No Stripe Dashboard:

1. Vá para **Developers** → **Webhooks**
2. Clique no seu endpoint
3. Clique na aba **Send test webhook**
4. Selecione um evento (ex: `checkout.session.completed`)
5. Clique em **Send test webhook**

Verifique se o status aparece como **Succeeded** (200).

---

## 🧪 Teste Rápido Sem Stripe CLI

Você também pode testar localmente sem o Stripe CLI:

```bash
cd /home/nataliabarros1994/Desktop/CleanTrack
python apps/billing/test_webhooks.py
```

Este script simula eventos de webhook localmente para validar os handlers.

---

## 📋 Checklist de Ativação

### Desenvolvimento Local

- [ ] Stripe CLI instalado (✅ já está!)
- [ ] Fazer login no Stripe CLI (`stripe login`)
- [ ] Iniciar servidor Django
- [ ] Iniciar listener: `stripe listen --forward-to localhost:8000/billing/webhook/stripe/`
- [ ] Copiar webhook secret exibido
- [ ] Atualizar `.env` com o secret
- [ ] Reiniciar servidor Django
- [ ] Testar com `stripe trigger`
- [ ] Verificar logs

### Produção

- [ ] Deploy da aplicação em servidor público
- [ ] Acessar Stripe Dashboard → Webhooks
- [ ] Adicionar endpoint com URL pública
- [ ] Selecionar os 8 eventos
- [ ] Copiar webhook secret
- [ ] Adicionar secret nas variáveis de ambiente do servidor
- [ ] Fazer redeploy
- [ ] Testar com "Send test webhook" no dashboard
- [ ] Monitorar logs de produção

---

## 🔍 Troubleshooting

### Problema: "Webhook signing secret not found"

**Solução:** Verifique se `STRIPE_WEBHOOK_SECRET` está no `.env` e foi carregado.

```bash
# Verificar se a variável está carregada
docker-compose exec web python manage.py shell

from django.conf import settings
print(settings.STRIPE_WEBHOOK_SECRET)
```

### Problema: "400 Bad Request" nos webhooks

**Solução:** Verifique se o endpoint está correto e o servidor está rodando.

```bash
# Testar se o endpoint responde
curl -X POST http://localhost:8000/billing/webhook/stripe/
```

### Problema: Eventos não aparecem nos logs

**Solução:** Verifique se o handler está registrado corretamente.

```bash
# Ver se os handlers foram registrados
grep "Registering Stripe webhook handler" logs/cleantrack.log
```

Deve aparecer 8 linhas como:
```
INFO apps.billing.apps: Registering Stripe webhook handler for: checkout.session.completed
```

### Problema: "No matching webhook handler"

**Solução:** Certifique-se de que `apps.billing` está em `INSTALLED_APPS` no settings.py.

### Problema: Stripe CLI não recebe eventos

**Solução:**

1. Verifique se está logado: `stripe login`
2. Verifique se o servidor está rodando
3. Tente com `--skip-verify`:
   ```bash
   stripe listen --forward-to localhost:8000/billing/webhook/stripe/ --skip-verify
   ```

---

## 📊 Eventos Configurados

| Evento | Ação |
|--------|------|
| `checkout.session.completed` | Ativa facility + envia email de boas-vindas |
| `customer.subscription.created` | Ativa facility |
| `customer.subscription.updated` | Atualiza status da facility |
| `customer.subscription.deleted` | Desativa facility |
| `invoice.payment_succeeded` | Garante facility ativa |
| `invoice.payment_failed` | Desativa após 3 falhas |
| `customer.subscription.trial_will_end` | Log de alerta (3 dias antes) |
| `charge.refunded` | Log de reembolso |

---

## 🚀 Comandos Rápidos

### Desenvolvimento

```bash
# Terminal 1: Servidor Django
docker-compose up

# Terminal 2: Stripe Listener
stripe listen --forward-to localhost:8000/billing/webhook/stripe/

# Terminal 3: Testar eventos
stripe trigger checkout.session.completed
stripe trigger invoice.payment_succeeded
stripe trigger customer.subscription.deleted

# Ver logs
tail -f logs/cleantrack.log | grep billing
```

### Ver Webhooks Recebidos

```bash
# Últimos 50 webhooks
stripe logs tail

# Filtrar por evento
stripe logs tail --filter-event-type checkout.session.completed
```

---

## 📚 Documentação Adicional

- **Stripe Webhooks:** https://stripe.com/docs/webhooks
- **Stripe CLI:** https://stripe.com/docs/stripe-cli
- **dj-stripe Webhooks:** https://dj-stripe.readthedocs.io/en/latest/usage/webhooks.html
- **Eventos do Stripe:** https://stripe.com/docs/api/events/types

---

## 🎯 Próximos Passos

Após ativar os webhooks:

1. **Testar fluxo completo:**
   - Criar checkout session
   - Completar pagamento
   - Verificar facility ativada
   - Confirmar email enviado

2. **Implementar TODOs:**
   - Email de cancelamento
   - Email de falha de pagamento
   - Email de fim de trial
   - Email de reembolso

3. **Monitoramento:**
   - Configurar alertas para webhooks falhados
   - Dashboard de métricas de billing
   - Logs estruturados

---

✅ **Você está pronto para ativar os webhooks do Stripe!**

Escolha entre desenvolvimento local (Opção 1) ou produção (Opção 2) e siga os passos.
