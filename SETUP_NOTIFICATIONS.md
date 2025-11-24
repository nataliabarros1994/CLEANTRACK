# Setup do Sistema de Notificações - CleanTrack

Este guia mostra como configurar e usar o sistema de notificações por e-mail do CleanTrack.

## 1. Pré-requisitos

- Conta no [Resend](https://resend.com)
- Python 3.8+
- Django 5.0+
- Banco de dados PostgreSQL configurado

## 2. Instalação das Dependências

Certifique-se de que todas as dependências estão instaladas:

```bash
pip install -r requirements.txt
```

Pacotes principais para notificações:
- `resend==2.3.0` - Cliente da API Resend

## 3. Configuração da API Resend

### 3.1 Obter API Key

1. Acesse [resend.com](https://resend.com) e faça login
2. Vá em **API Keys**
3. Crie uma nova API key
4. Copie a chave gerada (começa com `re_`)

### 3.2 Configurar Variáveis de Ambiente

Adicione ao arquivo `.env` na raiz do projeto:

```bash
# Resend API
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Nota:** Para testes, você pode usar o domínio padrão `onboarding@resend.dev`. Para produção, você precisa verificar seu próprio domínio no Resend.

## 4. Aplicar Migrations

Execute as migrations para adicionar o campo `managed_facilities` ao modelo User:

```bash
python manage.py migrate accounts
```

Isso criará a tabela de relacionamento many-to-many entre User e Facility.

## 5. Configurar Gerentes de Facilities

### Opção A: Via Django Admin

1. Acesse `/admin/`
2. Vá em **Accounts > Users**
3. Edite ou crie um usuário
4. Defina o **role** como `manager` ou `admin`
5. Na seção **Managed facilities**, selecione as unidades que este gerente supervisiona
6. Salve

### Opção B: Via Django Shell

```bash
python manage.py shell
```

```python
from apps.accounts.models import User
from apps.facilities.models import Facility

# Criar um gerente
manager = User.objects.create_user(
    username='joao.silva',
    email='joao.silva@cleantrack.com',
    password='senha_segura',
    first_name='João',
    last_name='Silva',
    role='manager'
)

# Atribuir facilities ao gerente
facility_central = Facility.objects.get(name='Unidade Central')
facility_sul = Facility.objects.get(name='Unidade Sul')

manager.managed_facilities.add(facility_central, facility_sul)

print(f"Gerente {manager.get_full_name()} agora gerencia:")
for f in manager.managed_facilities.all():
    print(f"  - {f.name}")
```

### Opção C: Via código Python

```python
from apps.accounts.models import User
from apps.facilities.models import Facility

# Buscar gerente existente
manager = User.objects.get(email='gerente@exemplo.com')

# Buscar facility
facility = Facility.objects.get(id=1)

# Atribuir
manager.managed_facilities.add(facility)

# Remover (se necessário)
# manager.managed_facilities.remove(facility)

# Limpar todas (se necessário)
# manager.managed_facilities.clear()
```

## 6. Testar o Sistema de Notificações

### Teste 1: Email de Boas-Vindas

```bash
python manage.py shell
```

```python
from apps.notifications.services import send_welcome_email

send_welcome_email(
    to_email='seu-email@exemplo.com',
    user_name='Seu Nome'
)
```

Verifique seu email!

### Teste 2: Alerta de Limpeza Atrasada

```python
from apps.notifications.services import send_cleaning_alert

send_cleaning_alert(
    to_email='seu-email@exemplo.com',
    equipment_name='Autoclave 123 (Unidade Central) - LIMPEZA FORA DO PRAZO'
)
```

### Teste 3: Notificação de Limpeza Registrada

```python
from apps.notifications.services import notify_cleaning_registered
from apps.cleaning_logs.models import CleaningLog

# Buscar último registro
cleaning_log = CleaningLog.objects.last()

if cleaning_log:
    notify_cleaning_registered(cleaning_log)
else:
    print("Nenhum registro de limpeza encontrado")
```

### Teste 4: Script de Teste Interativo

Execute o script de teste interativo:

```bash
python apps/notifications/test_email.py
```

## 7. Integração com o Sistema

### 7.1 Notificações Automáticas de Limpeza Atrasada

As notificações de limpeza atrasada já estão integradas no modelo `CleaningLog`:

**Arquivo:** `apps/cleaning_logs/models.py`

```python
# Linhas 74-94
def _notify_managers_of_non_compliant_cleaning(self):
    """Send email notification to managers about non-compliant cleaning"""
    from apps.accounts.models import User
    from apps.notifications.services import send_cleaning_alert

    managers = User.objects.filter(
        role__in=['admin', 'manager'],
        is_active=True
    )

    for manager in managers:
        try:
            send_cleaning_alert(
                to_email=manager.email,
                equipment_name=f"{self.equipment.name} ({self.equipment.facility.name}) - LIMPEZA FORA DO PRAZO"
            )
        except Exception as e:
            print(f"Failed to send notification to {manager.email}: {e}")
```

Esta função é chamada automaticamente quando `is_compliant=False`.

### 7.2 Notificação Opcional de Registro de Limpeza

Para notificar gerentes sobre TODAS as limpezas (não apenas atrasadas), adicione em suas views/APIs:

```python
# Em apps/cleaning_logs/views.py

from apps.notifications.services import notify_cleaning_registered

def register_cleaning(request, equipment_id):
    if request.method == 'POST':
        # ... processar formulário ...

        cleaning_log = CleaningLog.objects.create(
            equipment=equipment,
            cleaned_by=request.user,
            cleaned_at=cleaned_at
        )

        # Notificar gerentes específicos da facility (ou fallback para todos)
        notify_cleaning_registered(cleaning_log)

        return redirect('success')
```

### 7.3 Email de Boas-Vindas Automático

Para enviar email de boas-vindas automaticamente quando um usuário é criado:

**Criar arquivo:** `apps/accounts/signals.py`

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import User
from apps.notifications.services import send_welcome_email

@receiver(post_save, sender=User)
def send_welcome_email_on_user_creation(sender, instance, created, **kwargs):
    """Envia email de boas-vindas quando um novo usuário é criado"""
    if created and instance.email:
        send_welcome_email(
            to_email=instance.email,
            user_name=instance.get_full_name()
        )
```

**Registrar signals em:** `apps/accounts/apps.py`

```python
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'

    def ready(self):
        import apps.accounts.signals  # Importa os signals
```

## 8. Fluxo de Notificações

### Notificação de Limpeza Atrasada (Automática)

```
Limpeza registrada fora do prazo
        ↓
CleaningLog.save() detecta is_compliant=False
        ↓
_notify_managers_of_non_compliant_cleaning()
        ↓
send_cleaning_alert() para cada manager/admin
        ↓
Email enviado via Resend
```

### Notificação de Limpeza Registrada (Opcional)

```
Limpeza registrada
        ↓
View/API chama notify_cleaning_registered()
        ↓
Estratégia de notificação:
  1. Gerentes da facility específica?
     ↓ SIM → Notifica apenas eles
     ↓ NÃO → Continue
  2. Managers/admins ativos?
     ↓ SIM → Notifica todos
     ↓ NÃO → Continue
  3. Superusuários?
     ↓ SIM → Notifica como fallback
        ↓
Email enviado via Resend
```

## 9. Logging e Debugging

### Configurar Logging

Em `cleantrack/settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/notifications.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'apps.notifications': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### Ver Logs

```bash
# Em tempo real
tail -f logs/notifications.log

# Ver últimas 50 linhas
tail -n 50 logs/notifications.log

# Filtrar erros
grep ERROR logs/notifications.log
```

## 10. Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'resend'"

**Solução:**
```bash
pip install resend==2.3.0
```

### Problema: "RESEND_API_KEY not configured"

**Solução:**
1. Verifique se o arquivo `.env` existe na raiz do projeto
2. Verifique se contém `RESEND_API_KEY=re_...`
3. Reinicie o servidor Django

### Problema: "No managers found to notify"

**Solução:**
1. Crie pelo menos um usuário com role `manager` ou `admin`
2. Certifique-se de que o usuário está ativo (`is_active=True`)
3. Verifique se o usuário tem um email válido

### Problema: Emails não estão sendo enviados

**Solução:**
1. Verifique os logs: `tail -f logs/notifications.log`
2. Verifique sua conta no Resend (limites de envio)
3. Teste com um email simples via shell
4. Verifique se a API key está correta

### Problema: Quero notificar apenas gerentes específicos

**Solução:**
Atribua gerentes às facilities:
```python
manager.managed_facilities.add(facility)
```

## 11. Próximos Passos (Opcional)

- [ ] Configurar domínio próprio no Resend para produção
- [ ] Implementar tarefas agendadas (Celery) para resumos semanais
- [ ] Adicionar preferências de notificação por usuário
- [ ] Criar templates HTML mais elaborados
- [ ] Adicionar notificações por SMS (Twilio)
- [ ] Implementar webhook para rastreamento de emails

## 12. Referências

- [Documentação Resend](https://resend.com/docs)
- [Django Signals](https://docs.djangoproject.com/en/5.0/topics/signals/)
- [Django Logging](https://docs.djangoproject.com/en/5.0/topics/logging/)

---

**Dúvidas?** Consulte o arquivo `apps/notifications/README.md` para mais detalhes sobre cada função.
