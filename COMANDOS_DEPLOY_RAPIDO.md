# ⚡ Comandos de Deploy Rápido - CleanTrack

## 🎯 Escolha sua Opção:

---

## OPÇÃO 1️⃣: Landing Page (15 minutos)

### Passo 1: Configurar Calendly (5 min)

```
1. Abrir navegador: https://calendly.com/signup
2. Criar conta (email + senha)
3. Criar evento:
   - Nome: CleanTrack - Onboarding Piloto
   - Duração: 30 minutos
4. Copiar link (exemplo):
   https://calendly.com/seu-usuario/cleantrack-onboarding
```

### Passo 2: Configurar Formspree (3 min)

```
1. Abrir: https://formspree.io/register
2. Criar conta
3. Criar novo form: "CleanTrack Leads"
4. Copiar o ID (exemplo): xwpkabcd
   URL será: https://formspree.io/f/xwpkabcd
```

### Passo 3: Editar index.html (2 min)

Abra o arquivo: `/home/nataliabarros1994/Desktop/CleanTrack/index.html`

**Linha 170 - Calendly:**
```html
ANTES: data-url="https://calendly.com/seu-usuario/cleantrack-onboarding"
DEPOIS: data-url="https://calendly.com/SEU-LINK-REAL/cleantrack-onboarding"
```

**Linha 264 - Formspree:**
```html
ANTES: action="https://formspree.io/f/seu-form-id"
DEPOIS: action="https://formspree.io/f/SEU-ID-REAL"
```

**Linhas 326-334 - Contatos:**
```html
ANTES: contato@cleantrack.com.br
DEPOIS: seu-email-real@gmail.com

ANTES: (XX) XXXXX-XXXX
DEPOIS: (11) 98765-4321  (seu WhatsApp real)
```

Salve o arquivo (Ctrl+S)

### Passo 4: Deploy no Netlify (2 min)

```
1. Abrir: https://app.netlify.com/drop
2. Fazer login (ou criar conta com GitHub/Google)
3. Arrastar a pasta CleanTrack para a página
4. Aguardar upload (10-30 segundos)
5. Copiar URL gerada (exemplo):
   https://random-name-123.netlify.app
```

### Passo 5: Personalizar Nome (opcional, 1 min)

```
1. No Netlify: Site settings
2. Change site name
3. Escolher: cleantrack-brasil
4. Nova URL: https://cleantrack-brasil.netlify.app
```

### ✅ Testar:

```
1. Abrir: https://cleantrack-brasil.netlify.app
2. Testar calendário Calendly (deve aparecer)
3. Preencher formulário de teste
4. Verificar email do Formspree
```

**✅ PRONTO! Landing page capturando leads!**

---

## OPÇÃO 2️⃣: Backend Deploy (12 minutos)

### Passo 1: Criar Repositório GitHub (2 min)

```
1. Abrir: https://github.com/new
2. Preencher:
   - Repository name: cleantrack-backend
   - Description: CleanTrack - Sistema de Conformidade Médica
   - Visibility: ⚫ Private
   - NÃO marcar "Initialize with README"
3. Clicar: Create repository
4. Copiar a URL (exemplo):
   https://github.com/seu-usuario/cleantrack-backend.git
```

### Passo 2: Push para GitHub (1 min)

**Abra o terminal e execute:**

```bash
cd /home/nataliabarros1994/Desktop/CleanTrack

# Adicionar remote (SUBSTITUA SEU-USUARIO!)
git remote add origin https://github.com/SEU-USUARIO/cleantrack-backend.git

# Verificar
git remote -v

# Push
git push -u origin main
```

Se pedir senha, use um **Personal Access Token**:
```
Username: seu-usuario-github
Password: [cole o token, não a senha do GitHub]
```

### Passo 3: Deploy no Render com Blueprint (5 min)

```
1. Abrir: https://dashboard.render.com
2. Fazer login (ou criar conta com GitHub)
3. Clicar: New + (canto superior direito)
4. Selecionar: Blueprint
5. Conectar ao GitHub:
   - Authorize Render
   - Select Repository: cleantrack-backend
6. Render detectará render.yaml automaticamente
7. Clicar: Apply
8. Aguardar criação:
   - PostgreSQL database (1-2 min)
   - Web service (3-5 min)
9. Acompanhar logs em tempo real
```

### Passo 4: Configurar SECRET_KEY (2 min)

```
1. Render Dashboard > cleantrack-api
2. Environment (menu lateral)
3. Procurar: SECRET_KEY
4. Se vazio, clicar em Edit
5. Colar:
   rv2o%rw13na2+j3zsciqqu4pfu_fw=jv05c1%0ivauwgi&u7v5
6. Save Changes
7. Aguardar redeploy (1-2 min)
```

### Passo 5: Criar Superuser (2 min)

```
1. Render > cleantrack-api
2. Clicar em Shell (ícone de terminal no topo)
3. Aguardar shell abrir (10-20 segundos)
4. Executar:
   python manage.py createsuperuser

5. Preencher:
   Username: admin
   Email: seu-email@gmail.com
   Password: (senha forte)
   Password (again): (repetir senha)
```

### ✅ Testar:

```
1. Abrir: https://cleantrack-api.onrender.com/admin/
2. Login: admin
3. Senha: (a que você criou)
4. Deve ver o Django Admin Panel! 🎉
```

**✅ PRONTO! Backend no ar!**

---

## OPÇÃO 3️⃣: AMBOS - MVP Completo (30 minutos)

### Ordem Recomendada:

**1. Backend primeiro (12 min)** ← Pode rodar enquanto você configura a landing
```
- Passo 1: GitHub (2 min)
- Passo 2: Push (1 min)
- Passo 3: Render Blueprint (5 min) ← AGUARDAR aqui
- Enquanto aguarda deploy → Fazer landing page
- Passo 4: SECRET_KEY (2 min)
- Passo 5: Superuser (2 min)
```

**2. Landing page durante deploy (15 min)** ← Fazer enquanto Render faz build
```
- Passo 1: Calendly (5 min)
- Passo 2: Formspree (3 min)
- Passo 3: Editar HTML (2 min)
- Passo 4: Netlify Deploy (2 min)
- Passo 5: Testar (3 min)
```

**3. Finalizar backend (4 min)**
```
- Configurar SECRET_KEY
- Criar superuser
- Testar admin
```

**✅ RESULTADO: MVP completo em ~27 minutos!**

---

## 🔑 Informações Importantes

### SECRET_KEY (já gerada):
```
rv2o%rw13na2+j3zsciqqu4pfu_fw=jv05c1%0ivauwgi&u7v5
```

### URLs Esperadas:

**Landing Page:**
```
Netlify: https://cleantrack-brasil.netlify.app
(personalizar depois para domínio próprio)
```

**Backend:**
```
API: https://cleantrack-api.onrender.com
Admin: https://cleantrack-api.onrender.com/admin/
```

### Contas Necessárias:

```
✓ GitHub (já tem?)
✓ Netlify (criar com GitHub)
✓ Render (criar com GitHub)
✓ Calendly (criar com email)
✓ Formspree (criar com email)
```

---

## ⚠️ Troubleshooting Rápido

### Git push falha com "Permission denied":
```bash
# Usar HTTPS em vez de SSH
git remote set-url origin https://github.com/SEU-USUARIO/cleantrack-backend.git
git push -u origin main
```

### Render build falha:
```
1. Verificar logs: Render > Logs
2. Checar requirements.txt existe
3. Fazer manual rebuild
```

### Calendly não aparece na landing:
```
1. Verificar link correto na linha 170
2. Aguardar 2-3 segundos (widget carrega)
3. Limpar cache (Ctrl+Shift+R)
```

### Admin sem CSS:
```
1. Aguardar deploy completo
2. Verificar Build Command inclui collectstatic
3. Fazer redeploy
```

---

## 📋 Checklist Rápido

### Landing Page:
```
□ Conta Calendly criada
□ Link Calendly copiado
□ Editado index.html linha 170
□ Conta Formspree criada
□ ID Formspree copiado
□ Editado index.html linha 264
□ Email/WhatsApp atualizados (linhas 326-334)
□ Deploy no Netlify feito
□ Formulário testado
□ Calendário testado
□ URL copiada e salva
```

### Backend:
```
□ Repositório GitHub criado
□ Git remote adicionado
□ Push feito com sucesso
□ Conta Render criada
□ Blueprint aplicado
□ Deploy concluído (status: Live)
□ SECRET_KEY configurada
□ Superuser criado
□ Admin acessível
□ Login funcionando
□ URL copiada e salva
```

---

## 🎯 Próximos Passos (Depois do Deploy)

### Esta Semana:

**1. Resend (Email) - 20 min:**
```bash
# Ver guia: RESEND_SETUP_GUIDE.md
1. Criar conta: resend.com
2. Gerar API key
3. Adicionar no Render Environment
4. Testar envio
```

**2. Stripe Test Mode - 30 min:**
```bash
# Ver guia: STRIPE_SETUP_COMPLETE.md
1. Criar conta: stripe.com
2. Obter test keys
3. Criar 3 produtos
4. Configurar webhook
5. Testar com cartão 4242...
```

**3. Começar Marketing - 1 hora:**
```bash
1. Gravar demo (script: SCRIPT_DEMO_VIDEO_3MIN.md)
2. Post no LinkedIn
3. Compartilhar em grupos
4. Email para contatos
```

---

## 💡 Dicas Pro

### Terminal sempre aberto:
```bash
# Manter terminal na pasta do projeto
cd /home/nataliabarros1994/Desktop/CleanTrack
```

### Verificar status:
```bash
# Git
git status
git log --oneline -5

# Verificar se .env está ignorado
git status | grep .env  # Não deve aparecer!
```

### Backup local:
```bash
# Antes de mudanças grandes
cp -r /home/nataliabarros1994/Desktop/CleanTrack /home/nataliabarros1994/Desktop/CleanTrack_backup
```

---

## 📞 Links Úteis

**Deploy:**
- Netlify Drop: https://app.netlify.com/drop
- Render Dashboard: https://dashboard.render.com
- GitHub New Repo: https://github.com/new

**Integrações:**
- Calendly: https://calendly.com
- Formspree: https://formspree.io
- Resend: https://resend.com
- Stripe: https://dashboard.stripe.com

**Guias Completos:**
- Landing: `LANDING_PAGE_SETUP.md`
- Render: `DEPLOY_RENDER_PASSO_A_PASSO.md`
- Email: `RESEND_SETUP_GUIDE.md`
- Pagamentos: `STRIPE_SETUP_COMPLETE.md`
- Geral: `PRODUCTION_SETUP_GUIDE.md`

---

## ⏱️ Tempo Total Estimado

```
Landing Page:        15 min
Backend Deploy:      12 min
Testes:              3 min
──────────────────────────
TOTAL MVP:           30 min

+ Resend:            20 min
+ Stripe:            30 min
──────────────────────────
TOTAL COMPLETO:      80 min (~1h20min)
```

---

**Boa sorte! Você está a 30 minutos de ter um MVP no ar! 🚀**

_Última atualização: 2025-11-23_
