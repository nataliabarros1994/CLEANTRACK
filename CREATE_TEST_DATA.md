# 🚀 Criação Rápida de Dados de Teste

## 📋 Comando Principal

```bash
docker-compose exec web python manage.py createsuperuser
```

**Preencha:**
```
Email address: admin@cleantrack.local
Username: admin
First name: Admin
Last name: CleanTrack
Password: Admin@2025
Password (again): Admin@2025
```

---

## ⚡ Script Automatizado - Criar Todos os Dados de Teste

Copie e cole este script no Django shell para criar todos os dados de uma vez:

```bash
docker-compose exec web python manage.py shell
```

Cole o código abaixo:

```python
from django.utils import timezone
from datetime import timedelta
from apps.accounts.models import User
from apps.facilities.models import Facility
from apps.equipment.models import Equipment
from apps.cleaning_logs.models import CleaningLog

print("╔══════════════════════════════════════════════════════════════╗")
print("║          CRIANDO DADOS DE TESTE - CLEANTRACK                ║")
print("╚══════════════════════════════════════════════════════════════╝")
print()

# ============================================================
# PASSO 1: Criar Usuários
# ============================================================
print("👥 Criando usuários...")

# Gerente
gerente, created = User.objects.get_or_create(
    username='gerente1',
    defaults={
        'email': 'gerente@cleantrack.local',
        'first_name': 'João',
        'last_name': 'Silva',
        'role': 'manager',
        'phone': '(11) 98765-4321',
        'is_active': True,
    }
)
if created:
    gerente.set_password('Gerente@2025')
    gerente.save()
    print(f"   ✅ Gerente criado: {gerente.get_full_name()}")
else:
    print(f"   ℹ️  Gerente já existe: {gerente.get_full_name()}")

# Técnico
tecnico, created = User.objects.get_or_create(
    username='tecnico1',
    defaults={
        'email': 'tecnico@cleantrack.local',
        'first_name': 'Maria',
        'last_name': 'Santos',
        'role': 'technician',
        'phone': '(11) 91234-5678',
        'is_active': True,
    }
)
if created:
    tecnico.set_password('Tecnico@2025')
    tecnico.save()
    print(f"   ✅ Técnico criado: {tecnico.get_full_name()}")
else:
    print(f"   ℹ️  Técnico já existe: {tecnico.get_full_name()}")

# Auditor
auditor, created = User.objects.get_or_create(
    username='auditor1',
    defaults={
        'email': 'auditor@cleantrack.local',
        'first_name': 'Carlos',
        'last_name': 'Oliveira',
        'role': 'manager',
        'phone': '(11) 99876-5432',
        'is_active': True,
    }
)
if created:
    auditor.set_password('Auditor@2025')
    auditor.save()
    print(f"   ✅ Auditor criado: {auditor.get_full_name()}")
else:
    print(f"   ℹ️  Auditor já existe: {auditor.get_full_name()}")

print()

# ============================================================
# PASSO 2: Criar Facilities
# ============================================================
print("🏢 Criando facilities...")

# Facility 1: Hospital Central
hospital, created = Facility.objects.get_or_create(
    name='Hospital Central - Unidade Principal',
    defaults={
        'address': 'Av. Paulista, 1000 - São Paulo - SP, 01310-100',
        'is_active': True,
    }
)
if created:
    hospital.managers.add(gerente)
    print(f"   ✅ Facility criada: {hospital.name}")
else:
    print(f"   ℹ️  Facility já existe: {hospital.name}")

# Facility 2: Ala de Emergência
emergencia, created = Facility.objects.get_or_create(
    name='Hospital Central - Ala de Emergência',
    defaults={
        'address': 'Av. Paulista, 1000 - Bloco B - São Paulo - SP, 01310-100',
        'is_active': True,
    }
)
if created:
    emergencia.managers.add(gerente)
    print(f"   ✅ Facility criada: {emergencia.name}")
else:
    print(f"   ℹ️  Facility já existe: {emergencia.name}")

# Facility 3: Clínica
clinica, created = Facility.objects.get_or_create(
    name='Clínica de Diagnóstico Norte',
    defaults={
        'address': 'Rua Augusta, 500 - São Paulo - SP, 01305-000',
        'is_active': True,
    }
)
if created:
    clinica.managers.add(auditor)
    print(f"   ✅ Facility criada: {clinica.name}")
else:
    print(f"   ℹ️  Facility já existe: {clinica.name}")

print()

# ============================================================
# PASSO 3: Criar Equipamentos
# ============================================================
print("🔧 Criando equipamentos...")

equipamentos = [
    {
        'facility': hospital,
        'name': 'Ultrassom GE LOGIQ P9',
        'serial_number': 'US-GE-2024-001',
        'cleaning_frequency_hours': 24,
    },
    {
        'facility': hospital,
        'name': 'Ressonância Magnética Siemens 3T',
        'serial_number': 'RM-SIEMENS-2024-001',
        'cleaning_frequency_hours': 48,
    },
    {
        'facility': emergencia,
        'name': 'Tomógrafo Philips 128 canais',
        'serial_number': 'TC-PHILIPS-2024-001',
        'cleaning_frequency_hours': 12,
    },
    {
        'facility': emergencia,
        'name': 'Desfibrilador Philips HeartStart',
        'serial_number': 'DF-PHILIPS-2024-001',
        'cleaning_frequency_hours': 8,
    },
    {
        'facility': clinica,
        'name': 'Raio-X Digital Agfa',
        'serial_number': 'RX-AGFA-2024-001',
        'cleaning_frequency_hours': 24,
    },
]

equipamentos_criados = []

for eq_data in equipamentos:
    eq, created = Equipment.objects.get_or_create(
        serial_number=eq_data['serial_number'],
        defaults={
            'facility': eq_data['facility'],
            'name': eq_data['name'],
            'cleaning_frequency_hours': eq_data['cleaning_frequency_hours'],
            'is_active': True,
        }
    )
    equipamentos_criados.append(eq)
    if created:
        print(f"   ✅ Equipamento criado: {eq.name}")
    else:
        print(f"   ℹ️  Equipamento já existe: {eq.name}")

print()

# ============================================================
# PASSO 4: Criar Cleaning Logs
# ============================================================
print("🧹 Criando limpezas...")

now = timezone.now()

limpezas = [
    # Limpeza recente (hoje)
    {
        'equipment': equipamentos_criados[0],  # Ultrassom
        'cleaned_by': tecnico,
        'cleaned_at': now - timedelta(hours=2),
        'notes': 'Limpeza de rotina completa. Utilizado álcool 70% e pano de microfibra.',
        'is_compliant': True,
    },
    # Limpeza antiga (5 dias atrás) - VAI FICAR OVERDUE
    {
        'equipment': equipamentos_criados[1],  # Ressonância
        'cleaned_by': tecnico,
        'cleaned_at': now - timedelta(days=5),
        'notes': 'Última limpeza antes do período de manutenção.',
        'is_compliant': True,
    },
    # Limpeza não conforme
    {
        'equipment': equipamentos_criados[2],  # Tomógrafo
        'cleaned_by': tecnico,
        'cleaned_at': now - timedelta(hours=6),
        'notes': 'Limpeza parcial devido a equipamento em uso. Necessário completar procedimento.',
        'is_compliant': False,
    },
    # Primeira limpeza do desfibrilador (hoje, manhã)
    {
        'equipment': equipamentos_criados[3],  # Desfibrilador
        'cleaned_by': tecnico,
        'cleaned_at': now.replace(hour=8, minute=0),
        'notes': 'Primeira limpeza do dia - turno da manhã',
        'is_compliant': True,
    },
    # Segunda limpeza do desfibrilador (hoje, tarde)
    {
        'equipment': equipamentos_criados[3],  # Desfibrilador
        'cleaned_by': tecnico,
        'cleaned_at': now.replace(hour=16, minute=0),
        'notes': 'Segunda limpeza do dia - turno da tarde',
        'is_compliant': True,
    },
    # Limpeza do Raio-X (ontem)
    {
        'equipment': equipamentos_criados[4],  # Raio-X
        'cleaned_by': tecnico,
        'cleaned_at': now - timedelta(days=1),
        'notes': 'Limpeza de rotina - procedimento padrão',
        'is_compliant': True,
    },
]

for limpeza_data in limpezas:
    log, created = CleaningLog.objects.get_or_create(
        equipment=limpeza_data['equipment'],
        cleaned_at=limpeza_data['cleaned_at'],
        defaults={
            'cleaned_by': limpeza_data['cleaned_by'],
            'notes': limpeza_data['notes'],
            'is_compliant': limpeza_data['is_compliant'],
        }
    )
    if created:
        eq_name = log.equipment.name[:30] + '...' if len(log.equipment.name) > 30 else log.equipment.name
        print(f"   ✅ Limpeza criada: {eq_name}")

print()

# ============================================================
# RESUMO FINAL
# ============================================================
print("╔══════════════════════════════════════════════════════════════╗")
print("║                    DADOS CRIADOS COM SUCESSO!                ║")
print("╚══════════════════════════════════════════════════════════════╝")
print()

print("📊 RESUMO:")
print(f"   Usuários: {User.objects.count()}")
print(f"   Facilities: {Facility.objects.count()}")
print(f"   Equipamentos: {Equipment.objects.count()}")
print(f"   Limpezas: {CleaningLog.objects.count()}")
print()

print("👤 CREDENCIAIS:")
print(f"   Gerente:   gerente@cleantrack.local / Gerente@2025")
print(f"   Técnico:   tecnico@cleantrack.local / Tecnico@2025")
print(f"   Auditor:   auditor@cleantrack.local / Auditor@2025")
print()

print("🔗 PRÓXIMOS PASSOS:")
print(f"   1. Acesse: http://localhost:8000/admin")
print(f"   2. Faça login com as credenciais acima")
print(f"   3. Explore os dados criados!")
print()

print("✅ Execute 'exit()' para sair do shell")
```

---

## 🎯 Credenciais Criadas

| Usuário | Email | Senha | Role |
|---------|-------|-------|------|
| **Admin** | admin@cleantrack.local | Admin@2025 | Superuser |
| **Gerente** | gerente@cleantrack.local | Gerente@2025 | Manager |
| **Técnico** | tecnico@cleantrack.local | Tecnico@2025 | Technician |
| **Auditor** | auditor@cleantrack.local | Auditor@2025 | Manager |

---

## 📊 Dados Criados

### Facilities (3)
1. Hospital Central - Unidade Principal
2. Hospital Central - Ala de Emergência
3. Clínica de Diagnóstico Norte

### Equipamentos (5)
1. Ultrassom GE LOGIQ P9 (limpeza a cada 24h)
2. Ressonância Magnética Siemens 3T (48h) - **ESTARÁ OVERDUE**
3. Tomógrafo Philips 128 canais (12h)
4. Desfibrilador Philips HeartStart (8h)
5. Raio-X Digital Agfa (24h)

### Cleaning Logs (6)
- Limpezas recentes (hoje)
- Limpeza antiga (5 dias atrás)
- Limpeza não conforme
- Múltiplas limpezas do mesmo equipamento

---

## ✅ Verificação Rápida

Após criar os dados, verifique:

```bash
docker-compose exec web python manage.py shell
```

```python
from apps.accounts.models import User
from apps.facilities.models import Facility
from apps.equipment.models import Equipment
from apps.cleaning_logs.models import CleaningLog

print(f"Usuários: {User.objects.count()}")
print(f"Facilities: {Facility.objects.count()}")
print(f"Equipamentos: {Equipment.objects.count()}")
print(f"Limpezas: {CleaningLog.objects.count()}")

# Ver equipamentos atrasados
for eq in Equipment.objects.all():
    if eq.is_overdue:
        print(f"⚠️ ATRASADO: {eq.name}")

exit()
```

---

## 🌐 Testar no Admin

1. Acesse: http://localhost:8000/admin
2. Login: `admin@cleantrack.local` / `Admin@2025`
3. Explore:
   - ACCOUNTS → Users (4 usuários)
   - FACILITIES → Facilities (3 facilities)
   - EQUIPMENT → Equipment (5 equipamentos, 1 overdue)
   - CLEANING LOGS → Cleaning logs (6 limpezas)

---

## 🧹 Limpar Dados (Reset)

Se quiser começar do zero:

```bash
docker-compose exec web python manage.py shell
```

```python
from apps.accounts.models import User
from apps.facilities.models import Facility
from apps.equipment.models import Equipment
from apps.cleaning_logs.models import CleaningLog

# CUIDADO: Isso apaga TUDO!
CleaningLog.objects.all().delete()
Equipment.objects.all().delete()
Facility.objects.all().delete()
User.objects.filter(is_superuser=False).delete()

print("✅ Dados limpos! Execute o script de criação novamente.")
exit()
```

---

**Última atualização:** 2025-01-21
