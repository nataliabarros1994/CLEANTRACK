# DEPLOY DO CLEANTRACK NO RENDER (PASSO A PASSO COMPLETO)

## ✅ 1. Entre no painel

Acesse:

https://dashboard.render.com/

Clique em **New +** → **Web Service**

---

## ✅ 2. Conecte seu GitHub

Se ainda não conectou:
**Connect account** → autorize → escolha o repositório:
**nataliabarros1994/CLEANTRACK**

---

## ✅ 3. Configurações iniciais do Web Service

**➤ Name:**
```
cleantrack
```

**➤ Environment:**
```
Docker
```

**➤ Region:**
```
Use Oregon (US West) — melhor latência.
```

**➤ Branch:**
```
main
```

---

## ✅ 4. Render vai identificar o Docker automaticamente

Como o projeto tem **Dockerfile + docker-compose.yml**, o Render detecta tudo automaticamente.

Mas é necessário configurar corretamente as variáveis de ambiente.

---

## ⚠️ 5. Adicionar as variáveis de ambiente

No serviço → **Environment** → **Add Environment Variable**

**Adicionar:**

```
DJANGO_SETTINGS_MODULE=cleantrack.settings_production_ready
PYTHONUNBUFFERED=1
PORT=10000
SECRET_KEY=<generate one>
```

Se usar PostgreSQL do Render, adicionar:

```
DATABASE_URL=<Render PostgreSQL URL>
```

---

## 🔥 6. Ativar Web Service com Docker

Render usará automaticamente o **Dockerfile**.

Para garantir o comando de start:

```bash
gunicorn cleantrack.wsgi:application --bind 0.0.0.0:$PORT
```

---

## 🟢 7. Criar banco de dados PostgreSQL no Render

Volte ao Dashboard:

**New +** → **PostgreSQL**

**Configurações:**

```
Name: cleantrack-db
Region: Oregon
```

Copie a URL gerada:

```
DATABASE_URL=postgres://<...>
```

E cole no Web Service do CleanTrack.

---

## 🗄️ 8. Rodar migrations

No Render → Web Service → **Shell**:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

Se Shell não estiver ativo:

**Settings** → **Enable Shell**

---

## 🚀 9. Deploy

Clique:

**Deploy Latest Commit**

Render irá:

✔ instalar dependências
✔ rodar collectstatic
✔ expor a porta
✔ iniciar Gunicorn

---

## 🟦 10. Teste no navegador

Quando o serviço estiver verde:

Acesse a URL pública:

```
https://cleantrack.onrender.com
```

---

## 📋 VARIÁVEIS DE AMBIENTE COMPLETAS

Veja o arquivo **RENDER_ENV_VARS.txt** para a lista completa de todas as variáveis necessárias.

**Variáveis obrigatórias:**
- DJANGO_SETTINGS_MODULE=cleantrack.settings_production_ready
- PYTHONUNBUFFERED=1
- PORT=10000
- SECRET_KEY=<generate>
- DATABASE_URL=<auto from PostgreSQL>
- RESEND_API_KEY=***REMOVED***
- STRIPE_TEST_PUBLIC_KEY=***REMOVED***
- STRIPE_TEST_SECRET_KEY=***REMOVED***
- STRIPE_LIVE_MODE=False

---

## 🎯 VERIFICAÇÃO FINAL

Após o deploy bem-sucedido:

- [ ] Site carrega: https://cleantrack.onrender.com
- [ ] Admin acessível: https://cleantrack.onrender.com/admin/
- [ ] Login funciona
- [ ] Static files carregam (CSS/JS)
- [ ] Database conectado

---

## 🔧 TROUBLESHOOTING

### Erro: "Application failed to respond"
**Solução:** Verifique se PORT=10000 está configurado nas variáveis de ambiente

### Erro: "No module named 'cleantrack'"
**Solução:** Verifique se DJANGO_SETTINGS_MODULE está correto

### Erro: "ALLOWED_HOSTS"
**Solução:** settings_production_ready.py já inclui .onrender.com automaticamente

### Static files não carregam
**Solução:** 
```bash
# No Shell do Render:
python manage.py collectstatic --noinput
```

---

## ✅ SUCESSO!

Seu CleanTrack está rodando em produção no Render! 🎉

**URL:** https://cleantrack.onrender.com

**Próximos passos:**
1. Configure custom domain (opcional)
2. Configure Stripe webhooks
3. Teste todas as funcionalidades
4. Faça backup do banco de dados
5. Configure monitoramento

---

*Documentação atualizada: Janeiro 2025*
