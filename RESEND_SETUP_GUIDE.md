# 📧 Guia de Configuração Resend - CleanTrack

## O que é Resend?

Resend é um serviço moderno de email transacional para desenvolvedores. Ideal para:
- Enviar emails de confirmação
- Notificações do sistema
- Relatórios automáticos
- Alertas de conformidade

**Plano Gratuito:** 3.000 emails/mês grátis (suficiente para começar)

---

## Passo 1️⃣: Criar Conta

### A. Registro

1. Acesse: [resend.com](https://resend.com)
2. Clique em "Sign Up"
3. Preencha:
   - Email: seu-email@gmail.com
   - Nome: Seu Nome
   - Empresa: CleanTrack
4. Confirme seu email

### B. Confirmar Email

1. Verifique sua caixa de entrada
2. Clique no link de confirmação
3. Faça login no dashboard

---

## Passo 2️⃣: Criar API Key

### A. Gerar Chave

1. No Dashboard Resend, clique em **"API Keys"** (menu lateral)
2. Clique em **"Create API Key"**
3. Preencha:
   - Name: `CleanTrack Production`
   - Permission: `Full Access` (ou `Sending access` apenas)
   - Domains: `All domains` (ou selecione específico depois)
4. Clique em **"Create"**

### B. Copiar e Guardar

```
Você verá uma chave como:
re_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

⚠️ IMPORTANTE: Copie AGORA!
Esta chave será mostrada apenas uma vez.
```

**Guarde em local seguro:**
```bash
# Cole no arquivo .env.production
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Passo 3️⃣: Configurar no Render

### A. Adicionar Environment Variable

1. Acesse: [dashboard.render.com](https://dashboard.render.com)
2. Selecione: `cleantrack-api`
3. Vá em: **Environment** (menu lateral)
4. Clique em **"Add Environment Variable"**
5. Preencha:
   ```
   Key: RESEND_API_KEY
   Value: re_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (cole sua chave)
   ```
6. Clique em **"Save Changes"**
7. Render fará **redeploy automático** (aguarde 2-3 minutos)

### B. Configurar Email de Remetente

```
Key: DEFAULT_FROM_EMAIL
Value: contato@cleantrack.com
```

```
Key: SERVER_EMAIL
Value: noreply@cleantrack.com
```

---

## Passo 4️⃣: Testar Email (Modo Teste)

### A. Usar Email @resend.dev (temporário)

Por enquanto, você pode usar `onboarding@resend.dev` como remetente para testes:

1. No Render > cleantrack-api > **Shell**
2. Execute:

```python
from django.core.mail import send_mail

send_mail(
    subject='Teste CleanTrack',
    message='Email de teste funcionando via Resend!',
    from_email='onboarding@resend.dev',  # Email de teste da Resend
    recipient_list=['seu-email-pessoal@gmail.com'],
    fail_silently=False,
)
```

3. Verifique sua caixa de entrada
4. Você deve receber o email em alguns segundos

### B. Verificar Logs

1. Resend Dashboard > **Emails**
2. Você verá todos os emails enviados
3. Status: `Sent` ✅ ou `Failed` ❌
4. Clique para ver detalhes completos

---

## Passo 5️⃣: Verificar Domínio Personalizado (Produção)

Para usar `contato@cleantrack.com.br` em vez de `@resend.dev`:

### A. Adicionar Domínio

1. Resend Dashboard > **Domains**
2. Clique em **"Add Domain"**
3. Digite: `cleantrack.com.br`
4. Clique em **"Add"**

### B. Configurar DNS

Resend mostrará 3 registros DNS para adicionar:

```
Tipo  | Nome              | Valor
------|-------------------|--------------------------------
TXT   | @                 | resend-verify=xxxxxxxxxxxxx
CNAME | resend._domainkey | resend._domainkey.resend.com
CNAME | resend.bounce     | resend.bounce.resend.com
```

### C. Adicionar no Cloudflare (ou seu provedor DNS)

**Se usar Cloudflare:**

1. Cloudflare Dashboard
2. Selecione: `cleantrack.com.br`
3. Vá em: **DNS** > **Records**
4. Clique em **"Add record"**

**Registro 1 - TXT:**
```
Type: TXT
Name: @
Content: resend-verify=xxxxxxxxxxxxx (copie do Resend)
Proxy: OFF (cinza ☁️)
TTL: Auto
```

**Registro 2 - CNAME:**
```
Type: CNAME
Name: resend._domainkey
Target: resend._domainkey.resend.com
Proxy: OFF
TTL: Auto
```

**Registro 3 - CNAME:**
```
Type: CNAME
Name: resend.bounce
Target: resend.bounce.resend.com
Proxy: OFF
TTL: Auto
```

5. Clique em **"Save"** para cada registro

### D. Verificar Domínio

1. Volte ao Resend Dashboard > Domains
2. Aguarde 1-5 minutos (propagação DNS)
3. Clique em **"Verify"**
4. Status deve mudar para: ✅ **Verified**

---

## Passo 6️⃣: Testar com Domínio Verificado

Agora que o domínio está verificado:

```python
from django.core.mail import send_mail

send_mail(
    subject='CleanTrack - Bem-vindo!',
    message='Seu domínio está configurado corretamente!',
    from_email='contato@cleantrack.com.br',  # Seu domínio verificado
    recipient_list=['seu-email@gmail.com'],
    fail_silently=False,
)
```

---

## Passo 7️⃣: Atualizar Django Settings

### A. Verificar settings.py

Certifique-se que tem estas configurações:

```python
# Email Backend
if not DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.resend.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'resend'
    EMAIL_HOST_PASSWORD = os.getenv('RESEND_API_KEY')

    # From addresses
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'contato@cleantrack.com')
    SERVER_EMAIL = os.getenv('SERVER_EMAIL', 'noreply@cleantrack.com')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### B. Fazer commit e push

```bash
git add cleantrack/settings.py
git commit -m "Configure Resend email backend"
git push origin main
```

Render fará deploy automático.

---

## 📧 Templates de Email Prontos

### A. Email de Boas-Vindas

Crie: `templates/emails/welcome.html`

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; }
    .header { background: #3498db; color: white; padding: 20px; text-align: center; }
    .content { padding: 20px; }
    .button { background: #27ae60; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }
  </style>
</head>
<body>
  <div class="header">
    <h1>🎉 Bem-vindo ao CleanTrack!</h1>
  </div>
  <div class="content">
    <p>Olá {{ facility_name }},</p>
    <p>Sua conta foi criada com sucesso! Você agora faz parte dos clientes piloto do CleanTrack.</p>
    <h3>Próximos passos:</h3>
    <ol>
      <li>Acesse o dashboard: <a href="{{ dashboard_url }}">{{ dashboard_url }}</a></li>
      <li>Configure seus equipamentos</li>
      <li>Baixe e imprima as etiquetas QR Code</li>
    </ol>
    <a href="{{ dashboard_url }}" class="button">Acessar Dashboard</a>
    <p style="margin-top: 30px; color: #666;">
      Precisa de ajuda? Responda este email ou entre em contato:
      <br>📧 contato@cleantrack.com
      <br>📱 (XX) XXXXX-XXXX
    </p>
  </div>
</body>
</html>
```

### B. Enviar Email com Template

```python
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_welcome_email(user, facility):
    subject = 'Bem-vindo ao CleanTrack!'

    # Renderizar template
    html_content = render_to_string('emails/welcome.html', {
        'facility_name': facility.name,
        'dashboard_url': 'https://cleantrack.com/dashboard',
    })

    # Criar email
    email = EmailMultiAlternatives(
        subject=subject,
        body='Bem-vindo ao CleanTrack!',  # Fallback texto puro
        from_email='contato@cleantrack.com',
        to=[user.email],
    )

    # Anexar HTML
    email.attach_alternative(html_content, "text/html")

    # Enviar
    email.send()
```

---

## 📊 Monitoramento e Analytics

### A. Dashboard do Resend

Veja estatísticas em: **Resend Dashboard > Analytics**

- Total de emails enviados
- Taxa de entrega
- Bounces (rejeitados)
- Reclamações de spam

### B. Webhooks (opcional)

Para rastrear eventos (aberto, clicado, etc.):

1. Resend > **Webhooks**
2. Add Webhook
3. URL: `https://cleantrack-api.onrender.com/webhooks/resend/`
4. Eventos:
   - email.sent
   - email.delivered
   - email.bounced
   - email.complained

---

## ✅ Checklist de Configuração

- [ ] Conta Resend criada
- [ ] API Key gerada
- [ ] API Key adicionada no Render
- [ ] Email de teste enviado com sucesso
- [ ] Domínio personalizado adicionado
- [ ] Registros DNS configurados
- [ ] Domínio verificado no Resend
- [ ] Email de produção testado
- [ ] Templates de email criados

---

## 🚨 Troubleshooting

### Problema: "API key is invalid"
```
Solução:
1. Verificar se copiou a chave completa
2. Verificar se não tem espaços extras
3. Gerar nova chave se necessário
4. Atualizar no Render Environment
```

### Problema: "Domain not verified"
```
Solução:
1. Verificar registros DNS no Cloudflare
2. Aguardar propagação (até 24h, geralmente 5 min)
3. Usar ferramenta: https://mxtoolbox.com/SuperTool.aspx
4. Testar: dig resend._domainkey.cleantrack.com.br CNAME
```

### Problema: Email vai para spam
```
Solução:
1. Completar verificação SPF/DKIM/DMARC
2. Usar from_email verificado
3. Evitar palavras spam no subject
4. Incluir link de unsubscribe
5. Manter baixa taxa de bounce
```

### Problema: "Rate limit exceeded"
```
Solução:
1. Plano Free: 3.000 emails/mês
2. Upgrade para Pro: $20/mês (50k emails)
3. Implementar queue para envios em lote
```

---

## 💰 Custos

### Free Tier:
```
3.000 emails/mês: GRÁTIS
Ideal para: 0-100 clientes
```

### Pro Plan:
```
$20/mês: 50.000 emails
Ideal para: 100-500 clientes
```

### Enterprise:
```
Personalizado para volumes maiores
```

---

## 🎯 Próximos Passos

1. **Criar mais templates:**
   - Email de confirmação de limpeza
   - Relatório mensal automático
   - Alerta de equipamento pendente
   - Lembrete de auditoria

2. **Implementar automações:**
   - Email quando novo equipamento é registrado
   - Notificação quando limpeza vence
   - Resumo semanal para gestores

3. **Personalização:**
   - Logo do CleanTrack no header
   - Assinatura de email profissional
   - Footer com redes sociais

---

**Pronto! Seu sistema de email está configurado! 📧**

URL Resend: https://resend.com/emails
Documentação: https://resend.com/docs

_Última atualização: 2025-11-23_
