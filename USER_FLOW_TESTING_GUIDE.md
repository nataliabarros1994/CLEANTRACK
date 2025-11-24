# 👥 Guia Completo - Teste de Fluxo de Usuário

## 🎯 Objetivo

Testar todo o fluxo de usuário do CleanTrack, desde a criação do superusuário até o gerenciamento completo de equipamentos e limpezas.

---

## 📋 Pré-requisitos

### Verificar Containers

```bash
docker-compose ps
```

**Status esperado:**
```
cleantrack_web_1    Up    0.0.0.0:8000->8000/tcp
cleantrack_db_1     Up    0.0.0.0:5432->5432/tcp
```

Se não estiverem rodando:
```bash
docker-compose up -d
```

---

## 🔑 PASSO 1: Criar Superusuário

### Comando

```bash
docker-compose exec web python manage.py createsuperuser
```

### Preencher Dados

O sistema pedirá as seguintes informações:

```
Email address: admin@cleantrack.local
Username: admin
First name: Admin
Last name: CleanTrack
Password: ********
Password (again): ********
```

**Recomendações:**
- Email: `admin@cleantrack.local`
- Username: `admin`
- First name: `Admin`
- Last name: `CleanTrack`
- Password: Escolha uma senha segura (ex: `Admin@2025`)

**✅ Resultado esperado:**
```
Superuser created successfully.
```

---

## 🌐 PASSO 2: Acessar Admin Django

### Abrir Admin

Abra o navegador e acesse:
```
http://localhost:8000/admin
```

### Fazer Login

```
Email: admin@cleantrack.local
Password: (senha que você criou)
```

**✅ Você verá o painel do Django Admin com:**
- ACCOUNTS (Users, Accounts)
- FACILITIES (Facilities)
- EQUIPMENT (Equipment)
- CLEANING LOGS (Cleaning Logs)
- BILLING (Stripe models)
- NOTIFICATIONS

---

## 👤 PASSO 3: Criar Usuários

### 3.1. Criar Gerente (Manager)

1. No admin, clique em **ACCOUNTS** → **Users**
2. Clique em **ADD USER +** (canto superior direito)
3. Preencha:

```
Email address: gerente@cleantrack.local
Username: gerente1
First name: João
Last name: Silva
Password: Gerente@2025
Password confirmation: Gerente@2025
```

4. Na seção **PERSONAL INFO**:
```
Phone: (11) 98765-4321
Role: Manager
```

5. Na seção **PERMISSIONS**:
```
☑ Active
☐ Staff status (deixe desmarcado)
☐ Superuser status (deixe desmarcado)
```

6. Clique em **SAVE**

---

### 3.2. Criar Técnico (Technician)

1. Clique em **ADD USER +** novamente
2. Preencha:

```
Email address: tecnico@cleantrack.local
Username: tecnico1
First name: Maria
Last name: Santos
Password: Tecnico@2025
Password confirmation: Tecnico@2025

Phone: (11) 91234-5678
Role: Technician
```

3. Marque apenas:
```
☑ Active
☐ Staff status
☐ Superuser status
```

4. Clique em **SAVE**

---

### 3.3. Criar Auditor

1. Clique em **ADD USER +**
2. Preencha:

```
Email address: auditor@cleantrack.local
Username: auditor1
First name: Carlos
Last name: Oliveira
Password: Auditor@2025
Password confirmation: Auditor@2025

Phone: (11) 99876-5432
Role: Manager (ou pode adicionar role "auditor" no código)
```

3. Marque:
```
☑ Active
☐ Staff status
```

4. Clique em **SAVE**

---

## 🏢 PASSO 4: Criar Facilities (Unidades)

### 4.1. Criar Unidade Principal

1. No menu lateral, clique em **FACILITIES** → **Facilities**
2. Clique em **ADD FACILITY +**
3. Preencha:

```
Name: Hospital Central - Unidade Principal
Address: Av. Paulista, 1000 - São Paulo - SP, 01310-100

☑ Is active

Stripe customer id: (deixe vazio por enquanto)
```

4. Na seção **MANAGERS**:
   - Selecione o gerente que você criou (gerente1)
   - Use Ctrl+Clique para selecionar múltiplos

5. Clique em **SAVE**

---

### 4.2. Criar Unidade Secundária

1. Clique em **ADD FACILITY +**
2. Preencha:

```
Name: Hospital Central - Ala de Emergência
Address: Av. Paulista, 1000 - Bloco B - São Paulo - SP, 01310-100

☑ Is active
```

3. Selecione gerentes
4. Clique em **SAVE**

---

### 4.3. Criar Clínica

1. Clique em **ADD FACILITY +**
2. Preencha:

```
Name: Clínica de Diagnóstico Norte
Address: Rua Augusta, 500 - São Paulo - SP, 01305-000

☑ Is active
```

3. Clique em **SAVE**

---

## 🔧 PASSO 5: Criar Equipamentos

### 5.1. Criar Ultrassom

1. Clique em **EQUIPMENT** → **Equipment**
2. Clique em **ADD EQUIPMENT +**
3. Preencha:

```
Facility: Hospital Central - Unidade Principal

Name: Ultrassom GE LOGIQ P9
Serial number: US-GE-2024-001

Cleaning frequency hours: 24
(significa: deve ser limpo a cada 24 horas = diariamente)

☑ Is active
```

4. Clique em **SAVE**

---

### 5.2. Criar Ressonância Magnética

1. Clique em **ADD EQUIPMENT +**
2. Preencha:

```
Facility: Hospital Central - Unidade Principal

Name: Ressonância Magnética Siemens 3T
Serial number: RM-SIEMENS-2024-001

Cleaning frequency hours: 48
(48 horas = a cada 2 dias)

☑ Is active
```

3. Clique em **SAVE**

---

### 5.3. Criar Tomógrafo

1. Clique em **ADD EQUIPMENT +**
2. Preencha:

```
Facility: Hospital Central - Ala de Emergência

Name: Tomógrafo Philips 128 canais
Serial number: TC-PHILIPS-2024-001

Cleaning frequency hours: 12
(12 horas = 2x ao dia)

☑ Is active
```

3. Clique em **SAVE**

---

### 5.4. Criar Raio-X

1. Clique em **ADD EQUIPMENT +**
2. Preencha:

```
Facility: Clínica de Diagnóstico Norte

Name: Raio-X Digital Agfa
Serial number: RX-AGFA-2024-001

Cleaning frequency hours: 24

☑ Is active
```

3. Clique em **SAVE**

---

### 5.5. Criar Equipamento de Emergência

1. Clique em **ADD EQUIPMENT +**
2. Preencha:

```
Facility: Hospital Central - Ala de Emergência

Name: Desfibrilador Philips HeartStart
Serial number: DF-PHILIPS-2024-001

Cleaning frequency hours: 8
(8 horas = 3x ao dia - equipamento crítico)

☑ Is active
```

3. Clique em **SAVE**

---

## 🧹 PASSO 6: Registrar Limpezas

### 6.1. Limpeza Recente (Compliant)

1. Clique em **CLEANING LOGS** → **Cleaning logs**
2. Clique em **ADD CLEANING LOG +**
3. Preencha:

```
Equipment: Ultrassom GE LOGIQ P9
Cleaned by: tecnico1 (Maria Santos)
Cleaned at: (clique no calendário e selecione HOJE, hora atual)

Notes: Limpeza de rotina completa. Utilizado álcool 70% e pano de microfibra.

☑ Is compliant

Photo: (opcional - pode fazer upload de uma foto de teste)
```

4. Clique em **SAVE**

---

### 6.2. Limpeza Antiga (Para testar overdue)

1. Clique em **ADD CLEANING LOG +**
2. Preencha:

```
Equipment: Ressonância Magnética Siemens 3T
Cleaned by: tecnico1
Cleaned at: (selecione uma data 5 DIAS ATRÁS)
            Exemplo: se hoje é 21/01, coloque 16/01

Notes: Última limpeza antes do período de manutenção.

☑ Is compliant
```

3. Clique em **SAVE**

**⚠️ Este equipamento deve aparecer como OVERDUE pois a última limpeza foi há 5 dias e a frequência é de 48h.**

---

### 6.3. Limpeza Não Conforme (Non-compliant)

1. Clique em **ADD CLEANING LOG +**
2. Preencha:

```
Equipment: Tomógrafo Philips 128 canais
Cleaned by: tecnico1
Cleaned at: (hoje, algumas horas atrás)

Notes: Limpeza parcial devido a equipamento em uso. Necessário completar procedimento.

☐ Is compliant (DESMARQUE)
```

3. Clique em **SAVE**

---

### 6.4. Múltiplas Limpezas (Histórico)

Crie mais algumas limpezas variando:
- Equipamentos diferentes
- Datas diferentes
- Técnicos diferentes
- Status de conformidade

**Exemplo:**

```
Equipment: Desfibrilador Philips HeartStart
Cleaned by: tecnico1
Cleaned at: HOJE, 08:00
Notes: Primeira limpeza do dia
☑ Is compliant
```

```
Equipment: Desfibrilador Philips HeartStart
Cleaned by: tecnico1
Cleaned at: HOJE, 16:00
Notes: Segunda limpeza do dia
☑ Is compliant
```

```
Equipment: Raio-X Digital Agfa
Cleaned by: tecnico1
Cleaned at: ONTEM
Notes: Limpeza de rotina
☑ Is compliant
```

---

## 📊 PASSO 7: Verificar Funcionalidades

### 7.1. Verificar Equipment Overdue

1. Vá para **EQUIPMENT** → **Equipment**
2. Procure pela coluna **Overdue** (ícone vermelho ❌ ou verde ✅)
3. Equipamentos que não foram limpos dentro da frequência devem mostrar ❌

**Equipamentos que DEVEM estar overdue:**
- ✅ Ressonância Magnética (última limpeza 5 dias atrás, frequência 48h)

---

### 7.2. Filtrar Equipment por Status

1. Na lista de Equipment, use os filtros do lado direito:
   - **By Active:** Selecione "Yes" para ver apenas ativos
   - **By Facility:** Selecione uma facility específica
   - **By Created date:** Veja por data de criação

---

### 7.3. Buscar Equipment

No campo de busca no topo:
```
Digite: "Ultrassom"
```

Deve encontrar: "Ultrassom GE LOGIQ P9"

---

### 7.4. Ver Histórico de Limpezas

1. Clique em um equipamento (ex: "Ultrassom GE LOGIQ P9")
2. Role até o final da página
3. Você verá a seção **CLEANING LOGS** com todas as limpezas deste equipamento

**Informações visíveis:**
- Data/hora da limpeza
- Quem limpou
- Status de conformidade
- Notas

---

### 7.5. Verificar Cleaning Logs

1. Vá para **CLEANING LOGS** → **Cleaning logs**
2. Use filtros:
   - **By Is compliant:** Ver apenas conformes ou não-conformes
   - **By Equipment:** Filtrar por equipamento específico
   - **By Cleaned at:** Filtrar por data

---

### 7.6. Buscar Cleaning Logs

Busque por:
- Nome do equipamento: "Tomógrafo"
- Nome do técnico: "Maria"
- Número de série: "DF-PHILIPS-2024-001"
- Notas: "rotina"

---

## 🔍 PASSO 8: Testar no Django Shell

```bash
docker-compose exec web python manage.py shell
```

### 8.1. Verificar Usuários Criados

```python
from apps.accounts.models import User

# Listar todos os usuários
for user in User.objects.all():
    print(f"{user.username} - {user.get_full_name()} - Role: {user.role}")

# Resultado esperado:
# admin - Admin CleanTrack - Role: technician (ou admin)
# gerente1 - João Silva - Role: manager
# tecnico1 - Maria Santos - Role: technician
# auditor1 - Carlos Oliveira - Role: manager
```

---

### 8.2. Verificar Facilities

```python
from apps.facilities.models import Facility

# Listar facilities
for f in Facility.objects.all():
    managers = f.managers.all()
    manager_names = ", ".join([m.get_full_name() for m in managers])
    print(f"✓ {f.name}")
    print(f"  Endereço: {f.address}")
    print(f"  Ativo: {f.is_active}")
    print(f"  Gerentes: {manager_names or 'Nenhum'}")
    print()

# Contar
print(f"Total de facilities: {Facility.objects.count()}")
print(f"Facilities ativas: {Facility.objects.filter(is_active=True).count()}")
```

---

### 8.3. Verificar Equipamentos

```python
from apps.equipment.models import Equipment

# Listar equipamentos
for eq in Equipment.objects.all():
    print(f"✓ {eq.name}")
    print(f"  Facility: {eq.facility.name}")
    print(f"  Serial: {eq.serial_number}")
    print(f"  Frequência: a cada {eq.cleaning_frequency_hours}h")
    print(f"  Última limpeza: {eq.last_cleaning.cleaned_at if eq.last_cleaning else 'Nunca'}")
    print(f"  Status: {'⚠️ ATRASADO' if eq.is_overdue else '✅ OK'}")
    print()

# Contar
print(f"Total de equipamentos: {Equipment.objects.count()}")
print(f"Equipamentos ativos: {Equipment.objects.filter(is_active=True).count()}")
print(f"Equipamentos atrasados: {sum(1 for eq in Equipment.objects.all() if eq.is_overdue)}")
```

---

### 8.4. Verificar Cleaning Logs

```python
from apps.cleaning_logs.models import CleaningLog

# Listar limpezas
for log in CleaningLog.objects.order_by('-cleaned_at')[:10]:
    compliant = "✓ Conforme" if log.is_compliant else "✗ Não conforme"
    print(f"{log.cleaned_at.strftime('%d/%m/%Y %H:%M')}")
    print(f"  Equipamento: {log.equipment.name}")
    print(f"  Técnico: {log.cleaned_by.get_full_name() if log.cleaned_by else 'N/A'}")
    print(f"  Status: {compliant}")
    print()

# Estatísticas
total = CleaningLog.objects.count()
compliant = CleaningLog.objects.filter(is_compliant=True).count()
non_compliant = CleaningLog.objects.filter(is_compliant=False).count()

print(f"Total de limpezas: {total}")
print(f"Conformes: {compliant} ({compliant/total*100:.1f}%)")
print(f"Não conformes: {non_compliant} ({non_compliant/total*100:.1f}%)")
```

---

### 8.5. Testar Property is_overdue

```python
from apps.equipment.models import Equipment

# Verificar equipamentos atrasados
print("EQUIPAMENTOS ATRASADOS:")
print("=" * 60)

for eq in Equipment.objects.all():
    if eq.is_overdue:
        print(f"⚠️  {eq.name}")
        print(f"   Frequência: {eq.cleaning_frequency_hours}h")
        if eq.last_cleaning:
            print(f"   Última limpeza: {eq.last_cleaning.cleaned_at}")
        else:
            print(f"   Última limpeza: NUNCA")
        print()
```

---

### 8.6. Verificar Gerentes de Facilities

```python
from apps.accounts.models import User

# Ver facilities gerenciadas por cada gerente
for user in User.objects.filter(role='manager'):
    facilities = user.managed_facilities.all()
    print(f"👤 {user.get_full_name()}")
    print(f"   Facilities gerenciadas: {facilities.count()}")
    for f in facilities:
        print(f"   - {f.name}")
    print()
```

---

### 8.7. Sair do Shell

```python
exit()
```

---

## 📧 PASSO 9: Testar Notificações

### 9.1. Testar Email de Boas-vindas

```bash
docker-compose exec web python manage.py shell
```

```python
from apps.notifications.services import send_welcome_email

# Enviar email de teste
send_welcome_email('seu@email.com', 'Admin CleanTrack')

# Verificar resultado
# Deve retornar dados do email enviado
```

---

### 9.2. Testar Alerta de Limpeza

```python
from apps.notifications.services import send_cleaning_alert

# Enviar alerta
send_cleaning_alert('gerente@cleantrack.local', 'Ultrassom GE LOGIQ P9')
```

---

### 9.3. Testar Resumo de Conformidade

```python
from apps.notifications.services import send_compliance_summary

summary_data = {
    'total_equipment': 5,
    'cleanings_completed': 12,
    'overdue_count': 1,
    'compliance_rate': 94.0
}

send_compliance_summary('gerente@cleantrack.local', summary_data)
```

---

### 9.4. Testar Notificação de Limpeza Registrada

```python
from apps.cleaning_logs.models import CleaningLog
from apps.notifications.services import notify_cleaning_registered

# Pegar última limpeza
log = CleaningLog.objects.last()

# Enviar notificação
notify_cleaning_registered(log)

exit()
```

---

## 🎯 PASSO 10: Testar Webhooks Stripe

### 10.1. Iniciar Listener (se ainda não iniciou)

**Terminal separado:**
```bash
stripe listen --forward-to localhost:8000/billing/webhook/stripe/
```

---

### 10.2. Testar Ativação de Facility

```bash
stripe trigger checkout.session.completed
```

**Verificar:**
1. No admin: http://localhost:8000/admin/facilities/facility/
2. Deve ter uma nova facility criada com:
   - ✅ `is_active = True`
   - ✅ `stripe_customer_id` preenchido

---

## 📊 PASSO 11: Dashboard de Métricas (Manual)

### No Django Shell

```bash
docker-compose exec web python manage.py shell
```

```python
from apps.facilities.models import Facility
from apps.equipment.models import Equipment
from apps.cleaning_logs.models import CleaningLog
from django.utils import timezone
from datetime import timedelta

print("╔══════════════════════════════════════════════════════════════╗")
print("║              DASHBOARD DE MÉTRICAS - CLEANTRACK              ║")
print("╚══════════════════════════════════════════════════════════════╝")
print()

# Facilities
total_facilities = Facility.objects.count()
active_facilities = Facility.objects.filter(is_active=True).count()
print(f"🏢 FACILITIES:")
print(f"   Total: {total_facilities}")
print(f"   Ativas: {active_facilities}")
print()

# Equipment
total_equipment = Equipment.objects.count()
active_equipment = Equipment.objects.filter(is_active=True).count()
overdue_equipment = sum(1 for eq in Equipment.objects.all() if eq.is_overdue)
print(f"🔧 EQUIPAMENTOS:")
print(f"   Total: {total_equipment}")
print(f"   Ativos: {active_equipment}")
print(f"   Atrasados: {overdue_equipment} ({'⚠️' if overdue_equipment > 0 else '✅'})")
print()

# Cleaning Logs
total_cleanings = CleaningLog.objects.count()
compliant_cleanings = CleaningLog.objects.filter(is_compliant=True).count()
compliance_rate = (compliant_cleanings / total_cleanings * 100) if total_cleanings > 0 else 0

# Últimas 24h
yesterday = timezone.now() - timedelta(days=1)
cleanings_24h = CleaningLog.objects.filter(cleaned_at__gte=yesterday).count()

print(f"🧹 LIMPEZAS:")
print(f"   Total: {total_cleanings}")
print(f"   Conformes: {compliant_cleanings} ({compliance_rate:.1f}%)")
print(f"   Últimas 24h: {cleanings_24h}")
print()

# Top técnicos
from django.db.models import Count
top_technicians = CleaningLog.objects.values(
    'cleaned_by__first_name',
    'cleaned_by__last_name'
).annotate(
    total=Count('id')
).order_by('-total')[:3]

print(f"👥 TOP TÉCNICOS:")
for i, tech in enumerate(top_technicians, 1):
    name = f"{tech['cleaned_by__first_name']} {tech['cleaned_by__last_name']}"
    print(f"   {i}. {name}: {tech['total']} limpezas")
print()

exit()
```

---

## ✅ Checklist de Testes Completos

### Criação de Dados
- [ ] Superusuário criado
- [ ] 3 usuários criados (gerente, técnico, auditor)
- [ ] 3 facilities criadas
- [ ] 5 equipamentos criados
- [ ] 5+ limpezas registradas

### Funcionalidades Admin
- [ ] Login funcionando
- [ ] Busca de equipamentos funcionando
- [ ] Filtros de facilities funcionando
- [ ] Upload de foto em cleaning log funcionando
- [ ] Visualização de histórico de limpezas funcionando

### Propriedades e Lógica
- [ ] `is_overdue` detectando equipamentos atrasados
- [ ] `last_cleaning` retornando última limpeza
- [ ] Gerentes associados a facilities
- [ ] Status `is_active` funcionando

### Notificações
- [ ] Email de boas-vindas enviado
- [ ] Alerta de limpeza enviado
- [ ] Resumo de conformidade enviado
- [ ] Notificação de limpeza registrada enviada

### Webhooks
- [ ] Checkout completed criando facility
- [ ] Facility ativada após pagamento
- [ ] stripe_customer_id preenchido

### Verificações no Shell
- [ ] Usuários listados corretamente
- [ ] Facilities listadas com gerentes
- [ ] Equipamentos com status correto
- [ ] Limpezas com estatísticas corretas
- [ ] Dashboard de métricas exibido

---

## 🎊 Fluxo Completo Testado!

Se você completou todos os passos acima, seu CleanTrack está **100% funcional** e pronto para uso! 🚀

**Próximos passos:**
1. Criar views customizadas (dashboard, relatórios)
2. Implementar API REST
3. Adicionar mais funcionalidades (QR codes, IoT)
4. Deploy em produção

---

**Última atualização:** 2025-01-21
