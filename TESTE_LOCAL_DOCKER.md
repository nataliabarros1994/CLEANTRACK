# 🐳 Teste Local com Docker - CleanTrack

## Pré-requisitos

```bash
# Instalar Docker (se não tiver)
# Ubuntu/Debian:
sudo apt update
sudo apt install docker.io docker-compose -y

# Verificar instalação
docker --version
docker-compose --version
```

---

## Passo 1: Configurar .env Local

```bash
cd /home/nataliabarros1994/Desktop/CleanTrack

# Criar arquivo .env
cat > .env << 'EOF'
# Django
DEBUG=True
SECRET_KEY=rv2o%rw13na2+j3zsciqqu4pfu_fw=jv05c1%0ivauwgi&u7v5
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Docker PostgreSQL)
DATABASE_URL=postgresql://cleantrack:cleantrack@db:5432/cleantrack

# Email (opcional para testes locais)
RESEND_API_KEY=

# Stripe (modo test)
STRIPE_PUBLIC_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

# URLs
SITE_URL=http://localhost:8000
EOF
```

---

## Passo 2: Iniciar com Docker Compose

```bash
# Build e start
docker-compose up -d --build

# Ver logs
docker-compose logs -f web

# Aguardar mensagem:
# "Starting development server at http://0.0.0.0:8000/"
```

---

## Passo 3: Aplicar Migrations

```bash
# Rodar migrations
docker-compose exec web python manage.py migrate

# Criar superuser
docker-compose exec web python manage.py createsuperuser
```

Preencher:
```
Username: admin
Email: natalia@email.com
Password: admin123
Password (again): admin123
```

---

## Passo 4: Acessar Aplicação

```
Admin: http://localhost:8000/admin/
Login: admin / admin123

Dashboard: http://localhost:8000/
API: http://localhost:8000/api/
```

---

## Passo 5: Criar Dados de Teste

### Via Admin (http://localhost:8000/admin/):

**1. Criar Facility:**
```
Facilities > Add Facility
- Name: Hospital de Testes
- Slug: hospital-testes
- Active: ✓
```

**2. Criar Equipment:**
```
Equipment > Add Equipment
- Name: Ultrassom Portátil A
- Serial Number: US-2024-001
- Facility: Hospital de Testes
- Category: Diagnostic
- Cleaning Frequency: 24 horas
- Active: ✓
- Save
```

**3. Gerar QR Code:**
```
Equipment > [Ultrassom] > View on site
Copiar URL do token
```

**4. Registrar Limpeza:**
```
Abrir navegador:
http://localhost:8000/cleaning/public/{TOKEN_COPIADO}/

Preencher:
- Técnico: João Silva
- Produto usado: Álcool 70%
- Upload foto (opcional)
- Submit
```

**5. Ver Dashboard:**
```
http://localhost:8000/dashboard/
```

---

## Passo 6: Testar Fluxo Completo

### 1. Login como Admin
```
http://localhost:8000/admin/
admin / admin123
```

### 2. Adicionar 5 Equipamentos
```
Equipment > Add Equipment (x5)
- Ultrassom A, B, C
- Raio-X 1, 2
```

### 3. Gerar PDF de Etiquetas
```
Equipment > Generate Labels PDF
Download PDF
Imprimir (ou visualizar)
```

### 4. Simular Limpeza via QR
```
Para cada equipamento:
1. Copiar token público
2. Acessar: /cleaning/public/{token}/
3. Preencher form
4. Submit
```

### 5. Ver Métricas
```
Dashboard > Compliance Report
- X equipamentos em conformidade
- Y equipamentos vencidos
- Gráficos de tendência
```

---

## 🔧 Comandos Úteis

### Ver logs:
```bash
docker-compose logs -f web
docker-compose logs -f db
```

### Restart:
```bash
docker-compose restart
```

### Stop:
```bash
docker-compose down
```

### Reset completo (apaga DB):
```bash
docker-compose down -v
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### Entrar no shell Django:
```bash
docker-compose exec web python manage.py shell
```

### Backup do banco:
```bash
docker-compose exec db pg_dump -U cleantrack cleantrack > backup.sql
```

---

## 📊 Testar Integrações

### Stripe (Test Mode):

1. **Obter test keys:**
   - https://dashboard.stripe.com/test/apikeys
   - Copiar pk_test_xxx e sk_test_xxx

2. **Adicionar no .env:**
   ```
   STRIPE_PUBLIC_KEY=pk_test_xxx
   STRIPE_SECRET_KEY=sk_test_xxx
   ```

3. **Restart:**
   ```bash
   docker-compose restart web
   ```

4. **Testar webhook:**
   ```bash
   # Instalar Stripe CLI
   stripe listen --forward-to localhost:8000/billing/webhook/

   # Em outro terminal
   stripe trigger payment_intent.succeeded
   ```

### Resend (Email):

1. **Obter API key:**
   - https://resend.com/api-keys
   - Copiar re_xxx

2. **Adicionar no .env:**
   ```
   RESEND_API_KEY=re_xxx
   ```

3. **Testar envio:**
   ```bash
   docker-compose exec web python manage.py shell

   from django.core.mail import send_mail
   send_mail(
       'Teste CleanTrack',
       'Email funcionando!',
       'onboarding@resend.dev',
       ['natalia@email.com'],
   )
   ```

---

## ✅ Checklist de Testes

### Funcionalidades Core:
- [ ] Login no admin
- [ ] Criar facility
- [ ] Criar equipamento
- [ ] Gerar QR code
- [ ] Acessar via QR (token temporário)
- [ ] Registrar limpeza (autenticado)
- [ ] Registrar limpeza (anônimo via token)
- [ ] Upload de foto
- [ ] Ver dashboard
- [ ] Exportar relatório PDF
- [ ] Gerar etiquetas para impressão

### Integrações:
- [ ] Stripe test payment
- [ ] Stripe webhook
- [ ] Resend email
- [ ] Template rendering

### Multi-tenant:
- [ ] Criar 2 facilities
- [ ] Equipamentos isolados por facility
- [ ] Usuários com acesso limitado

---

## 🐛 Troubleshooting

### Porta 8000 já em uso:
```bash
# Mudar porta no docker-compose.yml
ports:
  - "8001:8000"

# Acessar em localhost:8001
```

### Permission denied no Docker:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Erro de migração:
```bash
# Reset database
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
```

### CSS não carrega:
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

---

## 📸 Screenshots Esperados

Após testes, você deve conseguir:

1. **Admin Panel** - Lista de equipamentos
2. **Dashboard** - Métricas de conformidade
3. **QR Code Form** - Formulário público de limpeza
4. **PDF Labels** - Etiquetas prontas para impressão
5. **Compliance Report** - Relatório exportado

---

## 🚀 Próximo Passo

Após validar localmente:

```bash
# Parar Docker
docker-compose down

# Deploy para produção (Render)
# Ver: DEPLOY_AGORA_3_COMANDOS.md
```

---

**Tempo estimado:** 15-20 minutos
**Custo:** R$ 0 (tudo local)

_Último update: 2025-11-23_
