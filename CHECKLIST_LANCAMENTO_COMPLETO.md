# ✅ Checklist de Lançamento CleanTrack - Completo

## 📊 Status Geral do Projeto

```
████████████████░░░░  80% Completo

✅ Backend desenvolvido
✅ Landing page criada
✅ Configurações prontas
⏳ Deploy pendente
⏳ Integrações pendentes
```

---

## 🎯 FASE 1: Landing Page (Prioridade MÁXIMA)

### Status: 🟡 Pronto para Deploy

| Tarefa | Status | Arquivo | Próxima Ação |
|--------|--------|---------|--------------|
| Landing page HTML criada | ✅ | `index.html` | Deploy no Netlify |
| Configurar Calendly | ⏳ | - | Criar conta + copiar link |
| Configurar Formspree | ⏳ | - | Criar conta + copiar ID |
| Deploy no Netlify | ⏳ | `netlify.toml` | Drag & drop |
| Domínio personalizado | ⏳ | - | Configurar DNS |

### ⚡ Ação Imediata - Landing Page:

```bash
TEMPO ESTIMADO: 15 minutos

1. Calendly (5 min):
   - Criar conta: calendly.com
   - Criar evento: "CleanTrack Onboarding" (30 min)
   - Copiar link: https://calendly.com/seu-usuario/cleantrack-onboarding
   - Editar index.html linha 170

2. Formspree (3 min):
   - Criar conta: formspree.io
   - Criar form: "CleanTrack Leads"
   - Copiar ID: xwpkabcd
   - Editar index.html linha 264

3. Deploy Netlify (2 min):
   - Acessar: app.netlify.com/drop
   - Arrastar pasta CleanTrack
   - Pronto! ✅

4. Atualizar contatos (5 min):
   - Editar index.html linhas 326-334
   - Seu email e WhatsApp reais
```

**URL após deploy:** `https://nome-aleatorio.netlify.app`

---

## 🚀 FASE 2: Backend no Render

### Status: 🟡 Código Pronto, Aguardando Push

| Tarefa | Status | Detalhes |
|--------|--------|----------|
| Código no GitHub | 🟢 PRONTO | Commit criado (61 arquivos) |
| render.yaml configurado | ✅ | Na raiz do projeto |
| .gitignore configurado | ✅ | Sem senhas |
| SECRET_KEY gerada | ✅ | `rv2o%rw13na2+j3...` |
| Conta no Render criada | ⏳ | dashboard.render.com |
| Push para GitHub | ⏳ | Aguardando ação |
| Deploy no Render | ⏳ | Após push |
| Secrets configurados | ⏳ | Após deploy |
| Superusuário criado | ⏳ | Após deploy |

### ⚡ Ação Imediata - Backend:

```bash
TEMPO ESTIMADO: 10 minutos

1. Criar repositório GitHub (2 min):
   - Acessar: github.com/new
   - Nome: cleantrack-backend
   - Private
   - Create repository

2. Push código (1 min):
   cd /home/nataliabarros1994/Desktop/CleanTrack
   git remote add origin https://github.com/SEU-USUARIO/cleantrack-backend.git
   git push -u origin main

3. Deploy Render com Blueprint (5 min):
   - Acessar: dashboard.render.com
   - New + > Blueprint
   - Conectar: cleantrack-backend
   - Apply (Render detecta render.yaml)
   - Aguardar deploy

4. Configurar SECRET_KEY (2 min):
   - Environment > SECRET_KEY
   - Valor: rv2o%rw13na2+j3zsciqqu4pfu_fw=jv05c1%0ivauwgi&u7v5
   - Save
```

**URL após deploy:** `https://cleantrack-api.onrender.com`

---

## 📧 FASE 3: Resend (Email)

### Status: ⏳ Aguardando Configuração

| Tarefa | Status | Tempo |
|--------|--------|-------|
| Criar conta Resend | ⏳ | 2 min |
| Gerar API Key | ⏳ | 1 min |
| Adicionar no Render | ⏳ | 2 min |
| Testar email | ⏳ | 5 min |
| Verificar domínio | ⏳ | 10 min |

### ⚡ Ação Imediata - Email:

```bash
TEMPO ESTIMADO: 20 minutos

1. Criar conta (2 min):
   - resend.com/signup
   - Confirmar email

2. Criar API Key (1 min):
   - Dashboard > API Keys
   - Create: "CleanTrack Production"
   - Copiar: re_xxxxxxxxxx

3. Adicionar no Render (2 min):
   - Environment > RESEND_API_KEY
   - Colar chave
   - Save

4. Testar (5 min):
   - Render > Shell
   - python manage.py shell
   - Enviar email de teste

5. Verificar domínio (10 min):
   - Resend > Add Domain
   - cleantrack.com.br
   - Configurar DNS (3 registros)
```

**Guia completo:** `RESEND_SETUP_GUIDE.md`

---

## 💳 FASE 4: Stripe (Pagamentos)

### Status: ⏳ Aguardando Configuração

| Tarefa | Status | Modo | Tempo |
|--------|--------|------|-------|
| Criar conta Stripe | ⏳ | - | 5 min |
| Obter Test Keys | ⏳ | Test | 2 min |
| Criar produtos (3 planos) | ⏳ | Test | 10 min |
| Configurar webhook | ⏳ | Test | 5 min |
| Testar pagamento | ⏳ | Test | 10 min |
| Completar cadastro | ⏳ | Live | 30 min |
| Obter Live Keys | ⏳ | Live | 2 min |
| Recriar produtos | ⏳ | Live | 5 min |
| Webhook produção | ⏳ | Live | 5 min |

### ⚡ Ação Imediata - Stripe (Test Mode):

```bash
TEMPO ESTIMADO: 30 minutos

1. Criar conta (5 min):
   - stripe.com/br
   - Confirmar email

2. Test Keys (2 min):
   - Dashboard > Test mode ON
   - Developers > API Keys
   - Copiar pk_test_xxx e sk_test_xxx

3. Criar produtos (10 min):
   - Products > Add Product
   - Starter: R$ 200/mês
   - Professional: R$ 500/mês
   - Enterprise: R$ 1.200/mês
   - Copiar Price IDs

4. Webhook (5 min):
   - Developers > Webhooks
   - Add endpoint
   - URL: https://cleantrack-api.onrender.com/billing/webhook/
   - Eventos: subscriptions + invoices
   - Copiar whsec_xxx

5. Adicionar no Render (3 min):
   - STRIPE_PUBLIC_KEY=pk_test_xxx
   - STRIPE_SECRET_KEY=sk_test_xxx
   - STRIPE_WEBHOOK_SECRET=whsec_xxx

6. Testar (5 min):
   - Criar checkout session
   - Pagar com 4242 4242 4242 4242
   - Verificar webhook recebido
```

**Guia completo:** `STRIPE_SETUP_COMPLETE.md`

---

## 🎬 FASE 5: Demo e Marketing

### Status: ⏳ Aguardando Produto Online

| Tarefa | Status | Depende de |
|--------|--------|------------|
| Script demo vídeo | ✅ | - |
| Gravar demo (3 min) | ⏳ | Landing + Backend live |
| Criar pitch deck | ✅ | - |
| Enviar para investidores | ⏳ | Demo gravado |
| Post LinkedIn | ⏳ | Landing page live |
| Grupos WhatsApp | ⏳ | Landing page live |

### ⚡ Ação Imediata - Marketing:

```bash
QUANDO: Após landing page + backend no ar

1. Gravar demo (15 min):
   - Usar script: SCRIPT_DEMO_VIDEO_3MIN.md
   - Ferramenta: Loom ou OBS
   - Upload: YouTube (unlisted)

2. LinkedIn (10 min):
   - Post de lançamento
   - Compartilhar em grupos de saúde
   - Tag: #healthtech #startups

3. Divulgação direta (30 min):
   - Email para contatos da área
   - WhatsApp para clínicas conhecidas
   - Grupos Facebook de gestão hospitalar
```

**Recursos criados:**
- `SCRIPT_DEMO_VIDEO_3MIN.md`
- `PITCH_DECK_INVESTIDORES.md`
- `PLANO_ONBOARDING_CLIENTES_PILOTO.md`

---

## 📋 PRIORIZAÇÃO - O QUE FAZER AGORA

### 🔥 HOJE (1-2 horas):

```
┌─────────────────────────────────────────────────┐
│ 1. Landing Page Deploy (15 min)                │
│    ✓ Configurar Calendly                       │
│    ✓ Configurar Formspree                      │
│    ✓ Deploy no Netlify                         │
│                                                 │
│ 2. Backend Deploy (10 min)                     │
│    ✓ Push para GitHub                          │
│    ✓ Deploy no Render                          │
│    ✓ Criar superuser                           │
│                                                 │
│ 3. Testar tudo (10 min)                        │
│    ✓ Landing page funcionando                  │
│    ✓ Formulário enviando                       │
│    ✓ Admin acessível                           │
│                                                 │
│ RESULTADO: Produto minimamente viável no ar!   │
└─────────────────────────────────────────────────┘
```

### 📅 ESTA SEMANA (2-3 horas):

```
1. Resend (Email) - 20 min
2. Stripe Test Mode - 30 min
3. Gravar demo - 15 min
4. Começar divulgação - 1 hora
```

### 📅 PRÓXIMAS 2 SEMANAS:

```
1. Completar cadastro Stripe
2. Ativar Live Mode
3. Conseguir 10 clientes piloto
4. Coletar feedback
5. Iterar produto
```

---

## 💰 Investimento Necessário

### Custos Iniciais (Primeiros 3 meses):

```
┌─────────────────────────┬──────────┬───────────┐
│ Item                    │ Custo    │ Período   │
├─────────────────────────┼──────────┼───────────┤
│ Netlify (landing)       │ R$ 0     │ Grátis    │
│ Render (backend)        │ R$ 0     │ 90d free  │
│ Render (database)       │ R$ 0     │ 90d free  │
│ Resend (3k emails)      │ R$ 0     │ Grátis    │
│ Stripe (sem mensalidade)│ R$ 0     │ Por trx   │
│ Domínio .com.br         │ R$ 40    │ 1 ano     │
├─────────────────────────┼──────────┼───────────┤
│ TOTAL PRIMEIROS 3 MESES │ R$ 40    │           │
└─────────────────────────┴──────────┴───────────┘

Após 90 dias (com clientes):
- Render Starter: R$ 70/mês
- Resend Pro: R$ 100/mês (se >3k emails)
- TOTAL: ~R$ 170/mês
```

---

## 🎯 Metas de Tração (30 dias)

```
Semana 1:
□ Landing page no ar
□ Backend deployado
□ 50 visitas na landing
□ 10 formulários preenchidos
□ 5 agendamentos

Semana 2:
□ 3 demos realizadas
□ 2 clientes piloto confirmados
□ Resend + Stripe configurados
□ Email de boas-vindas automático

Semana 3-4:
□ 5 clientes piloto usando
□ Feedback coletado
□ Melhorias implementadas
□ 10 clientes piloto completos
```

---

## 📞 Recursos e Suporte

### Documentação Criada:

- ✅ `CHECKLIST_DEPLOY.md` - Checklist detalhado
- ✅ `GITHUB_PUSH_INSTRUCTIONS.md` - Push e deploy
- ✅ `DEPLOY_RENDER_PASSO_A_PASSO.md` - Render completo
- ✅ `RESEND_SETUP_GUIDE.md` - Email configuração
- ✅ `STRIPE_SETUP_COMPLETE.md` - Pagamentos completo
- ✅ `PRODUCTION_SETUP_GUIDE.md` - Guia geral produção
- ✅ `LANDING_PAGE_SETUP.md` - Landing page
- ✅ `PLANO_ONBOARDING_CLIENTES_PILOTO.md` - Onboarding

### Links Úteis:

- Netlify: https://app.netlify.com
- Render: https://dashboard.render.com
- Resend: https://resend.com/emails
- Stripe: https://dashboard.stripe.com
- Calendly: https://calendly.com
- Formspree: https://formspree.io

---

## ✅ Checklist Rápido - Copiar e Colar

```
FASE 1 - LANDING PAGE (HOJE):
□ Criar conta Calendly
□ Copiar link do Calendly
□ Editar index.html linha 170
□ Criar conta Formspree
□ Copiar ID do Formspree
□ Editar index.html linha 264
□ Atualizar email/WhatsApp (linhas 326-334)
□ Deploy no Netlify (drag & drop)
□ Testar formulário
□ Testar agendamento

FASE 2 - BACKEND (HOJE):
□ Criar repo GitHub (cleantrack-backend)
□ git remote add origin [URL]
□ git push -u origin main
□ Criar conta Render
□ New + > Blueprint
□ Conectar ao GitHub
□ Apply (Render detecta render.yaml)
□ Aguardar deploy (3-5 min)
□ Environment > SECRET_KEY (preencher)
□ Shell > createsuperuser
□ Testar admin

FASE 3 - EMAIL (ESTA SEMANA):
□ Criar conta Resend
□ Gerar API Key
□ Adicionar no Render
□ Testar envio
□ Verificar domínio

FASE 4 - PAGAMENTOS (ESTA SEMANA):
□ Criar conta Stripe
□ Test mode: obter keys
□ Criar 3 produtos
□ Configurar webhook
□ Testar com cartão 4242...
□ Adicionar keys no Render

FASE 5 - MARKETING (APÓS DEPLOY):
□ Gravar demo
□ Post LinkedIn
□ Divulgação WhatsApp
□ Email para contatos
```

---

**Status Atual: 80% pronto. Faltam apenas deploys e integrações!**

**Próxima ação:** Configurar Calendly + Formspree + Deploy Netlify (15 min)

_Última atualização: 2025-11-23_
