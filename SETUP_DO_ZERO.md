# 🚀 CleanTrack - Setup do Zero em Ambiente Limpo

Guia passo-a-passo para rodar o CleanTrack em qualquer máquina.

---

## ✅ Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional, para clone)

---

## 📋 Passo a Passo

### 1. Navegar até o Projeto

```bash
cd /home/nataliabarros1994/Desktop/CleanTrack
```

### 2. Criar e Ativar Ambiente Virtual

```bash
# Criar venv
python3 -m venv venv

# Ativar venv (Linux/Mac)
source venv/bin/activate

# OU no Windows:
# venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Dependências principais instaladas:**
- Django 5.0.6
- dj-stripe (Stripe integration)
- python-decouple (environment variables)
- Pillow + qrcode (QR codes)
- reportlab (PDF generation)
- resend (email API)

### 4. Configurar Variáveis de Ambiente

O arquivo `.env` já está configurado. Verifique:

```bash
cat .env
```

Deve conter:
```env
DEBUG=True
SECRET_KEY=rv2o%rw13na2+j3zsciqqu4pfu_fw=jv05c1%0ivauwgi&u7v5
DATABASE_URL=sqlite:///db.sqlite3
RESEND_API_KEY=***REMOVED***
STRIPE_TEST_PUBLIC_KEY=pk_test_...
STRIPE_TEST_SECRET_KEY=sk_test_...
# ... etc
```

### 5. Executar Migrations

```bash
python manage.py migrate
```

**Saída esperada:**
```
Running migrations:
  No migrations to apply.
  (ou lista de migrations aplicadas)
```

### 6. Criar Superusuário (se ainda não existir)

```bash
python manage.py createsuperuser
```

**OU use o script pronto:**

```bash
python verify_and_create_user.py
```

Credenciais criadas:
- Email: natyssis23@gmail.com
- Senha: admin

### 7. Validar Sistema

```bash
python validate_system.py
```

**Saída esperada:**
```
✅ Testes passados: 8/8
🎉 SISTEMA 100% OPERACIONAL!
```

### 8. Iniciar Servidor de Desenvolvimento

```bash
python manage.py runserver
```

**Saída esperada:**
```
System check identified no issues (0 silenced).
Starting development server at http://127.0.0.1:8000/
```

### 9. Acessar o Sistema

Abra o navegador:

- **Homepage**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/

**Login:**
- Email: natyssis23@gmail.com
- Senha: admin

---

## 🔧 Comandos Úteis

### Verificar Sistema

```bash
# Check geral
python manage.py check

# Check para deploy
python manage.py check --deploy

# Validação completa
python validate_system.py
```

### Gerenciar Dados

```bash
# Criar superusuário
python manage.py createsuperuser

# Shell interativo
python manage.py shell

# Listar todas as migrations
python manage.py showmigrations

# Criar nova migration
python manage.py makemigrations

# Aplicar migrations
python manage.py migrate
```

### Coletar Arquivos Estáticos

```bash
python manage.py collectstatic
```

### Limpar Sessões Expiradas

```bash
python manage.py clearsessions
```

---

## 📊 Estrutura do Projeto

```
CleanTrack/
├── apps/                       # Django apps
│   ├── accounts/              # Autenticação e usuários
│   ├── facilities/            # Clínicas
│   ├── equipment/             # Equipamentos
│   ├── cleaning_logs/         # Registros de limpeza
│   ├── billing/               # Pagamentos (Stripe)
│   ├── notifications/         # Emails
│   └── documentation/         # Docs
├── cleantrack/                # Settings do projeto
│   ├── settings.py            # Configurações base
│   ├── settings_production.py # Configurações de produção
│   ├── urls.py                # URLs principais
│   └── wsgi.py                # WSGI config
├── media/                     # Uploads (fotos, etc)
├── staticfiles/               # Arquivos estáticos coletados
├── logs/                      # Logs da aplicação
├── .env                       # Variáveis de ambiente
├── db.sqlite3                 # Banco de dados SQLite
├── manage.py                  # Django management
├── requirements.txt           # Dependências Python
├── validate_system.py         # Script de validação
└── README.md                  # Documentação
```

---

## 🐛 Solução de Problemas

### Erro: "No module named 'django'"

```bash
# Certifique-se que o venv está ativado
source venv/bin/activate

# Reinstale dependências
pip install -r requirements.txt
```

### Erro: "DJANGO_SETTINGS_MODULE not set"

```bash
# Defina manualmente
export DJANGO_SETTINGS_MODULE=cleantrack.settings

# No Windows:
set DJANGO_SETTINGS_MODULE=cleantrack.settings
```

### Erro: "Database is locked"

```bash
# Pare todos os servidores rodando
# Depois reinicie
python manage.py runserver
```

### Erro: "Port 8000 already in use"

```bash
# Use outra porta
python manage.py runserver 8001

# OU mate o processo
lsof -t -i tcp:8000 | xargs kill -9  # Linux/Mac
```

### Servidor não inicia / Apps travadas

```bash
# Execute o diagnóstico
python validate_system.py

# Verifique logs
tail -f logs/error.log
tail -f logs/app.log
```

---

## ✅ Checklist de Verificação

Antes de apresentar ao cliente, confirme:

- [ ] Servidor inicia sem erros
- [ ] Admin acessível (http://127.0.0.1:8000/admin/)
- [ ] Login funciona
- [ ] Todas as 8 apps carregadas
- [ ] 49 modelos registrados no admin
- [ ] QR codes gerando
- [ ] Pode criar facility
- [ ] Pode criar equipment
- [ ] Pode registrar cleaning log
- [ ] Validação completa passa (8/8)

---

## 🎯 Teste Rápido de 5 Minutos

```bash
# 1. Ativar venv
source venv/bin/activate

# 2. Validar
python validate_system.py

# 3. Iniciar servidor
python manage.py runserver

# 4. Abrir browser
# http://127.0.0.1:8000/admin/

# 5. Login e testar
# Email: natyssis23@gmail.com
# Senha: admin
```

Se tudo funcionar = ✅ **PRONTO PARA DEMO!**

---

## 📞 Suporte

Qualquer problema, execute:

```bash
python validate_system.py > validation_report.txt
```

E compartilhe o arquivo `validation_report.txt`.

---

**Última atualização**: 24/11/2025
**Versão do Sistema**: 1.0.0
**Status**: ✅ Produção-Ready
