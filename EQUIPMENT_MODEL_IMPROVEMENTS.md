# 🚀 Melhorias no Modelo Equipment

## 📋 Resumo das Implementações

Implementamos **6 melhorias principais** no modelo Equipment conforme solicitado:

1. ✅ Método para regenerar token (segurança/revogação)
2. ✅ Melhorias no método `generate_qr_code` (URL completa, HTTPS em produção)
3. ✅ Propriedades para obter URL pública do QR
4. ✅ Método para validar tokens
5. ✅ Campos adicionais (descrição, localização, categoria)
6. ✅ Melhorias na geração do QR code (tamanho, correção de erros)

---

## 1️⃣ Novos Campos no Modelo

### Campos Adicionados

```python
# Informações Adicionais
description = models.TextField(
    "Descrição",
    blank=True,
    help_text="Descrição detalhada do equipamento"
)

category = models.CharField(
    "Categoria",
    max_length=20,
    choices=EQUIPMENT_CATEGORIES,
    default='other',
    help_text="Categoria do equipamento"
)

location = models.CharField(
    "Localização específica",
    max_length=200,
    blank=True,
    help_text="Ex: Sala 101, Ala B, 2º andar"
)
```

### Categorias Disponíveis

| Valor | Label |
|-------|-------|
| `diagnostic` | Diagnóstico |
| `monitoring` | Monitoramento |
| `life_support` | Suporte à Vida |
| `surgical` | Cirúrgico |
| `laboratory` | Laboratório |
| `other` | Outro |

---

## 2️⃣ Novas Propriedades

### `public_url`
Retorna a URL completa para registro via QR code.

```python
equipment = Equipment.objects.get(id=1)
print(equipment.public_url)
# Desenvolvimento: http://localhost:8000/log/IdYqlTd8wnpiXNz2HlNHWQ/
# Produção: https://app.cleantrack.com/log/IdYqlTd8wnpiXNz2HlNHWQ/
```

**Características:**
- ✅ Usa HTTPS automaticamente em produção (`DEBUG=False`)
- ✅ Usa HTTP em desenvolvimento (`DEBUG=True`)
- ✅ Obtém domínio do Django Sites framework
- ✅ Fallback para `localhost:8000` se Site não configurado

### `category_display`
Retorna o nome legível da categoria.

```python
equipment.category = 'diagnostic'
print(equipment.category_display)  # "Diagnóstico"
```

### `full_location`
Retorna localização completa (facility + localização específica).

```python
equipment.facility.name = "Hospital Central"
equipment.location = "Sala 101, Ala B"
print(equipment.full_location)  # "Hospital Central - Sala 101, Ala B"
```

---

## 3️⃣ Método `generate_qr_code()` Melhorado

### Assinatura
```python
def generate_qr_code(self, size=10, border=4, error_correction='H'):
```

### Parâmetros

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `size` | int | 10 | Tamanho do box (8-12 recomendado) |
| `border` | int | 4 | Tamanho da borda (mínimo 4) |
| `error_correction` | str | 'H' | Nível de correção de erros |

### Níveis de Correção de Erros

| Nível | Correção | Uso Recomendado |
|-------|----------|-----------------|
| `L` | 7% | Ambiente limpo, QR grande |
| `M` | 15% | Uso geral |
| `Q` | 25% | Ambiente com sujeira leve |
| `H` | 30% | **Padrão** - Máxima durabilidade |

### Exemplos de Uso

```python
# Gerar QR code padrão (alta correção de erros)
equipment.generate_qr_code()

# Gerar QR code maior (melhor para impressão)
equipment.generate_qr_code(size=12)

# Gerar QR code com correção média (menor tamanho)
equipment.generate_qr_code(error_correction='M')

# Personalizado: grande + borda pequena
equipment.generate_qr_code(size=15, border=2, error_correction='H')
```

### Melhorias Implementadas

- ✅ Usa `public_url` property (consistência + HTTPS automático)
- ✅ Correção de erros configurável
- ✅ Tamanho configurável
- ✅ Nome de arquivo único inclui parte do token
- ✅ Alto contraste (preto no branco)

---

## 4️⃣ Método `regenerate_token()`

### Uso Principal: Segurança e Revogação

```python
# Regenerar token e QR code (recomendado)
equipment = Equipment.objects.get(id=1)
new_token = equipment.regenerate_token()
print(f"Novo token: {new_token}")

# Regenerar apenas token (sem QR code)
new_token = equipment.regenerate_token(regenerate_qr=False)
```

### Quando Usar

| Situação | Ação |
|----------|------|
| 🚨 QR code comprometido | `equipment.regenerate_token()` |
| 🔒 Auditoria de segurança | `equipment.regenerate_token()` |
| 📄 Reimprimir QR code | `equipment.regenerate_token()` |
| ⚡ Rotação periódica | `equipment.regenerate_token()` |
| 🚫 Revogar acesso permanentemente | `equipment.revoke_access()` |

### Logging Automático

O método registra automaticamente a regeneração:

```
INFO: Token regenerated for equipment 5 (Desfibrilador Philips HeartStart).
      Old token: IdYqlTd8..., New token: 2r7Zgna2...
```

---

## 5️⃣ Método `validate_token()` (Class Method)

### Validação Simples e Segura

```python
# Validar token e obter equipamento
equipment = Equipment.validate_token('IdYqlTd8wnpiXNz2HlNHWQ')

if equipment:
    print(f"✅ Token válido: {equipment.name}")
else:
    print("❌ Token inválido ou equipamento inativo")
```

### Uso nas Views

```python
@require_http_methods(["GET", "POST"])
def public_cleaning_register(request, token):
    # Validar token
    equipment = Equipment.validate_token(token)

    if equipment is None:
        return JsonResponse({'error': 'Token inválido'}, status=404)

    # Processar registro...
```

### Validações Automáticas

- ✅ Token existe no banco
- ✅ Equipamento está ativo (`is_active=True`)
- ✅ Retorna `None` se inválido (nunca levanta exceção)

---

## 6️⃣ Método `revoke_access()`

### Revogar Acesso Permanentemente

```python
# Desativar equipamento (revoga acesso via QR code)
equipment = Equipment.objects.get(id=1)
equipment.revoke_access()

# Agora Equipment.validate_token(equipment.public_token) retorna None
```

### Diferença: `revoke_access()` vs `regenerate_token()`

| Método | Ação | Quando Usar |
|--------|------|-------------|
| `revoke_access()` | Desativa equipamento | Equipamento em manutenção, desativado permanentemente |
| `regenerate_token()` | Troca token, mantém ativo | QR code comprometido, rotação de segurança |

### Logging Automático

```
WARNING: Access revoked for equipment 5 (Desfibrilador Philips HeartStart).
         Token: IdYqlTd8...
```

---

## 📊 Comparação: Antes vs Depois

### Propriedades

| Recurso | Antes | Depois |
|---------|-------|--------|
| Obter URL pública | ❌ Não existia | ✅ `equipment.public_url` |
| Nome da categoria | ❌ Não existia | ✅ `equipment.category_display` |
| Localização completa | ❌ Só facility | ✅ `equipment.full_location` |

### Métodos

| Recurso | Antes | Depois |
|---------|-------|--------|
| Gerar QR code | ✅ Básico | ✅ Configurável (tamanho, correção) |
| Validar token | ❌ Manual no view | ✅ `Equipment.validate_token()` |
| Regenerar token | ❌ Não existia | ✅ `equipment.regenerate_token()` |
| Revogar acesso | ❌ Manual | ✅ `equipment.revoke_access()` |

### Campos

| Campo | Antes | Depois |
|-------|-------|--------|
| Descrição | ❌ | ✅ `description` (TextField) |
| Categoria | ❌ | ✅ `category` (6 opções) |
| Localização específica | ❌ | ✅ `location` (CharField) |

---

## 🧪 Testes Realizados

### Teste 1: Propriedades ✅
```python
equipment = Equipment.objects.first()
print(equipment.public_url)          # http://example.com/log/IdYql...
print(equipment.category_display)    # "Outro"
print(equipment.full_location)       # "Hospital Central - Ala de Emergência"
```

### Teste 2: Validação de Token ✅
```python
# Token válido
eq = Equipment.validate_token('IdYqlTd8wnpiXNz2HlNHWQ')
# Retorna: <Equipment: Desfibrilador Philips HeartStart>

# Token inválido
eq = Equipment.validate_token('token_invalido')
# Retorna: None
```

### Teste 3: Regeneração de Token ✅
```python
old_token = equipment.public_token  # IdYqlTd8wnpiXNz2HlNHWQ
new_token = equipment.regenerate_token()
print(old_token != new_token)  # True
print(equipment.public_url)    # Nova URL com novo token
```

---

## 📝 Migração Aplicada

```bash
✅ apps/equipment/migrations/0004_equipment_category_equipment_description_and_more.py
   - Add field category to equipment
   - Add field description to equipment
   - Add field location to equipment
```

---

## 🎯 Exemplos de Uso no Admin

### 1. Regenerar Token para Equipamento Comprometido

```python
# No Django Admin, criar action customizada
from django.contrib import admin

@admin.action(description='Regenerar tokens selecionados')
def regenerate_tokens(modeladmin, request, queryset):
    for equipment in queryset:
        old_token = equipment.public_token
        new_token = equipment.regenerate_token()
        modeladmin.message_user(
            request,
            f"{equipment.name}: {old_token[:8]}... → {new_token[:8]}..."
        )

class EquipmentAdmin(admin.ModelAdmin):
    actions = [regenerate_tokens]
```

### 2. Exibir Localização Completa

```python
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'serial_number', 'full_location', 'category_display', 'is_active']
```

### 3. Exibir QR Code e URL

```python
class EquipmentAdmin(admin.ModelAdmin):
    readonly_fields = ['public_url', 'qr_code_preview']

    def qr_code_preview(self, obj):
        if obj.qr_code:
            return format_html(
                '<img src="{}" width="200"><br><a href="{}">{}</a>',
                obj.qr_code.url,
                obj.public_url,
                obj.public_url
            )
        return "No QR code"
    qr_code_preview.short_description = "QR Code"
```

---

## 🔒 Boas Práticas de Segurança

### 1. Rotação Periódica de Tokens
```python
# Management command: rotate_tokens.py
from django.core.management.base import BaseCommand
from apps.equipment.models import Equipment
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Regenerar tokens de equipamentos não atualizados há 90 dias
        threshold = timezone.now() - timedelta(days=90)
        old_equipment = Equipment.objects.filter(updated_at__lt=threshold)

        for eq in old_equipment:
            eq.regenerate_token()
            self.stdout.write(f"✅ {eq.name}: Token regenerado")
```

### 2. Logging de Acessos
```python
# Adicionar em CleaningLog.save()
import logging
logger = logging.getLogger('security')

logger.info(
    f"QR cleaning registered - Equipment: {self.equipment.id}, "
    f"Token: {self.equipment.public_token[:8]}..., "
    f"IP: {request.META.get('REMOTE_ADDR')}"
)
```

### 3. Rate Limiting por Token
```python
# Implementar cache para prevenir spam
from django.core.cache import cache

def check_rate_limit(token):
    cache_key = f"qr_access:{token}"
    count = cache.get(cache_key, 0)

    if count > 10:  # Max 10 acessos por minuto
        return False

    cache.set(cache_key, count + 1, 60)  # Expira em 60s
    return True
```

---

## 📚 Documentação de Referência

### Arquivos Modificados
- ✅ `apps/equipment/models.py` - Modelo completo atualizado
- ✅ `apps/cleaning_logs/views.py` - Usa `Equipment.validate_token()`
- ✅ `apps/equipment/migrations/0004_*.py` - Migração aplicada

### Arquivos Criados
- ✅ `EQUIPMENT_MODEL_IMPROVEMENTS.md` - Este documento

### Próximos Passos Sugeridos
1. Atualizar Django Admin com novos campos
2. Criar management command para rotação de tokens
3. Adicionar rate limiting por token
4. Implementar logging de acessos por QR code
5. Criar dashboard de estatísticas por equipamento

---

## 🎉 Status

**🟢 TODAS AS MELHORIAS IMPLEMENTADAS E TESTADAS**

- [x] Campos adicionais (descrição, categoria, localização)
- [x] Propriedade `public_url` (HTTPS em produção)
- [x] Propriedade `category_display`
- [x] Propriedade `full_location`
- [x] Método `generate_qr_code()` melhorado
- [x] Método `regenerate_token()`
- [x] Método `validate_token()` (class method)
- [x] Método `revoke_access()`
- [x] Migração aplicada com sucesso
- [x] Testes realizados e passando
- [x] Documentação completa

**Data**: 21/11/2025
**Versão**: 2.0
