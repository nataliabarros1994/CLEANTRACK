# CleanTrack - Guia de Acesso Rápido 🚀

## 🌐 Links para Acessar o Projeto

### Após Iniciar o Docker

Uma vez que você execute `docker-compose up`, o projeto estará disponível em:

#### Aplicação Web Principal
```
🌍 http://localhost:8000
```
- Landing page
- Dashboard (após login)
- Todas as funcionalidades

#### Painel Administrativo
```
🔐 http://localhost:8000/admin
```
- Gerenciar todos os dados
- Visualizar modelos
- CRUD completo

#### Endpoints da API

**Webhooks Stripe:**
```
📨 http://localhost:8000/billing/webhooks/stripe/
```

**Autenticação (Django AllAuth):**
```
👤 http://localhost:8000/accounts/login/
👤 http://localhost:8000/accounts/signup/
👤 http://localhost:8000/accounts/logout/
```

**Stripe (dj-stripe):**
```
💳 http://localhost:8000/stripe/
```

---

## 🚀 Como Iniciar o Projeto

### Método 1: Docker (Mais Rápido)

```bash
# 1. Navegue até a pasta do projeto
cd /home/nataliabarros1994/Desktop/CleanTrack

# 2. Copie o arquivo de configuração
cp .env.example .env

# 3. (Opcional) Edite as variáveis de ambiente
nano .env

# 4. Inicie todos os serviços
docker-compose up --build

# Aguarde até ver:
# ✓ web_1    | Starting development server at http://0.0.0.0:8000/
```

**Em outro terminal, execute:**

```bash
# 5. Execute as migrações do banco de dados
docker-compose exec web python manage.py migrate

# 6. Crie um superusuário
docker-compose exec web python manage.py createsuperuser
# Digite: email, password, password (confirmation)

# 7. Crie dados de demonstração (opcional)
docker-compose exec web python manage.py create_demo_data
```

**Agora acesse:**
- 🌍 **Aplicação**: http://localhost:8000
- 🔐 **Admin**: http://localhost:8000/admin

---

### Método 2: Desenvolvimento Local (Sem Docker)

```bash
# 1. Navegue até a pasta do projeto
cd /home/nataliabarros1994/Desktop/CleanTrack

# 2. Execute o script de setup
chmod +x setup.sh
./setup.sh

# 3. Ative o ambiente virtual
source venv/bin/activate

# 4. Instale dependências adicionais
pip install -r requirements.txt

# 5. Configure o banco de dados
# Certifique-se de que PostgreSQL está rodando
# Ou use SQLite para desenvolvimento rápido

# 6. Execute migrações
python manage.py migrate

# 7. Crie superusuário
python manage.py createsuperuser

# 8. Crie dados de demonstração
python manage.py create_demo_data

# 9. Inicie o servidor
python manage.py runserver
```

**Em terminais separados:**

```bash
# Terminal 2: Celery Worker
source venv/bin/activate
celery -A cleantrack worker -l info

# Terminal 3: Celery Beat
source venv/bin/activate
celery -A cleantrack beat -l info
```

**Agora acesse:**
- 🌍 **Aplicação**: http://localhost:8000
- 🔐 **Admin**: http://localhost:8000/admin

---

## 👤 Credenciais de Acesso

### Superusuário (Criado por Você)
```
Email: [o que você definir]
Senha: [o que você definir]
```

### Usuários de Demonstração (se executou create_demo_data)

**Administrador:**
```
Email: demo.admin@cleantrack.app
Senha: demo123
```

**Técnico:**
```
Email: demo.technician@cleantrack.app
Senha: demo123
```

---

## 🎯 Primeiros Passos no Sistema

### 1. Acesse o Admin
```
http://localhost:8000/admin
```
- Faça login com superusuário ou usuário demo
- Explore os modelos: Accounts, Equipment, Compliance

### 2. Veja os Dados de Demonstração
Se você executou `create_demo_data`, verá:
- ✅ **1 Conta**: Demo Hospital
- ✅ **2 Localizações**: Main Building, ICU Wing
- ✅ **4 Equipamentos**: Ultrasound, Ventilators, X-Ray
- ✅ **2 Logs de Limpeza**: Registros recentes
- ✅ **3 Alertas**: Overdue, Due Soon, Never Cleaned

### 3. Explore as Funcionalidades

**No Admin, você pode:**
- ➕ Adicionar novos equipamentos
- 📝 Registrar limpezas
- ⚠️ Ver alertas de conformidade
- 📊 Gerar relatórios

---

## 🔧 Verificando se Está Funcionando

### Verificar Serviços Docker

```bash
# Ver todos os containers rodando
docker-compose ps

# Deve mostrar:
# cleantrack_web_1        - UP
# cleantrack_db_1         - UP
# cleantrack_redis_1      - UP
# cleantrack_celery_1     - UP
# cleantrack_celery-beat_1 - UP
```

### Verificar Logs

```bash
# Logs da aplicação web
docker-compose logs web

# Logs do Celery
docker-compose logs celery

# Logs do banco de dados
docker-compose logs db

# Seguir logs em tempo real
docker-compose logs -f web
```

### Testar Endpoints

```bash
# Testar a home page
curl http://localhost:8000/

# Testar o admin
curl http://localhost:8000/admin/

# Testar webhook (deve retornar erro 400 sem signature)
curl -X POST http://localhost:8000/billing/webhooks/stripe/
```

---

## 🧪 Testando Integrações

### Stripe Webhook (Local)

```bash
# 1. Instale Stripe CLI
# Mac:
brew install stripe/stripe-cli/stripe

# Linux:
wget https://github.com/stripe/stripe-cli/releases/download/v1.19.5/stripe_1.19.5_linux_x86_64.tar.gz
tar -xvf stripe_1.19.5_linux_x86_64.tar.gz
sudo mv stripe /usr/local/bin/

# 2. Login no Stripe
stripe login

# 3. Encaminhe webhooks para seu local
stripe listen --forward-to localhost:8000/billing/webhooks/stripe/

# 4. Em outro terminal, dispare eventos de teste
stripe trigger customer.subscription.created
stripe trigger invoice.payment_succeeded
```

### Email Resend (Desenvolvimento)

```python
# No Django shell
docker-compose exec web python manage.py shell

# Execute:
from cleantrack.email_service import send_template_email

send_template_email(
    to_email='seu@email.com',
    subject='Teste CleanTrack',
    template_name='emails/welcome.html',
    context={
        'user_name': 'Teste',
        'account_name': 'Teste Hospital',
        'plan_name': 'Trial',
        'subscription_end_date': 'Janeiro 31, 2025',
        'max_locations': 5,
        'max_users': 10,
        'dashboard_url': 'http://localhost:8000/dashboard',
        'help_url': 'http://localhost:8000/help',
    }
)
```

---

## 📱 Acessando de Outro Dispositivo

Se você quiser acessar de outro computador/celular na mesma rede:

```bash
# 1. Descubra seu IP local
hostname -I
# Exemplo: 192.168.1.100

# 2. Adicione ao ALLOWED_HOSTS no .env
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.100

# 3. Reinicie o Docker
docker-compose restart web

# 4. Acesse de outro dispositivo
http://192.168.1.100:8000
```

---

## 🛑 Parando o Projeto

```bash
# Parar todos os containers (mas manter os dados)
docker-compose stop

# Parar e remover containers (dados persistem)
docker-compose down

# Parar, remover containers E volumes (APAGA TUDO)
docker-compose down -v
```

---

## 🔄 Reiniciando do Zero

```bash
# 1. Parar tudo
docker-compose down -v

# 2. Remover imagens antigas
docker-compose build --no-cache

# 3. Iniciar novamente
docker-compose up --build

# 4. Em outro terminal, refazer migrations e dados
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py create_demo_data
```

---

## 📖 Explorando o Código

### Principais Arquivos

```
cleantrack/
├── accounts/models.py      # Usuários, Contas, Localizações
├── equipment/models.py     # Equipamentos, Protocolos
├── compliance/models.py    # Logs de Limpeza, Alertas
├── billing/views.py        # Webhook Stripe
├── cleantrack/email_service.py  # Serviço de Email
└── templates/emails/       # Templates HTML
```

### Interface Admin

Para personalizar o admin, veja:
```
accounts/admin.py
equipment/admin.py
compliance/admin.py
```

---

## 🎨 Próximos Passos

### 1. **Explore a Documentação**
```bash
# Leia os guias:
cat README.md
cat LEIAME_PT.md
cat QUICKSTART.md
cat INTEGRATION_EXAMPLES.md
```

### 2. **Personalize o Sistema**
- Edite templates em `templates/`
- Adicione novos tipos de equipamento
- Crie protocolos de limpeza personalizados

### 3. **Configure Integrações**
- Adicione suas chaves Stripe em `.env`
- Configure Resend para envio de emails
- Conecte sensores IoT (futuro)

### 4. **Deploy em Produção**
- Leia `DEPLOYMENT_CHECKLIST.md`
- Configure domínio e SSL
- Use serviços como Render, Fly.io ou AWS

---

## 📞 Suporte

### Problemas Comuns

**"Port already in use"**
```bash
# Pare o processo na porta 8000
sudo lsof -ti:8000 | xargs kill -9

# Ou mude a porta no docker-compose.yml
ports:
  - "8001:8000"
```

**"Database connection failed"**
```bash
# Verifique se o PostgreSQL está rodando
docker-compose ps db

# Reinicie o container do banco
docker-compose restart db
```

**"Module not found"**
```bash
# Reinstale dependências
docker-compose exec web pip install -r requirements.txt

# Ou rebuild a imagem
docker-compose build --no-cache web
```

---

## 🎉 Resumo de Comandos Rápidos

```bash
# Iniciar projeto
docker-compose up

# Acessar shell Django
docker-compose exec web python manage.py shell

# Ver logs
docker-compose logs -f web

# Executar migrações
docker-compose exec web python manage.py migrate

# Criar superusuário
docker-compose exec web python manage.py createsuperuser

# Dados demo
docker-compose exec web python manage.py create_demo_data

# Parar projeto
docker-compose down
```

---

## 🌟 Links Importantes

| Recurso | URL |
|---------|-----|
| 🏠 Home | http://localhost:8000 |
| 🔐 Admin | http://localhost:8000/admin |
| 📨 Webhook Stripe | http://localhost:8000/billing/webhooks/stripe/ |
| 👤 Login | http://localhost:8000/accounts/login/ |
| 📝 Signup | http://localhost:8000/accounts/signup/ |

---

**Pronto para começar!** 🚀

Execute `docker-compose up` e acesse http://localhost:8000
