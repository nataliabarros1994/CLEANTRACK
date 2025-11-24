# Serviço de Notificações - CleanTrack

Este módulo gerencia o envio de notificações por e-mail usando a API do Resend.

## Configuração

### 1. API Key do Resend

Certifique-se de ter a chave da API do Resend configurada no arquivo `.env`:

```
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 2. Relacionamento de Gerentes com Facilities

O sistema agora suporta atribuir gerentes específicos para cada facility através do campo `managed_facilities` no modelo User.

**Aplicar migrations:**

```bash
python manage.py migrate accounts
```

**Atribuir gerentes via Django Admin:**

1. Acesse o admin Django: `/admin/`
2. Vá em `Accounts > Users`
3. Edite um usuário com role `manager` ou `admin`
4. Na seção "Managed facilities", selecione as facilities que este gerente supervisiona
5. Salve

**Atribuir gerentes via código:**

```python
from apps.accounts.models import User
from apps.facilities.models import Facility

manager = User.objects.get(email='gerente@exemplo.com')
facility = Facility.objects.get(name='Unidade Central')

manager.managed_facilities.add(facility)
```

## Funções Disponíveis

### 1. `send_cleaning_alert(to_email, equipment_name)`

Envia alerta quando um equipamento está com limpeza atrasada (não conforme).

**Uso:**
```python
from apps.notifications.services import send_cleaning_alert

send_cleaning_alert(
    to_email='gerente@exemplo.com',
    equipment_name='Autoclave 123 (Unidade Central) - LIMPEZA FORA DO PRAZO'
)
```

**Quando é chamada:**
- Automaticamente pelo modelo `CleaningLog` quando `is_compliant=False`
- Ver `apps/cleaning_logs/models.py:74-94`

---

### 2. `send_compliance_summary(to_email, summary_data)`

Envia resumo semanal de conformidade com estatísticas.

**Uso:**
```python
from apps.notifications.services import send_compliance_summary

summary_data = {
    'total_equipment': 50,
    'cleanings_completed': 120,
    'overdue_count': 3,
    'compliance_rate': 94.0
}

send_compliance_summary(
    to_email='gerente@exemplo.com',
    summary_data=summary_data
)
```

**Quando usar:**
- Em tarefas agendadas (Celery, cron) para envio semanal
- Em dashboards para envio manual de relatórios

---

### 3. `send_welcome_email(to_email, user_name)`

Envia e-mail de boas-vindas para novos usuários.

**Uso:**
```python
from apps.notifications.services import send_welcome_email

send_welcome_email(
    to_email='novousuario@exemplo.com',
    user_name='João Silva'
)
```

**Quando usar:**
- Após criar um novo usuário via API ou admin
- Em signals `post_save` do modelo User (se implementado)

---

### 4. `notify_cleaning_registered(cleaning_log)`

Notifica gerentes sobre nova limpeza registrada (opcional).

**Estratégia de notificação inteligente:**
1. Primeiro tenta notificar gerentes **específicos da facility** (via `managed_facilities`)
2. Se não houver, notifica **todos os managers/admins** ativos
3. Se ainda não houver, notifica **superusuários** como fallback

**Uso:**
```python
from apps.notifications.services import notify_cleaning_registered
from apps.cleaning_logs.models import CleaningLog

# Após criar um registro de limpeza
cleaning_log = CleaningLog.objects.get(id=123)
notify_cleaning_registered(cleaning_log)
```

**Quando usar:**
- Opcionalmente após cada registro de limpeza
- Em views ou APIs de registro de limpeza
- **Nota:** Esta função NÃO é chamada automaticamente pelo modelo

**Exemplo de atribuição de gerente para usar notificação inteligente:**
```python
# Atribuir gerente a uma facility específica
manager = User.objects.get(email='joao@exemplo.com')
facility = Facility.objects.get(name='Unidade Sul')
manager.managed_facilities.add(facility)

# Agora, quando houver limpeza de equipamentos da "Unidade Sul",
# apenas João será notificado (em vez de todos os gerentes)
```

---

## Exemplo: Integrando com Views

```python
# Em apps/cleaning_logs/views.py ou apps/cleaning_logs/api/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from apps.cleaning_logs.models import CleaningLog
from apps.notifications.services import notify_cleaning_registered

def register_cleaning(request, equipment_id):
    if request.method == 'POST':
        # ... processar dados do formulário ...

        cleaning_log = CleaningLog.objects.create(
            equipment=equipment,
            cleaned_by=request.user,
            cleaned_at=cleaned_at,
            notes=notes
        )

        # Notificar gerentes (opcional)
        notify_cleaning_registered(cleaning_log)

        messages.success(request, 'Limpeza registrada com sucesso!')
        return redirect('equipment_detail', equipment_id=equipment.id)

    return render(request, 'cleaning_logs/register.html', context)
```

---

## Exemplo: Usando Django Signals

Você pode configurar signals para enviar notificações automaticamente:

```python
# Em apps/accounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import User
from apps.notifications.services import send_welcome_email

@receiver(post_save, sender=User)
def send_welcome_email_on_user_creation(sender, instance, created, **kwargs):
    if created:
        send_welcome_email(
            to_email=instance.email,
            user_name=instance.get_full_name()
        )
```

Não se esqueça de registrar os signals em `apps/accounts/apps.py`:

```python
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'

    def ready(self):
        import apps.accounts.signals
```

---

## Logging

Todas as funções usam o módulo de logging do Python. Para ver os logs:

```python
# Em settings.py

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'apps.notifications': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
```

---

## Notas Importantes

1. **Domínio do Remetente:** Atualmente usando `onboarding@resend.dev` para testes. Em produção, configure um domínio verificado no Resend.

2. **Taxa de Envio:** Resend tem limites de envio. Consulte sua conta para detalhes.

3. **Erros Não Fatais:** Todas as funções capturam exceções e retornam `None` em caso de erro, garantindo que falhas de e-mail não quebrem o fluxo principal.

4. **Retornos:** Todas as funções retornam o response do Resend em caso de sucesso ou `None` em caso de falha.

---

## Testando Localmente

```python
# No Django shell
python manage.py shell

from apps.notifications.services import send_welcome_email

# Enviar email de teste
send_welcome_email('seu-email@exemplo.com', 'Seu Nome')
```
