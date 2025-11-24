# 🚀 Guia de Deploy em Produção - CleanTrack

Este guia detalha o processo completo para colocar o CleanTrack no ar em produção.

---

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Landing Page (Frontend)](#landing-page-frontend)
3. [Backend Django (API)](#backend-django-api)
4. [Banco de Dados](#banco-de-dados)
5. [Configurações de Email](#configurações-de-email)
6. [Stripe (Pagamentos)](#stripe-pagamentos)
7. [Domínio e DNS](#domínio-e-dns)
8. [Monitoramento](#monitoramento)

---

## 1️⃣ Pré-requisitos

### Criar Contas (todas gratuitas para começar):

- [ ] **Netlify** - [netlify.com](https://netlify.com) (Landing Page)
- [ ] **Render** - [render.com](https://render.com) (Backend Django)
- [ ] **Resend** - [resend.com](https://resend.com) (Email transacional)
- [ ] **Stripe** - [stripe.com](https://stripe.com) (Pagamentos)
- [ ] **Calendly** - [calendly.com](https://calendly.com) (Agendamentos)
- [ ] **Formspree** - [formspree.io](https://formspree.io) (Formulários)

### Opcional (mas recomendado):
- [ ] **Sentry** - [sentry.io](https://sentry.io) (Monitoramento de erros)
- [ ] **Cloudflare** - [cloudflare.com](https://cloudflare.com) (CDN + DNS grátis)

---

## 2️⃣ Landing Page (Frontend)

### A. Configurar Integrações

**1. Calendly:**
```bash
# 1. Acesse calendly.com
# 2. Crie evento: "CleanTrack - Onboarding Piloto" (30 min)
# 3. Copie o link: https://calendly.com/seu-usuario/cleantrack-onboarding
```

**Editar index.html (linha 170):**
```html
data-url="https://calendly.com/seu-usuario/cleantrack-onboarding"
```

**2. Formspree:**
```bash
# 1. Acesse formspree.io
# 2. Crie formulário: "CleanTrack Leads"
# 3. Copie o ID: xwpkabcd
```

**Editar index.html (linha 264):**
```html
action="https://formspree.io/f/xwpkabcd"
```

**3. Atualizar Contatos (linhas 326-334):**
```html
<!-- Substitua por seus dados reais -->
<i class="bi bi-envelope"></i> contato@cleantrack.com.br<br>
<i class="bi bi-whatsapp"></i> (11) 98765-4321
```

### B. Deploy no Netlify

**Opção 1: Drag & Drop (Mais Rápido)**
```bash
# 1. Acesse: app.netlify.com/drop
# 2. Arraste a pasta CleanTrack
# 3. Aguarde deploy (10-30 segundos)
# 4. Copie a URL: https://random-name.netlify.app
# 5. Personalize: Site Settings > Change site name > cleantrack-brasil
```

**Opção 2: Git (Recomendado para updates)**
```bash
# 1. Criar repositório
cd /home/nataliabarros1994/Desktop/CleanTrack
git init
git add index.html netlify.toml
git commit -m "Landing page CleanTrack"

# 2. Subir para GitHub
# Crie repo em github.com/new
git remote add origin https://github.com/seu-usuario/cleantrack-landing.git
git push -u origin main

# 3. No Netlify: New site > Import from Git > GitHub
# Deploy automático a cada push!
```

**C. Configurar Domínio Personalizado (Opcional)**
```bash
# 1. No Netlify: Domain Settings > Add custom domain
# 2. Digite: cleantrack.com.br
# 3. Configure DNS (veja seção "Domínio e DNS" abaixo)
```

---

## 3️⃣ Backend Django (API)

### A. Preparar Código

**1. Gerar SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Exemplo de output:
# django-insecure-x7v2k@m9$p8q3w#e4r5t6y7u8i9o0p1a2s3d4f5g6h7j8k9l0
```

**2. Atualizar .env.production:**
```bash
# Cole a SECRET_KEY gerada acima
SECRET_KEY=django-insecure-x7v2k@m9$p8q3w#e4r5t6y7u8i9o0p1a2s3d4f5g6h7j8k9l0
```

**3. Criar requirements.txt (se não existir):**
```bash
cd /home/nataliabarros1994/Desktop/CleanTrack
pip freeze > requirements.txt
```

### B. Deploy no Render

**1. Preparar Repositório:**
```bash
# Certifique-se que .env.production está no .gitignore
echo ".env.production" >> .gitignore
echo ".env" >> .gitignore

# Commit
git add .
git commit -m "Backend pronto para produção"
git push
```

**2. Criar Web Service no Render:**
```
1. Acesse: dashboard.render.com
2. New > Web Service
3. Conecte ao GitHub
4. Selecione repositório: cleantrack
5. Configure:
   - Name: cleantrack-api
   - Environment: Python 3
   - Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   - Start Command: gunicorn cleantrack.wsgi:application
   - Instance Type: Free (para começar)
```

**3. Configurar Environment Variables:**
```
No Render > cleantrack-api > Environment:

DEBUG=False
SECRET_KEY=cole_a_secret_key_gerada
ALLOWED_HOSTS=cleantrack-api.onrender.com
DATABASE_URL=postgresql://... (Render fornece automaticamente)
RESEND_API_KEY=re_xxxx (configure abaixo)
STRIPE_SECRET_KEY=sk_live_xxxx (configure abaixo)
STRIPE_PUBLIC_KEY=pk_live_xxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxx
SITE_URL=https://cleantrack-api.onrender.com
```

**4. Aguardar Deploy:**
```
- Render fará build automático (2-5 minutos)
- Acesse: https://cleantrack-api.onrender.com
- Teste: https://cleantrack-api.onrender.com/admin
```

---

## 4️⃣ Banco de Dados

### PostgreSQL no Render (Recomendado)

**1. Criar Database:**
```
1. Render Dashboard > New > PostgreSQL
2. Name: cleantrack-db
3. Database: cleantrack_production
4. User: cleantrack_user
5. Region: Oregon (mais barato)
6. Instance Type: Free
```

**2. Copiar Connection String:**
```
Formato:
postgresql://cleantrack_user:senha@host.com:5432/cleantrack_production

Cole em:
Render > cleantrack-api > Environment > DATABASE_URL
```

**3. Rodar Migrações:**
```bash
# No Render > cleantrack-api > Shell
python manage.py migrate
python manage.py createsuperuser
```

### Alternativa: Supabase (PostgreSQL Grátis + Storage)

```
1. Acesse supabase.com
2. New Project > CleanTrack
3. Copie connection string
4. Cole em DATABASE_URL
```

---

## 5️⃣ Configurações de Email

### Resend (Recomendado - 3.000 emails/mês grátis)

**1. Criar Conta e API Key:**
```
1. Acesse: resend.com
2. API Keys > Create API Key
3. Nome: CleanTrack Production
4. Copie: re_xxxxxxxxxxxxxxxxxxxxxxxxx
```

**2. Verificar Domínio:**
```
1. Resend > Domains > Add Domain
2. Digite: cleantrack.com.br
3. Adicione registros DNS:

   Tipo  | Nome        | Valor
   ------|-------------|---------------------------
   TXT   | _resend     | [valor fornecido]
   CNAME | resend._    | [valor fornecido]
   CNAME | resend._dm  | [valor fornecido]
```

**3. Configurar no Render:**
```
Environment Variables:
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxxxxxx
DEFAULT_FROM_EMAIL=contato@cleantrack.com.br
SERVER_EMAIL=noreply@cleantrack.com.br
```

**4. Testar Email:**
```bash
# No Render Shell ou localmente
python manage.py shell

from django.core.mail import send_mail
send_mail(
    'Teste CleanTrack',
    'Email funcionando!',
    'contato@cleantrack.com.br',
    ['seu-email@gmail.com'],
)
```

### Alternativa: SendGrid / Mailgun
```
# SendGrid: 100 emails/dia grátis
# Mailgun: 5.000 emails/mês grátis
```

---

## 6️⃣ Stripe (Pagamentos)

### A. Ativar Conta Live

**1. Completar Cadastro:**
```
1. Acesse: dashboard.stripe.com
2. Complete informações da empresa:
   - Nome: CleanTrack Medical Systems
   - CNPJ
   - Endereço
   - Conta bancária para recebimentos
```

**2. Obter API Keys (Live):**
```
1. Stripe Dashboard > Developers > API Keys
2. Ative "View live mode"
3. Copie:
   - Publishable key: pk_live_xxxxxx
   - Secret key: sk_live_xxxxxx (Revelar)
```

### B. Configurar Produtos

**1. Criar Produtos:**
```
Stripe Dashboard > Products > Add Product

Produto 1:
- Nome: CleanTrack Starter
- Preço: R$ 200/mês
- Descrição: Até 50 equipamentos

Produto 2:
- Nome: CleanTrack Professional
- Preço: R$ 500/mês
- Descrição: Até 200 equipamentos

Produto 3:
- Nome: CleanTrack Enterprise
- Preço: R$ 1.200/mês
- Descrição: Equipamentos ilimitados
```

**2. Copiar Price IDs:**
```
Cada produto tem um price_id (price_xxxxx)
Guarde para usar na aplicação
```

### C. Configurar Webhooks

**1. Criar Webhook Endpoint:**
```
1. Stripe > Developers > Webhooks
2. Add endpoint
3. URL: https://cleantrack-api.onrender.com/billing/webhook/
4. Eventos a escutar:
   - customer.subscription.created
   - customer.subscription.updated
   - customer.subscription.deleted
   - invoice.payment_succeeded
   - invoice.payment_failed
```

**2. Copiar Webhook Secret:**
```
whsec_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Cole em:
Render > Environment > STRIPE_WEBHOOK_SECRET
```

**3. Testar Webhook:**
```bash
# No Render Shell
python test_stripe_connection.py
```

---

## 7️⃣ Domínio e DNS

### A. Registrar Domínio

**Opções:**
- **Registro.br** (R$ 40/ano) - .com.br
- **Namecheap** ($10/ano) - .com
- **Cloudflare Registrar** (preço de custo)

### B. Configurar DNS no Cloudflare (Recomendado)

**1. Adicionar Site:**
```
1. Cloudflare > Add a Site
2. Digite: cleantrack.com.br
3. Plano Free
```

**2. Configurar Nameservers:**
```
No registro.br (ou outro registrador):
- Nameserver 1: ada.ns.cloudflare.com
- Nameserver 2: hans.ns.cloudflare.com
```

**3. Adicionar DNS Records:**
```
Tipo  | Nome  | Conteúdo                              | Proxy
------|-------|---------------------------------------|-------
A     | @     | [IP do Netlify]                      | ✅ On
CNAME | www   | cleantrack-brasil.netlify.app        | ✅ On
CNAME | api   | cleantrack-api.onrender.com          | ⬜ Off
TXT   | @     | [Verificação Resend]                 | -
```

**4. SSL/TLS:**
```
Cloudflare > SSL/TLS > Full (strict)
```

### C. Atualizar Configurações

**Netlify:**
```
Domain Settings > Custom domain > cleantrack.com.br
Enable HTTPS (automático via Let's Encrypt)
```

**Render:**
```
Settings > Custom Domain > api.cleantrack.com.br
```

---

## 8️⃣ Monitoramento

### A. Sentry (Rastreamento de Erros)

**1. Criar Projeto:**
```
1. Acesse sentry.io
2. Create Project > Django
3. Copie DSN: https://xxxxx@o123.ingest.sentry.io/123
```

**2. Instalar:**
```bash
pip install sentry-sdk
```

**3. Configurar (settings.py):**
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    environment='production',
    traces_sample_rate=1.0,
)
```

**4. Adicionar ao Render:**
```
Environment > SENTRY_DSN=https://xxxxx@...
```

### B. Google Analytics (Landing Page)

**1. Criar Propriedade:**
```
analytics.google.com > Admin > Create Property
- Nome: CleanTrack
- Time Zone: São Paulo
```

**2. Obter Measurement ID:**
```
G-XXXXXXXXXX
```

**3. Adicionar ao index.html (antes do </head>):**
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### C. Uptime Monitoring

**UptimeRobot (Grátis):**
```
1. uptimerobot.com
2. Add New Monitor
3. Type: HTTPS
4. URL: https://cleantrack.com.br
5. Interval: 5 minutos
6. Alertas: seu-email@gmail.com
```

---

## ✅ Checklist Final de Produção

### Landing Page:
- [ ] Calendly configurado
- [ ] Formspree configurado
- [ ] Contatos atualizados
- [ ] Google Analytics instalado
- [ ] Testado em mobile e desktop
- [ ] Deploy no Netlify concluído
- [ ] Domínio personalizado configurado

### Backend:
- [ ] SECRET_KEY gerada e configurada
- [ ] PostgreSQL configurado
- [ ] Migrações rodadas
- [ ] Superuser criado
- [ ] Resend configurado e testado
- [ ] Stripe Live Mode ativado
- [ ] Webhooks configurados
- [ ] Deploy no Render concluído
- [ ] API acessível via domínio

### Segurança:
- [ ] DEBUG=False
- [ ] HTTPS habilitado
- [ ] HSTS configurado
- [ ] .env.production no .gitignore
- [ ] Senhas fortes configuradas
- [ ] Cors configurado corretamente

### Monitoramento:
- [ ] Sentry configurado
- [ ] UptimeRobot ativo
- [ ] Google Analytics instalado
- [ ] Logs sendo monitorados

---

## 🚨 Comandos de Emergência

### Rollback Rápido (Render):
```
Dashboard > Deploys > [versão anterior] > Redeploy
```

### Ver Logs em Tempo Real:
```
Render > cleantrack-api > Logs
```

### Acessar Shell Produção:
```
Render > cleantrack-api > Shell
python manage.py shell
```

### Backup Manual do Banco:
```
render db-backup cleantrack-db
```

---

## 📊 Custos Estimados

### Fase Piloto (0-10 clientes):
```
Landing Page (Netlify):          R$ 0
Backend (Render Free):           R$ 0
Database (Render Free):          R$ 0
Email (Resend 3k/mês):          R$ 0
Stripe (2.99% + R$ 0,39):       Variável
Domínio (.com.br):              R$ 40/ano
---------------------------------------------
Total mensal:                    ~R$ 0
```

### Escalando (10-100 clientes):
```
Netlify Pro:                     R$ 90/mês
Render Starter (DB):             R$ 35/mês
Render Standard (API):           R$ 140/mês
Resend Pro:                      R$ 100/mês
---------------------------------------------
Total mensal:                    ~R$ 365/mês
```

---

## 🆘 Troubleshooting

### Problema: "Bad Gateway" no Render
```
1. Verificar logs: Render > Logs
2. Confirmar gunicorn instalado: pip install gunicorn
3. Testar localmente: gunicorn cleantrack.wsgi:application
```

### Problema: Email não envia
```
1. Verificar RESEND_API_KEY no Environment
2. Confirmar domínio verificado no Resend
3. Testar: python manage.py shell > send_mail()
4. Ver logs do Resend Dashboard
```

### Problema: Stripe webhook falha
```
1. Verificar URL: https://api.cleantrack.com.br/billing/webhook/
2. Confirmar STRIPE_WEBHOOK_SECRET correto
3. Testar com Stripe CLI: stripe listen --forward-to localhost:8000/billing/webhook/
```

### Problema: CSS não carrega
```
1. Rodar: python manage.py collectstatic
2. Verificar STATIC_ROOT em settings.py
3. Considerar usar S3 para static files
```

---

## 📞 Suporte

**Documentação Oficial:**
- Render: [render.com/docs](https://render.com/docs)
- Netlify: [docs.netlify.com](https://docs.netlify.com)
- Stripe: [stripe.com/docs](https://stripe.com/docs)
- Resend: [resend.com/docs](https://resend.com/docs)

**Comunidades:**
- Django Brasil: [t.me/djangobrasil](https://t.me/djangobrasil)
- Stack Overflow: [pt.stackoverflow.com](https://pt.stackoverflow.com)

---

**Boa sorte com o lançamento! 🚀**

_Última atualização: 2025-11-23_
