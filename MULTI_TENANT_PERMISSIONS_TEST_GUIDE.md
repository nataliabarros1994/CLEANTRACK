# 🔐 Multi-Tenant Permissions & Isolation Testing Guide

## ✅ Test Data Created Successfully!

**Date:** 2025-01-21

---

## 📊 Test Data Summary

### Users Created

| Role | Email | Password | Username | Facilities |
|------|-------|----------|----------|------------|
| **Manager** | gerente@cleantrack.local | Gerente@2025 | gerente1 | Hospital Central + Emergência |
| **Technician** | tecnico@cleantrack.local | Tecnico@2025 | tecnico1 | Hospital Central + Emergência |
| **Manager** | auditor@cleantrack.local | Auditor@2025 | auditor1 | Clínica de Diagnóstico Norte |

### Facilities Created

1. **Hospital Central - Unidade Principal**
   - Manager: João Silva (gerente1)
   - Equipment: Ultrassom GE, Ressonância Magnética

2. **Hospital Central - Ala de Emergência**
   - Manager: João Silva (gerente1)
   - Equipment: Tomógrafo, Desfibrilador

3. **Clínica de Diagnóstico Norte**
   - Manager: Carlos Oliveira (auditor1)
   - Equipment: Raio-X Digital

### Equipment Created (5 total)

| # | Name | Serial | Facility | Frequency |
|---|------|--------|----------|-----------|
| 1 | Ultrassom GE LOGIQ P9 | US-GE-2024-001 | Hospital Central | 24h |
| 2 | Ressonância Magnética Siemens 3T | RM-SIEMENS-2024-001 | Hospital Central | 48h |
| 3 | Tomógrafo Philips 128 canais | TC-PHILIPS-2024-001 | Emergência | 12h |
| 4 | Desfibrilador Philips HeartStart | DF-PHILIPS-2024-001 | Emergência | 8h |
| 5 | Raio-X Digital Agfa | RX-AGFA-2024-001 | Clínica | 24h |

### Cleaning Logs Created (3 total)

- Ultrassom: Cleaned 2 hours ago ✅
- Ressonância: Cleaned 5 days ago (OVERDUE) ❌
- Tomógrafo: Cleaned 6 hours ago (non-compliant) ⚠️

---

## 🎯 Permission Requirements

### Role-Based Access Control

#### 1. **Superuser/Admin (is_superuser=True)**
- ✅ Can see ALL facilities
- ✅ Can see ALL equipment
- ✅ Can see ALL cleaning logs
- ✅ Full CRUD permissions on everything

#### 2. **Manager (role='manager')**
- ✅ Can see ONLY facilities they manage (`managed_facilities`)
- ✅ Can see ONLY equipment in their facilities
- ✅ Can see ONLY cleaning logs for their equipment
- ✅ Can manage multiple facilities
- ❌ Cannot see other managers' facilities

#### 3. **Technician (role='technician')**
- ✅ Can see ONLY facilities assigned to them (`managed_facilities`)
- ✅ Can see ONLY equipment in assigned facilities
- ✅ Can CREATE cleaning logs for assigned equipment
- ✅ Can VIEW cleaning logs for assigned equipment
- ❌ Cannot edit or delete cleaning logs
- ❌ Cannot see other facilities

---

## ⚠️ Current Implementation Status

### ❌ NOT IMPLEMENTED YET

The Django admin classes (`FacilityAdmin`, `EquipmentAdmin`, `CleaningLogAdmin`) **DO NOT** currently filter querysets based on user roles.

**Current behavior:**
- All users can see ALL facilities
- All users can see ALL equipment
- All users can see ALL cleaning logs

**This means:**
- ❌ No multi-tenant isolation
- ❌ Data leakage between facilities
- ❌ Security risk

---

## 🔧 Implementation Needed

### 1. Update `apps/facilities/admin.py`

```python
from django.contrib import admin
from .models import Facility


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'address']
    date_hierarchy = 'created_at'
    filter_horizontal = ['managers']

    def get_queryset(self, request):
        """
        Filter facilities based on user role:
        - Superusers see everything
        - Managers/Technicians see only their assigned facilities
        """
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        # Managers and technicians see only their facilities
        return qs.filter(managers=request.user)

    def has_change_permission(self, request, obj=None):
        """
        Managers can edit their facilities
        Technicians have read-only access
        """
        if request.user.is_superuser:
            return True

        if obj is None:
            return request.user.role == 'manager'

        # Check if user manages this facility
        if request.user.role == 'manager':
            return obj.managers.filter(id=request.user.id).exists()

        return False

    def has_delete_permission(self, request, obj=None):
        """Only superusers and managers can delete their own facilities"""
        if request.user.is_superuser:
            return True

        if obj is None:
            return request.user.role == 'manager'

        if request.user.role == 'manager':
            return obj.managers.filter(id=request.user.id).exists()

        return False
```

### 2. Update `apps/equipment/admin.py`

```python
from django.contrib import admin
from .models import Equipment


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'serial_number', 'facility', 'cleaning_frequency_hours', 'is_active', 'is_overdue']
    list_filter = ['is_active', 'facility', 'created_at']
    search_fields = ['name', 'serial_number']
    raw_id_fields = ['facility']
    date_hierarchy = 'created_at'

    def get_queryset(self, request):
        """
        Filter equipment based on user's assigned facilities
        """
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        # Filter by user's managed facilities
        return qs.filter(facility__managers=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Limit facility choices to user's managed facilities
        """
        if db_field.name == "facility" and not request.user.is_superuser:
            kwargs["queryset"] = request.user.managed_facilities.all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue?'

    def has_change_permission(self, request, obj=None):
        """Managers can edit, technicians have read-only"""
        if request.user.is_superuser:
            return True

        if obj is None:
            return request.user.role == 'manager'

        # Check if user has access to this equipment's facility
        if request.user.role == 'manager':
            return obj.facility.managers.filter(id=request.user.id).exists()

        return False

    def has_delete_permission(self, request, obj=None):
        """Only managers can delete equipment in their facilities"""
        if request.user.is_superuser:
            return True

        if obj is None:
            return request.user.role == 'manager'

        if request.user.role == 'manager':
            return obj.facility.managers.filter(id=request.user.id).exists()

        return False
```

### 3. Update `apps/cleaning_logs/admin.py`

```python
from django.contrib import admin
from .models import CleaningLog


@admin.register(CleaningLog)
class CleaningLogAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'cleaned_by', 'cleaned_at', 'is_compliant', 'created_at']
    list_filter = ['is_compliant', 'cleaned_at', 'created_at']
    search_fields = ['equipment__name', 'equipment__serial_number', 'cleaned_by__email', 'notes']
    raw_id_fields = ['equipment', 'cleaned_by']
    date_hierarchy = 'cleaned_at'
    readonly_fields = ['created_at']

    fieldsets = (
        ('Equipment & Staff', {
            'fields': ('equipment', 'cleaned_by')
        }),
        ('Cleaning Details', {
            'fields': ('cleaned_at', 'notes', 'photo', 'is_compliant')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """
        Filter cleaning logs based on user's assigned facilities
        """
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        # Filter by equipment in user's managed facilities
        return qs.filter(equipment__facility__managers=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Limit equipment choices to user's managed facilities
        """
        if db_field.name == "equipment" and not request.user.is_superuser:
            kwargs["queryset"] = Equipment.objects.filter(
                facility__managers=request.user
            )

        if db_field.name == "cleaned_by" and not request.user.is_superuser:
            # Show only technicians assigned to same facilities
            from apps.accounts.models import User
            kwargs["queryset"] = User.objects.filter(
                managed_facilities__in=request.user.managed_facilities.all()
            ).distinct()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request):
        """Technicians and managers can add cleaning logs"""
        return True

    def has_change_permission(self, request, obj=None):
        """Managers can edit, technicians have read-only"""
        if request.user.is_superuser:
            return True

        if obj is None:
            return request.user.role == 'manager'

        # Check if user has access to this log's equipment facility
        if request.user.role == 'manager':
            return obj.equipment.facility.managers.filter(id=request.user.id).exists()

        return False

    def has_delete_permission(self, request, obj=None):
        """Only managers can delete logs in their facilities"""
        if request.user.is_superuser:
            return True

        if obj is None:
            return request.user.role == 'manager'

        if request.user.role == 'manager':
            return obj.equipment.facility.managers.filter(id=request.user.id).exists()

        return False

    def save_model(self, request, obj, form, change):
        """Auto-fill cleaned_by if not set"""
        if not obj.cleaned_by and request.user.role == 'technician':
            obj.cleaned_by = request.user
        super().save_model(request, obj, form, change)
```

---

## 🧪 Manual Testing Steps

### Test 1: Login as Technician

```
1. Open: http://localhost:8000/admin
2. Login: tecnico@cleantrack.local / Tecnico@2025
3. Expected results:
   ✅ Can see only 2 facilities (Hospital Central + Emergência)
   ❌ Cannot see Clínica de Diagnóstico Norte
   ✅ Can see only 4 equipment (from Hospital + Emergência)
   ❌ Cannot see Raio-X from Clínica
   ✅ Can see cleaning logs from Hospital/Emergência only
   ✅ Can ADD new cleaning logs
   ❌ Cannot EDIT or DELETE cleaning logs
```

### Test 2: Login as Manager (Gerente)

```
1. Logout from technician
2. Login: gerente@cleantrack.local / Gerente@2025
3. Expected results:
   ✅ Can see only 2 facilities (Hospital Central + Emergência)
   ❌ Cannot see Clínica de Diagnóstico Norte
   ✅ Can see only 4 equipment (from Hospital + Emergência)
   ✅ Can EDIT equipment in his facilities
   ✅ Can DELETE equipment in his facilities
   ✅ Can EDIT cleaning logs in his facilities
   ✅ Can DELETE cleaning logs in his facilities
```

### Test 3: Login as Manager (Auditor)

```
1. Logout from gerente
2. Login: auditor@cleantrack.local / Auditor@2025
3. Expected results:
   ✅ Can see only 1 facility (Clínica de Diagnóstico Norte)
   ❌ Cannot see Hospital Central or Emergência
   ✅ Can see only 1 equipment (Raio-X)
   ❌ Cannot see equipment from Hospital
   ✅ Can manage his facility
   ✅ Can edit/delete equipment in his facility
```

### Test 4: Create Superuser and Login

```bash
docker-compose exec web python manage.py createsuperuser
# Email: admin@cleantrack.local
# Username: admin
# Password: Admin@2025
```

```
1. Login: admin@cleantrack.local / Admin@2025
2. Expected results:
   ✅ Can see ALL 3 facilities
   ✅ Can see ALL 5 equipment
   ✅ Can see ALL cleaning logs
   ✅ Full CRUD on everything
```

---

## 🔍 Automated Permission Testing Script

Run this in Django shell to verify permissions programmatically:

```bash
docker-compose exec -T web python manage.py shell <<'EOF'
from apps.accounts.models import User
from apps.facilities.models import Facility
from apps.equipment.models import Equipment
from apps.cleaning_logs.models import CleaningLog

print("╔══════════════════════════════════════════════════════════════╗")
print("║          TESTANDO PERMISSÕES MULTI-TENANT                   ║")
print("╚══════════════════════════════════════════════════════════════╝")
print()

# Get users
gerente = User.objects.get(username='gerente1')
tecnico = User.objects.get(username='tecnico1')
auditor = User.objects.get(username='auditor1')

print("👤 TESTE 1: TÉCNICO (Maria Santos)")
print("="*60)
tecnico_facilities = Facility.objects.filter(managers=tecnico)
tecnico_equipment = Equipment.objects.filter(facility__managers=tecnico)
tecnico_logs = CleaningLog.objects.filter(equipment__facility__managers=tecnico)

print(f"Facilities acessíveis: {tecnico_facilities.count()} (esperado: 2)")
for f in tecnico_facilities:
    print(f"   ✅ {f.name}")

print(f"\nEquipamentos acessíveis: {tecnico_equipment.count()} (esperado: 4)")
for e in tecnico_equipment:
    print(f"   ✅ {e.name} ({e.facility.name})")

print(f"\nCleaning Logs acessíveis: {tecnico_logs.count()} (esperado: 3)")
print()

print("👤 TESTE 2: GERENTE (João Silva)")
print("="*60)
gerente_facilities = Facility.objects.filter(managers=gerente)
gerente_equipment = Equipment.objects.filter(facility__managers=gerente)
gerente_logs = CleaningLog.objects.filter(equipment__facility__managers=gerente)

print(f"Facilities gerenciadas: {gerente_facilities.count()} (esperado: 2)")
for f in gerente_facilities:
    print(f"   ✅ {f.name}")

print(f"\nEquipamentos gerenciados: {gerente_equipment.count()} (esperado: 4)")
print(f"Cleaning Logs gerenciados: {gerente_logs.count()} (esperado: 3)")
print()

print("👤 TESTE 3: AUDITOR (Carlos Oliveira)")
print("="*60)
auditor_facilities = Facility.objects.filter(managers=auditor)
auditor_equipment = Equipment.objects.filter(facility__managers=auditor)
auditor_logs = CleaningLog.objects.filter(equipment__facility__managers=auditor)

print(f"Facilities gerenciadas: {auditor_facilities.count()} (esperado: 1)")
for f in auditor_facilities:
    print(f"   ✅ {f.name}")

print(f"\nEquipamentos gerenciados: {auditor_equipment.count()} (esperado: 1)")
for e in auditor_equipment:
    print(f"   ✅ {e.name}")

print(f"\nCleaning Logs gerenciados: {auditor_logs.count()} (esperado: 0)")
print()

print("╔══════════════════════════════════════════════════════════════╗")
print("║                    TESTES CONCLUÍDOS!                        ║")
print("╚══════════════════════════════════════════════════════════════╝")
EOF
```

---

## 📋 Testing Checklist

### Before Testing
- [ ] Migrations applied (`python manage.py migrate`)
- [ ] Test data created (users, facilities, equipment, logs)
- [ ] Superuser created for admin testing

### Technician Tests (tecnico@cleantrack.local)
- [ ] Can see only Hospital Central + Emergência
- [ ] Cannot see Clínica
- [ ] Can see only 4 equipment (not Raio-X)
- [ ] Can create cleaning logs
- [ ] Cannot edit cleaning logs
- [ ] Cannot delete cleaning logs
- [ ] Cannot create new equipment

### Manager Tests (gerente@cleantrack.local)
- [ ] Can see Hospital Central + Emergência
- [ ] Cannot see Clínica
- [ ] Can edit equipment in his facilities
- [ ] Can delete equipment in his facilities
- [ ] Can edit cleaning logs in his facilities
- [ ] Can create new facilities (only for superuser in reality)

### Auditor Tests (auditor@cleantrack.local)
- [ ] Can see only Clínica
- [ ] Cannot see Hospital Central or Emergência
- [ ] Can see only Raio-X equipment
- [ ] Can manage his facility
- [ ] Cannot access other facilities' data

### Superuser Tests (admin@cleantrack.local)
- [ ] Can see all 3 facilities
- [ ] Can see all 5 equipment
- [ ] Can see all cleaning logs
- [ ] Full CRUD on all models
- [ ] No restrictions

---

## 🚀 Next Steps

1. **Implement Admin Filters** - Add the `get_queryset()` methods to admin classes
2. **Test in Browser** - Manually verify each role's permissions
3. **Run Automated Tests** - Execute the permission testing script
4. **Document Results** - Record any issues or unexpected behavior
5. **Security Audit** - Verify no data leakage between tenants

---

**Last Updated:** 2025-01-21
