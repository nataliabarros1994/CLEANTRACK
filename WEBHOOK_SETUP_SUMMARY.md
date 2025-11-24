# 🎯 Resumo: Ativação do Webhook do Stripe

## ✅ O que foi criado

Foram criados **4 arquivos** para facilitar a configuração do webhook:

1. **`STRIPE_WEBHOOK_ACTIVATION.md`** (documentação completa)
2. **`WEBHOOK_QUICK_START.md`** (guia rápido de 3 passos)
3. **`activate_stripe_webhook.sh`** (script automatizado)
4. **`test_stripe_connection.py`** (script de teste)

---

## 🚀 Como Ativar o Webhook (Escolha uma opção)

### Opção 1: Manual (Mais Simples) ⭐ **RECOMENDADO**

#### **Passo 1:** Inicie o servidor Django

Em um terminal:

```bash
cd /home/nataliabarros1994/Desktop/CleanTrack
docker-compose up
```

#### **Passo 2:** Inicie o Stripe listener

Em um **segundo terminal**:

```bash
# Se necessário, faça login primeiro (apenas 1ª vez)
stripe login

# Inicie o listener
stripe listen --forward-to localhost:8000/billing/webhook/stripe/
```

**Você verá algo assim:**
```
> Ready! You are using Stripe API Version [2024-XX-XX]
> Your webhook signing secret is whsec_abc123def456ghi789jkl012mno345pqr
                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

#### **Passo 3:** Copie o webhook secret

Copie o `whsec_...` que apareceu acima.

#### **Passo 4:** Atualize o .env

```bash
nano .env
```

Encontre a linha:
```
STRIPE_WEBHOOK_SECRET=whsec_...
```

E substitua por:
```
STRIPE_WEBHOOK_SECRET=whsec_abc123def456ghi789jkl012mno345pqr
```

(Use o secret que você copiou)

Salve com `Ctrl+O`, Enter, `Ctrl+X`

#### **Passo 5:** Reinicie o servidor

No **primeiro terminal**, pressione `Ctrl+C` e execute:

```bash
docker-compose restart web
```

#### **Passo 6:** Teste

Em um **terceiro terminal**:

```bash
stripe trigger checkout.session.completed
```

Verifique no **segundo terminal** (listener) se apareceu:
```
[200] POST /billing/webhook/stripe/ [evt_xxxx]
```

**✅ Pronto! Webhook configurado e funcionando!**

---

### Opção 2: Script Automatizado

```bash
cd /home/nataliabarros1994/Desktop/CleanTrack
./activate_stripe_webhook.sh
```

O script vai guiá-lo por todos os passos automaticamente.

---

## 🔍 Como Verificar se Está Funcionando

### 1. Ver logs do listener

No terminal onde o `stripe listen` está rodando, você deve ver:

```
[200] POST /billing/webhook/stripe/ [evt_xxxx]
```

O `[200]` indica sucesso!

### 2. Ver logs do Django

```bash
tail -f logs/cleantrack.log | grep billing
```

Você deve ver:

```
INFO apps.billing.webhook_handlers: Handling checkout.session.completed for session cs_test_xxxxx
INFO apps.billing.webhook_handlers: Facility activated after successful checkout
```

### 3. Verificar no Admin

Acesse: http://localhost:8000/admin/facilities/facility/

Se você testou `checkout.session.completed`, deve ter uma nova facility criada com:
- `is_active = True` ✅
- `stripe_customer_id` preenchido

---

## 🧪 Testes Disponíveis

### Testar todos os 8 eventos:

```bash
# 1. Checkout completo
stripe trigger checkout.session.completed

# 2. Subscription criada
stripe trigger customer.subscription.created

# 3. Subscription atualizada
stripe trigger customer.subscription.updated

# 4. Subscription deletada
stripe trigger customer.subscription.deleted

# 5. Pagamento bem-sucedido
stripe trigger invoice.payment_succeeded

# 6. Pagamento falhado
stripe trigger invoice.payment_failed

# 7. Trial expirando
stripe trigger customer.subscription.trial_will_end

# 8. Reembolso
stripe trigger charge.refunded
```

---

## ❌ Troubleshooting

### Problema: "stripe: command not found"

**Solução:** Instale o Stripe CLI:

```bash
# Verificar se está no PATH
which stripe

# Se não estiver, adicione ao PATH
export PATH="$HOME/.local/bin:$PATH"

# Ou instale novamente
# macOS: brew install stripe/stripe-cli/stripe
# Linux: wget https://github.com/stripe/stripe-cli/releases/latest/download/stripe_*_linux_x86_64.tar.gz
```

### Problema: "Connection refused" no listener

**Solução:** Certifique-se de que o servidor Django está rodando ANTES de iniciar o listener.

```bash
# Verificar se está rodando
curl http://localhost:8000
```

### Problema: "Webhook signature verification failed"

**Solução:**

1. Verifique se o `.env` foi atualizado corretamente
2. Reinicie o servidor Django
3. Verifique se o secret no `.env` corresponde ao do listener

```bash
# Ver o secret atual no .env
grep STRIPE_WEBHOOK_SECRET .env

# Ver o secret no listener
# Deve aparecer quando você executa: stripe listen --forward-to localhost:8000/billing/webhook/stripe/
```

### Problema: Eventos não aparecem nos logs

**Solução:** Verifique se os handlers foram registrados:

```bash
grep "Registering Stripe webhook handler" logs/cleantrack.log
```

Deve aparecer 8 linhas.

---

## 📁 Documentação Disponível

| Arquivo | Descrição |
|---------|-----------|
| `WEBHOOK_QUICK_START.md` | Guia rápido de 3 passos |
| `STRIPE_WEBHOOK_ACTIVATION.md` | Documentação completa |
| `activate_stripe_webhook.sh` | Script automatizado |
| `test_stripe_connection.py` | Script de teste |
| `WEBHOOK_SETUP_SUMMARY.md` | Este arquivo |

---

## 🎯 Status dos Handlers Implementados

✅ **8 webhook handlers configurados:**

| Evento | Status | Ação |
|--------|--------|------|
| `checkout.session.completed` | ✅ | Ativa facility + email |
| `customer.subscription.created` | ✅ | Ativa facility |
| `customer.subscription.updated` | ✅ | Atualiza status |
| `customer.subscription.deleted` | ✅ | Desativa facility |
| `invoice.payment_succeeded` | ✅ | Garante ativa |
| `invoice.payment_failed` | ✅ | Desativa após 3 falhas |
| `customer.subscription.trial_will_end` | ✅ | Log de aviso |
| `charge.refunded` | ✅ | Log de reembolso |

---

## ✅ Checklist de Ativação

- [ ] Stripe CLI instalado (`stripe --version`)
- [ ] Login no Stripe CLI (`stripe login`)
- [ ] Servidor Django rodando
- [ ] Listener iniciado (`stripe listen --forward-to...`)
- [ ] Webhook secret copiado
- [ ] `.env` atualizado com o secret
- [ ] Servidor Django reiniciado
- [ ] Teste executado (`stripe trigger checkout.session.completed`)
- [ ] Logs verificados (deve aparecer [200])

---

## 🎉 Pronto!

Após seguir os passos acima, seu webhook do Stripe estará **100% funcional**!

**Mantenha o terminal com `stripe listen` rodando enquanto estiver desenvolvendo.**

Para produção, consulte a seção "Opção 2: Webhook em Produção" no arquivo `STRIPE_WEBHOOK_ACTIVATION.md`.

---

**Última atualização:** 2025-01-21
