# Comandos Úteis - CleanTrack

Referência rápida de comandos para desenvolvimento e manutenção do CleanTrack.

---

## 🚀 Setup e Inicialização

```bash
# Instalar dependências
pip install -r requirements.txt

# Criar/ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Aplicar todas as migrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Iniciar servidor de desenvolvimento
python manage.py runserver

# Iniciar servidor em outra porta
python manage.py runserver 8080
```

---

## 🔄 Migrations

```bash
# Ver migrations pendentes
python manage.py showmigrations

# Criar migrations
python manage.py makemigrations

# Criar migration para app específico
python manage.py makemigrations accounts
python manage.py makemigrations facilities

# Aplicar migrations
python manage.py migrate

# Aplicar migration específica
python manage.py migrate accounts 0002

# Reverter migration
python manage.py migrate accounts 0001

# Ver SQL de uma migration
python manage.py sqlmigrate accounts 0002

# Verificar problemas
python manage.py check
```

---

## 🗃️ Banco de Dados

```bash
# Abrir shell do Django
python manage.py shell

# Abrir shell do banco de dados
python manage.py dbshell

# Dump do banco de dados (backup)
python manage.py dumpdata > backup.json

# Dump de um app específico
python manage.py dumpdata accounts > accounts_backup.json

# Restaurar backup
python manage.py loaddata backup.json

# Limpar banco de dados (cuidado!)
python manage.py flush
```

### Comandos no Django Shell

```python
# Importar modelos
from apps.accounts.models import User
from apps.facilities.models import Facility
from apps.equipment.models import Equipment
from apps.cleaning_logs.models import CleaningLog

# Contar registros
User.objects.count()
Facility.objects.count()
Equipment.objects.count()
CleaningLog.objects.count()

# Listar todos
User.objects.all()
Facility.objects.all()

# Filtrar
User.objects.filter(role='manager')
Facility.objects.filter(is_active=True)
Equipment.objects.filter(is_active=True, facility__name='Unidade Central')

# Buscar por ID
user = User.objects.get(id=1)
facility = Facility.objects.get(id=1)

# Criar
facility = Facility.objects.create(
    name='Nova Unidade',
    address='Rua Teste, 123'
)

# Atualizar
facility.is_active = True
facility.save()

# Deletar
facility.delete()

# Relações ManyToMany
user = User.objects.get(email='gerente@teste.com')
facility = Facility.objects.get(id=1)
user.managed_facilities.add(facility)        # Adicionar
user.managed_facilities.remove(facility)     # Remover
user.managed_facilities.clear()              # Limpar todos
user.managed_facilities.all()                # Listar todos

# Queries complexas
from django.db.models import Q, Count
Equipment.objects.filter(
    Q(facility__name__icontains='central') |
    Q(cleaning_frequency_hours=24)
)

# Agregar
Facility.objects.annotate(
    equipment_count=Count('equipment_set')
).values('name', 'equipment_count')
```

---

## 📧 Notificações (Resend)

```bash
# Testar emails interativamente
python apps/notifications/test_email.py

# Testar via shell
python manage.py shell

from apps.notifications.services import send_welcome_email
send_welcome_email('teste@exemplo.com', 'Nome Teste')

from apps.notifications.services import send_cleaning_alert
send_cleaning_alert('gerente@exemplo.com', 'Autoclave 123 - ATRASADA')

from apps.notifications.services import send_compliance_summary
send_compliance_summary('gerente@exemplo.com', {
    'total_equipment': 50,
    'cleanings_completed': 120,
    'overdue_count': 3,
    'compliance_rate': 94.0
})

from apps.notifications.services import notify_cleaning_registered
from apps.cleaning_logs.models import CleaningLog
log = CleaningLog.objects.last()
notify_cleaning_registered(log)
```

---

## 💳 Stripe Webhooks

```bash
# Instalar Stripe CLI (uma vez)
# macOS
brew install stripe/stripe-cli/stripe

# Linux
wget https://github.com/stripe/stripe-cli/releases/latest/download/stripe_X.X.X_linux_x86_64.tar.gz
tar -xvf stripe_X.X.X_linux_x86_64.tar.gz
sudo mv stripe /usr/local/bin/

# Login no Stripe
stripe login

# Encaminhar webhooks para local
stripe listen --forward-to localhost:8000/billing/webhook/stripe/

# Disparar eventos de teste
stripe trigger checkout.session.completed
stripe trigger customer.subscription.created
stripe trigger customer.subscription.updated
stripe trigger customer.subscription.deleted
stripe trigger invoice.payment_succeeded
stripe trigger invoice.payment_failed

# Ver logs de webhooks
stripe logs tail

# Testar webhooks sem Stripe CLI
python apps/billing/test_webhooks.py
```

---

## 📊 Admin Django

```bash
# Criar superusuário
python manage.py createsuperuser

# Mudar senha de usuário
python manage.py changepassword username

# Listar todos os usuários
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('\n'.join([f'{u.username} - {u.email}' for u in User.objects.all()]))"
```

---

## 🔍 Logs e Debugging

```bash
# Ver logs em tempo real
tail -f logs/cleantrack.log

# Ver logs de notificações
tail -f logs/cleantrack.log | grep "apps.notifications"

# Ver logs de billing
tail -f logs/cleantrack.log | grep "apps.billing"

# Ver apenas erros
tail -f logs/cleantrack.log | grep ERROR

# Ver últimas 100 linhas
tail -n 100 logs/cleantrack.log

# Buscar por padrão
grep "checkout.session.completed" logs/cleantrack.log

# Contar ocorrências
grep -c "Payment succeeded" logs/cleantrack.log
```

---

## 🧪 Testes

```bash
# Rodar todos os testes
python manage.py test

# Testar app específico
python manage.py test apps.accounts
python manage.py test apps.facilities
python manage.py test apps.billing

# Testar com verbose
python manage.py test --verbosity=2

# Manter banco de dados após teste
python manage.py test --keepdb

# Verificar cobertura (requer coverage)
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Gera relatório HTML
```

---

## 🔐 Segurança

```bash
# Verificar problemas de segurança
python manage.py check --deploy

# Gerar nova SECRET_KEY
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Ver configurações atuais (DEBUG MODE)
python manage.py diffsettings
```

---

## 📦 Dependências

```bash
# Listar dependências instaladas
pip list

# Listar pacotes desatualizados
pip list --outdated

# Atualizar pacote específico
pip install --upgrade django

# Congelar dependências
pip freeze > requirements.txt

# Instalar de requirements
pip install -r requirements.txt

# Verificar dependências não usadas
pip install pipdeptree
pipdeptree
```

---

## 🧹 Limpeza e Manutenção

```bash
# Limpar arquivos .pyc
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete

# Limpar migrations (cuidado!)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Limpar staticfiles
python manage.py collectstatic --clear --noinput

# Otimizar imagens (se tiver pillow-simd)
python manage.py optimize_images
```

---

## 🚀 Deploy e Produção

```bash
# Coletar arquivos estáticos
python manage.py collectstatic

# Verificar configuração para produção
python manage.py check --deploy

# Criar requirements.txt para produção
pip freeze > requirements.txt

# Executar gunicorn (servidor de produção)
gunicorn cleantrack.wsgi:application --bind 0.0.0.0:8000

# Com workers
gunicorn cleantrack.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 60 \
  --access-logfile -
```

---

## 🐳 Docker (se usar)

```bash
# Build da imagem
docker build -t cleantrack .

# Rodar container
docker run -p 8000:8000 cleantrack

# Com docker-compose
docker-compose up
docker-compose up -d  # Detached mode

# Ver logs
docker-compose logs -f

# Parar containers
docker-compose down

# Rebuild
docker-compose up --build

# Executar comando no container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## 🔄 Git

```bash
# Status
git status

# Adicionar mudanças
git add .
git add apps/notifications/

# Commit
git commit -m "feat: add Resend email notifications"

# Push
git push origin main

# Ver histórico
git log --oneline

# Ver diferenças
git diff
git diff apps/billing/views.py

# Criar branch
git checkout -b feature/new-feature

# Voltar para main
git checkout main

# Merge
git merge feature/new-feature

# Desfazer último commit (mantém mudanças)
git reset --soft HEAD~1

# Desfazer mudanças em arquivo
git checkout -- arquivo.py
```

---

## 📈 Performance

```bash
# Ver queries executadas
python manage.py shell

from django.db import connection
from django.db import reset_queries

# Habilitar query logging
from django.conf import settings
settings.DEBUG = True

# Executar queries
from apps.equipment.models import Equipment
list(Equipment.objects.all())

# Ver queries
print(len(connection.queries))
for q in connection.queries:
    print(q)

# Analisar query lenta
from django.db import connection
from apps.facilities.models import Facility
facilities = Facility.objects.prefetch_related('equipment_set').all()
print(connection.queries[-1]['sql'])
```

---

## 🛠️ Utilitários

```bash
# Abrir shell com IPython (mais bonito)
pip install ipython
python manage.py shell

# Executar script Python no contexto Django
python manage.py shell < script.py

# Ver estrutura de URLs
python manage.py show_urls  # requer django-extensions

# Gerar diagrama de modelos
pip install django-extensions pygraphviz
python manage.py graph_models -a -o models.png

# Verificar templates não usados
python manage.py validate_templates  # requer django-extensions
```

---

## 📝 Atalhos Personalizados

Adicione ao seu `.bashrc` ou `.zshrc`:

```bash
# Django shortcuts
alias dj='python manage.py'
alias djrun='python manage.py runserver'
alias djmm='python manage.py makemigrations'
alias djm='python manage.py migrate'
alias djs='python manage.py shell'
alias djt='python manage.py test'

# Logs
alias djlogs='tail -f logs/cleantrack.log'
alias djlogs-notif='tail -f logs/cleantrack.log | grep notifications'
alias djlogs-billing='tail -f logs/cleantrack.log | grep billing'

# Stripe
alias stripe-listen='stripe listen --forward-to localhost:8000/billing/webhook/stripe/'
```

Uso:
```bash
djrun           # python manage.py runserver
djmm            # python manage.py makemigrations
djm             # python manage.py migrate
djs             # python manage.py shell
djlogs          # tail -f logs/cleantrack.log
stripe-listen   # stripe listen --forward-to localhost:8000/billing/webhook/stripe/
```

---

## 🆘 Comandos de Emergência

```bash
# Reset completo do banco (CUIDADO!)
python manage.py reset_db  # requer django-extensions
python manage.py migrate
python manage.py createsuperuser

# Backup rápido antes de mudanças grandes
python manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json

# Restaurar backup
python manage.py loaddata backup_20250121_120000.json

# Ver processos Django rodando
ps aux | grep manage.py

# Matar processo Django travado
pkill -f "python manage.py runserver"
```

---

**Dica:** Salve os comandos mais usados em um arquivo `.bashrc` ou crie um `Makefile` para facilitar!
