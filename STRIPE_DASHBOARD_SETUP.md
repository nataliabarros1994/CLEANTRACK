# 🎯 Configuração do Webhook no Stripe Dashboard - Guia Visual

## ⚠️ IMPORTANTE: Desenvolvimento Local vs Produção

### Para Desenvolvimento Local (Testando Localmente)

**NÃO use o Stripe Dashboard para desenvolvimento local!**

Use o Stripe CLI:
```bash
stripe listen --forward-to localhost:8000/billing/webhook/stripe/
```

**Por quê?**
- O Stripe Dashboard só consegue enviar webhooks para URLs públicas (HTTPS)
- `http://localhost:8000` NÃO é acessível pela internet
- O Stripe CLI cria um túnel seguro para sua máquina local

---

### Para Produção (Servidor Público)

Use o Stripe Dashboard quando seu servidor estiver em produção (ex: Render, Heroku, AWS).

---

## 🚀 Opção 1: Desenvolvimento Local (RECOMENDADO AGORA)

### Passo 1: Verificar se containers estão rodando

```bash
docker-compose ps
```

Deve mostrar:
```
cleantrack_web_1    Up    0.0.0.0:8000->8000/tcp
cleantrack_db_1     Up    0.0.0.0:5432->5432/tcp
```

### Passo 2: Login no Stripe CLI

```bash
stripe login
```

Isso abrirá o navegador para autenticar. Pressione Enter após autorizar.

### Passo 3: Iniciar o Listener

```bash
stripe listen --forward-to localhost:8000/billing/webhook/stripe/
```

**Você verá:**
```
> Ready! You are using Stripe API Version [2024-XX-XX]
> Your webhook signing secret is whsec_abc123def456ghi789jkl012mno345pqr678
```

### Passo 4: Copiar o Webhook Secret

Copie o valor `whsec_...` que apareceu.

### Passo 5: Atualizar o .env

```bash
nano .env
```

Encontre:
```
STRIPE_WEBHOOK_SECRET=whsec_...
```

Substitua por (cole o secret copiado):
```
STRIPE_WEBHOOK_SECRET=whsec_abc123def456ghi789jkl012mno345pqr678stu901
```

Salve: `Ctrl+O`, Enter, `Ctrl+X`

### Passo 6: Reiniciar o Container

```bash
docker-compose restart web
```

### Passo 7: Testar

Em outro terminal:
```bash
stripe trigger checkout.session.completed
```

Verifique no terminal do listener se apareceu:
```
[200] POST /billing/webhook/stripe/ [evt_xxxx]
```

**✅ Se viu [200], o webhook está funcionando!**

---

## 🌐 Opção 2: Produção (Stripe Dashboard)

Use isso APENAS quando seu servidor estiver em produção com domínio público.

### Requisitos:
- ✅ Servidor em produção (ex: `https://cleantrack.onrender.com`)
- ✅ Domínio público acessível pela internet
- ✅ HTTPS configurado (obrigatório)

### Passo 1: Acessar Stripe Dashboard

1. Acesse: https://dashboard.stripe.com/
2. Faça login com sua conta Stripe
3. Certifique-se de estar em **modo de teste** (toggle no canto superior direito)

### Passo 2: Navegar para Webhooks

1. Clique em **Developers** no menu superior
2. Clique em **Webhooks** no menu lateral

### Passo 3: Adicionar Endpoint

1. Clique no botão **"Add endpoint"** (ou "+ Add an endpoint")
2. Você verá um formulário

### Passo 4: Configurar o Endpoint

#### Endpoint URL:
```
https://seu-dominio.com/billing/webhook/stripe/
```

**Exemplos:**
- Render: `https://cleantrack.onrender.com/billing/webhook/stripe/`
- Heroku: `https://cleantrack-app.herokuapp.com/billing/webhook/stripe/`
- Custom: `https://cleantrack.app/billing/webhook/stripe/`

⚠️ **IMPORTANTE:**
- Use `https://` (não `http://`)
- Inclua a barra `/` no final
- Não use `localhost` (não funcionará!)

#### Versão da API:
Deixe em branco ou selecione a versão mais recente.

#### Events to send:

**Opção A: Selecionar os 8 eventos específicos** (Recomendado)

Clique em **"Select events"** e procure por cada um:

1. ✅ `checkout.session.completed`
2. ✅ `customer.subscription.created`
3. ✅ `customer.subscription.updated`
4. ✅ `customer.subscription.deleted`
5. ✅ `invoice.payment_succeeded`
6. ✅ `invoice.payment_failed`
7. ✅ `customer.subscription.trial_will_end`
8. ✅ `charge.refunded`

**Opção B: Selecionar todos** (Para teste)

Clique em **"Select all"** para receber todos os eventos.

⚠️ Em produção, selecione apenas os eventos que você precisa (Opção A).

### Passo 5: Criar o Endpoint

1. Clique em **"Add endpoint"**
2. O endpoint será criado

### Passo 6: Copiar o Webhook Secret

1. Você será redirecionado para a página do endpoint
2. Na seção **"Signing secret"**, clique em **"Reveal"**
3. Copie o secret que aparece (formato: `whsec_...`)

**Exemplo:**
```
whsec_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

### Passo 7: Adicionar Secret nas Variáveis de Ambiente

#### Render:
1. Vá para seu serviço no Render Dashboard
2. Clique em **Environment**
3. Adicione:
   - Key: `STRIPE_WEBHOOK_SECRET`
   - Value: `whsec_...` (cole o secret)
4. Clique em **Save Changes**

#### Heroku:
```bash
heroku config:set STRIPE_WEBHOOK_SECRET=whsec_...
```

#### Fly.io:
```bash
fly secrets set STRIPE_WEBHOOK_SECRET=whsec_...
```

#### AWS ECS:
Adicione na Task Definition como variável de ambiente.

#### VPS (manual):
```bash
# Editar .env no servidor
nano .env

# Adicionar
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Passo 8: Redeploy (se necessário)

Reinicie sua aplicação para carregar a nova variável:
- **Render:** Redeploy automático
- **Heroku:** `git push heroku main`
- **Fly.io:** `fly deploy`
- **VPS:** `sudo systemctl restart cleantrack`

### Passo 9: Testar o Webhook

1. Volte para o Stripe Dashboard
2. Clique no endpoint que você criou
3. Clique na aba **"Send test webhook"**
4. Selecione um evento (ex: `checkout.session.completed`)
5. Clique em **"Send test webhook"**

**Resultado esperado:**
- Status: **Succeeded** (200)
- Response time: < 1s

Se aparecer erro:
- ❌ **Failed (404)**: URL incorreta
- ❌ **Failed (500)**: Erro no servidor
- ❌ **Failed (timeout)**: Servidor não respondeu

### Passo 10: Verificar Logs

No seu servidor, verifique os logs:

```bash
# Render
render logs

# Heroku
heroku logs --tail

# Docker
docker-compose logs -f web | grep billing
```

Você deve ver:
```
INFO apps.billing.webhook_handlers: Handling checkout.session.completed for session cs_test_xxxxx
INFO apps.billing.webhook_handlers: Facility activated after successful checkout
```

---

## 📋 Checklist de Configuração

### Desenvolvimento Local (Stripe CLI)
- [ ] Containers rodando (`docker-compose ps`)
- [ ] Login no Stripe CLI (`stripe login`)
- [ ] Listener iniciado (`stripe listen --forward-to...`)
- [ ] Webhook secret copiado
- [ ] `.env` atualizado com secret
- [ ] Container reiniciado (`docker-compose restart web`)
- [ ] Testado com `stripe trigger`
- [ ] Logs verificados ([200] apareceu)

### Produção (Stripe Dashboard)
- [ ] Servidor em produção com domínio público
- [ ] HTTPS configurado
- [ ] Acessado Stripe Dashboard
- [ ] Navegado para Developers > Webhooks
- [ ] Clicado em "Add endpoint"
- [ ] URL configurada (https://...)
- [ ] 8 eventos selecionados (ou "Select all")
- [ ] Endpoint criado
- [ ] Webhook secret copiado
- [ ] Secret adicionado nas variáveis de ambiente
- [ ] Aplicação redeployada
- [ ] Teste enviado pelo dashboard (Succeeded)
- [ ] Logs verificados (eventos recebidos)

---

## 🎯 Os 8 Eventos Implementados

Quando for selecionar no Stripe Dashboard, procure por esses nomes EXATOS:

| # | Nome do Evento | O que faz |
|---|----------------|-----------|
| 1 | `checkout.session.completed` | Ativa facility após pagamento |
| 2 | `customer.subscription.created` | Ativa facility quando assinatura criada |
| 3 | `customer.subscription.updated` | Atualiza status da facility |
| 4 | `customer.subscription.deleted` | Desativa facility quando cancelada |
| 5 | `invoice.payment_succeeded` | Confirma facility ativa após pagamento |
| 6 | `invoice.payment_failed` | Desativa facility após 3 falhas |
| 7 | `customer.subscription.trial_will_end` | Alerta 3 dias antes do fim do trial |
| 8 | `charge.refunded` | Registra reembolsos |

---

## 🔍 Como Encontrar os Eventos no Dashboard

No formulário de criação do endpoint:

1. Clique em **"Select events"**
2. Use a busca para encontrar cada evento:
   - Digite: `checkout.session` → Selecione `checkout.session.completed`
   - Digite: `customer.subscription` → Selecione os 3 eventos
   - Digite: `invoice.payment` → Selecione os 2 eventos
   - Digite: `trial_will_end` → Selecione
   - Digite: `charge.refunded` → Selecione

3. Quando terminar, você verá: **"8 events selected"**

4. Clique em **"Add events"**

---

## 🆘 Troubleshooting

### Erro: "URL must be a public endpoint"

**Problema:** Você tentou usar `http://localhost` no Stripe Dashboard

**Solução:** Use o Stripe CLI para desenvolvimento local (Opção 1)

### Erro: "Failed to send test webhook (404)"

**Problema:** URL incorreta ou rota não existe

**Solução:**
1. Verifique a URL: `https://seu-dominio.com/billing/webhook/stripe/`
2. Certifique-se de que a rota existe no Django
3. Verifique os logs do servidor

### Erro: "Webhook signature verification failed"

**Problema:** Secret incorreto ou não configurado

**Solução:**
1. Copie novamente o secret do Stripe Dashboard
2. Atualize a variável de ambiente
3. Redeploy a aplicação
4. Reinicie o servidor

### Erro: "Failed to send test webhook (500)"

**Problema:** Erro no código do handler

**Solução:**
1. Veja os logs do servidor para identificar o erro
2. Verifique se todos os handlers estão registrados
3. Verifique se o código está correto

### Webhook recebido mas nada acontece

**Problema:** Handler não está registrado ou não está sendo chamado

**Solução:**
1. Verifique os logs: `grep "Registering Stripe webhook handler" logs/cleantrack.log`
2. Deve aparecer 8 linhas
3. Se não aparecer, verifique `apps/billing/apps.py`

---

## 📚 Documentação de Referência

- **Stripe Webhooks:** https://stripe.com/docs/webhooks
- **Stripe CLI:** https://stripe.com/docs/stripe-cli
- **dj-stripe:** https://dj-stripe.readthedocs.io/
- **Eventos do Stripe:** https://stripe.com/docs/api/events/types

---

## 🎊 Resumo

### Para AGORA (Desenvolvimento Local):
✅ Use o Stripe CLI com `stripe listen`
✅ Copie o secret gerado
✅ Atualize o `.env`
✅ Teste com `stripe trigger`

### Para DEPOIS (Produção):
✅ Configure webhook no Stripe Dashboard
✅ Use URL pública com HTTPS
✅ Selecione os 8 eventos
✅ Copie o secret do dashboard
✅ Configure nas variáveis de ambiente do servidor
✅ Teste pelo dashboard

---

**Você está configurando para desenvolvimento local ou produção?**

- **Local:** Siga a Opção 1 (Stripe CLI)
- **Produção:** Siga a Opção 2 (Stripe Dashboard)

---

**Última atualização:** 2025-01-21
