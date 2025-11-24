# 🔐 Proteção Granular do Endpoint de PDF

## ✅ Implementação Completa

Agora o endpoint de PDF possui **proteção granular** que verifica se o usuário tem permissão específica para acessar aquela facility.

---

## 🎯 Como Funciona

### Antes (Proteção Genérica):
```python
# Qualquer manager podia acessar qualquer facility
@user_passes_test(is_manager_or_admin)
def generate_labels_pdf(request, facility_id):
    # ...
```

**Problema:**
- ❌ Manager da Facility A podia acessar PDF da Facility B
- ❌ Sem verificação de relação entre manager e facility
- ❌ Brecha de segurança

---

### Agora (Proteção Granular):
```python
@manager_required
def generate_labels_pdf(request, facility_id):
    # Só acessa se for:
    # 1. Admin (acesso total) OU
    # 2. Manager desta facility específica
```

**Benefícios:**
- ✅ Manager só acessa PDFs das suas facilities
- ✅ Admin continua com acesso total
- ✅ Verificação no banco de dados (managed_facilities)
- ✅ Segurança reforçada

---

## 🔧 Código Implementado

### 1. Função de Verificação

```python
def facility_manager_or_admin(user, facility_id):
    """
    Verifica se o usuário pode gerenciar esta facility específica
    """
    if not user.is_authenticated:
        return False

    # Admins têm acesso total
    if hasattr(user, 'role') and user.role == 'admin':
        return True

    # Managers só acessam facilities que gerenciam
    if hasattr(user, 'role') and user.role == 'manager':
        return user.managed_facilities.filter(id=facility_id).exists()

    return False
```

**O que faz:**
1. Verifica se usuário está autenticado
2. Se for admin → ✅ Acesso total
3. Se for manager → Verifica relação com facility no banco
4. Qualquer outro caso → ❌ Bloqueado

---

### 2. Decorator Customizado

```python
def manager_required(view_func):
    """
    Decorator para proteger views que precisam verificar acesso à facility
    """
    @wraps(view_func)
    def wrapper(request, facility_id, *args, **kwargs):
        if not facility_manager_or_admin(request.user, facility_id):
            # Redireciona para login do admin com 'next' parameter
            login_url = reverse('admin:login')
            return redirect(f"{login_url}?next={request.path}")
        return view_func(request, facility_id, *args, **kwargs)
    return wrapper
```

**O que faz:**
1. Verifica permissão ANTES de executar a view
2. Se bloqueado → Redireciona para login com URL de retorno
3. Se autorizado → Executa a view normalmente
4. Usa `@wraps` para manter metadata da função original

---

### 3. Aplicação na View

```python
@require_http_methods(["GET"])
@manager_required  # <-- Proteção granular
def generate_labels_pdf(request, facility_id):
    # ... código do PDF ...
```

---

## 🧪 Cenários de Teste

### Cenário 1: Admin Global
```python
# Usuário: admin@cleantrack.com (role='admin')
# Facility: Qualquer (ID 1, 2, 3, etc.)

# Resultado: ✅ PERMITIDO
# Motivo: Admins têm acesso total
```

---

### Cenário 2: Manager da Facility
```python
# Usuário: manager@hospital-a.com (role='manager')
# Managed Facilities: [Facility ID 1]
# Tentando acessar: /equipment/labels/pdf/1/

# Resultado: ✅ PERMITIDO
# Motivo: Manager gerencia esta facility
```

---

### Cenário 3: Manager de Outra Facility
```python
# Usuário: manager@hospital-a.com (role='manager')
# Managed Facilities: [Facility ID 1]
# Tentando acessar: /equipment/labels/pdf/2/

# Resultado: ❌ BLOQUEADO (302 Redirect)
# Motivo: Manager NÃO gerencia a Facility ID 2
# Redirecionado para: /admin/login/?next=/equipment/labels/pdf/2/
```

---

### Cenário 4: Técnico
```python
# Usuário: tech@hospital.com (role='technician')
# Tentando acessar: /equipment/labels/pdf/1/

# Resultado: ❌ BLOQUEADO (302 Redirect)
# Motivo: Técnicos não têm permissão para gerar PDFs
# Redirecionado para: /admin/login/?next=/equipment/labels/pdf/1/
```

---

### Cenário 5: Não Autenticado
```python
# Usuário: Anônimo (não logado)
# Tentando acessar: /equipment/labels/pdf/1/

# Resultado: ❌ BLOQUEADO (302 Redirect)
# Motivo: Não está autenticado
# Redirecionado para: /admin/login/?next=/equipment/labels/pdf/1/
```

---

## 🔍 Query de Verificação

Quando um manager tenta acessar:

```python
# Django executa esta query:
user.managed_facilities.filter(id=facility_id).exists()

# SQL equivalente:
SELECT EXISTS(
    SELECT 1
    FROM facilities_facility_managers
    WHERE user_id = <manager_id>
    AND facility_id = <facility_id>
)
```

**Resultado:**
- `True` → Manager gerencia esta facility → ✅ Acesso permitido
- `False` → Manager NÃO gerencia → ❌ Bloqueado

---

## 📊 Matriz de Permissões

| Papel | Facility Própria | Facility de Outro | Qualquer Facility |
|-------|------------------|-------------------|-------------------|
| **Admin** | ✅ Permitido | ✅ Permitido | ✅ Permitido |
| **Manager** | ✅ Permitido | ❌ Bloqueado | ❌ Bloqueado |
| **Técnico** | ❌ Bloqueado | ❌ Bloqueado | ❌ Bloqueado |
| **Anônimo** | ❌ Bloqueado | ❌ Bloqueado | ❌ Bloqueado |

---

## 🎨 Fluxo de Acesso

```
1. Usuário clica em "🖨️ PDF" para Facility ID 1
   ↓
2. Request: GET /equipment/labels/pdf/1/
   ↓
3. Decorator @manager_required intercepta
   ↓
4. Executa facility_manager_or_admin(user, 1)
   ↓
5. Verifica:
   ┌─────────────────────────────────────┐
   │ user.is_authenticated? → Não        │ → Redirect para login
   │                                     │
   │ user.role == 'admin'? → Sim         │ → ✅ Permite acesso
   │                                     │
   │ user.role == 'manager' E            │
   │ user.managed_facilities.filter(     │
   │     id=1                            │
   │ ).exists()? → Sim                   │ → ✅ Permite acesso
   │                                     │
   │ Qualquer outro caso                 │ → ❌ Redirect para login
   └─────────────────────────────────────┘
   ↓
6. Se permitido: Gera e retorna PDF
   Se bloqueado: Redirect para /admin/login/?next=/equipment/labels/pdf/1/
```

---

## 🔐 Segurança Adicional

### 1. Proteção em Múltiplas Camadas

```python
# Camada 1: Decorator @manager_required
@manager_required
def generate_labels_pdf(request, facility_id):

    # Camada 2: get_object_or_404 (verifica se facility existe)
    facility = get_object_or_404(Facility, id=facility_id)

    # Camada 3: Filtragem por facility
    equipment_list = Equipment.objects.filter(
        facility=facility,
        is_active=True
    )
```

### 2. Redirect Inteligente

```python
# Salva URL original para retornar após login
login_url = reverse('admin:login')
return redirect(f"{login_url}?next={request.path}")

# Após login bem-sucedido, Django redireciona para:
# /equipment/labels/pdf/1/ (URL original)
```

### 3. Uso de `@wraps`

```python
from functools import wraps

@wraps(view_func)
def wrapper(request, facility_id, *args, **kwargs):
    # Mantém metadata da função original:
    # - __name__
    # - __doc__
    # - __module__
    # - etc.
```

---

## 🧪 Como Testar

### Teste 1: Admin Acessa Qualquer Facility
```bash
# 1. Login como admin
# 2. Acesse: http://localhost:8001/equipment/labels/pdf/1/
# 3. Acesse: http://localhost:8001/equipment/labels/pdf/2/
# Resultado esperado: Ambos funcionam ✅
```

### Teste 2: Manager Acessa Sua Facility
```bash
# 1. Login como manager que gerencia Facility ID 1
# 2. Acesse: http://localhost:8001/equipment/labels/pdf/1/
# Resultado esperado: PDF gerado ✅
```

### Teste 3: Manager Tenta Acessar Facility de Outro
```bash
# 1. Login como manager que gerencia Facility ID 1
# 2. Acesse: http://localhost:8001/equipment/labels/pdf/2/
# Resultado esperado: Redirect para login ❌
```

### Teste 4: Técnico Tenta Acessar
```bash
# 1. Login como técnico
# 2. Acesse: http://localhost:8001/equipment/labels/pdf/1/
# Resultado esperado: Redirect para login ❌
```

### Teste 5: Via Botão no Admin
```bash
# 1. Login como manager
# 2. Acesse Admin → Facilities
# 3. Veja lista: Só aparecem facilities que você gerencia
# 4. Clique em "🖨️ PDF" de uma facility
# Resultado esperado: PDF gerado ✅
```

---

## 📝 Logs de Auditoria (Opcional)

Para rastrear tentativas de acesso:

```python
import logging

logger = logging.getLogger(__name__)

def facility_manager_or_admin(user, facility_id):
    if not user.is_authenticated:
        logger.warning(f"Unauthenticated access attempt to facility {facility_id}")
        return False

    if hasattr(user, 'role') and user.role == 'admin':
        logger.info(f"Admin {user.email} accessed facility {facility_id}")
        return True

    if hasattr(user, 'role') and user.role == 'manager':
        has_access = user.managed_facilities.filter(id=facility_id).exists()
        if has_access:
            logger.info(f"Manager {user.email} accessed facility {facility_id}")
        else:
            logger.warning(f"Manager {user.email} attempted to access unauthorized facility {facility_id}")
        return has_access

    logger.warning(f"User {user.email} (role: {getattr(user, 'role', 'none')}) attempted to access facility {facility_id}")
    return False
```

---

## ✅ Conclusão

**Proteção Implementada:**
- ✅ Verificação granular por facility
- ✅ Managers só acessam suas facilities
- ✅ Admins mantêm acesso total
- ✅ Técnicos e anônimos bloqueados
- ✅ Redirect inteligente com URL de retorno
- ✅ Múltiplas camadas de segurança

**Arquivo Modificado:**
- `apps/equipment/views.py`

**Status:**
- 🚀 Pronto para produção

---

**Desenvolvido com Django 5.0.6 | Python 3.12**
**Data:** 2025-11-23
