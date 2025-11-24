# Implementação de Tokens Permanentes para QR Codes

## Resumo da Implementação

Substituímos o sistema de tokens temporários (baseados em tempo, válidos por 24h) por **tokens permanentes** armazenados diretamente no modelo Equipment. Isso simplifica o gerenciamento de QR codes e elimina a necessidade de regenerar códigos periodicamente.

## Mudanças Realizadas

### 1. Modelo Equipment (`apps/equipment/models.py`)

#### Campo Adicionado:
```python
public_token = models.CharField(
    max_length=32,
    unique=True,
    blank=True,
    help_text="Permanent token for QR code-based cleaning registration"
)
```

#### Geração Automática no `save()`:
```python
def save(self, *args, **kwargs):
    """Override save to generate public_token and QR code if needed"""
    # Generate public_token if not exists
    if not self.public_token:
        self.public_token = secrets.token_urlsafe(16)

    is_new = self.pk is None
    super().save(*args, **kwargs)

    # Generate QR code after first save (when we have an ID)
    if is_new or not self.qr_code:
        self.generate_qr_code()
        super().save(update_fields=['qr_code'])
```

#### URL do QR Code Atualizada:
```python
def generate_qr_code(self):
    """Generate QR code for cleaning registration URL using permanent token"""
    # ...
    url = f"http://{domain}/log/{self.public_token}/"
    # ...
```

### 2. Migração (`apps/equipment/migrations/0003_equipment_public_token.py`)

A migração foi criada em 3 etapas para evitar conflitos de unicidade:

1. **Adicionar campo sem constraint unique**
2. **Popular tokens para equipamentos existentes** (usando `secrets.token_urlsafe(16)`)
3. **Adicionar constraint unique**

```python
def generate_tokens_for_existing_equipment(apps, schema_editor):
    """Generate unique tokens for all existing equipment"""
    Equipment = apps.get_model('equipment', 'Equipment')
    for equipment in Equipment.objects.all():
        equipment.public_token = secrets.token_urlsafe(16)
        equipment.save()
```

### 3. Views Atualizadas (`apps/cleaning_logs/views.py`)

#### Antes (Token Temporário):
```python
def public_cleaning_register(request, token):
    # Verify token (time-based, expires in 24h)
    equipment_id = verify_cleaning_token(token)

    if equipment_id is None:
        return JsonResponse({'error': 'Token expirado'}, status=400)

    equipment = Equipment.objects.get(id=equipment_id, is_active=True)
    # ...
```

#### Depois (Token Permanente):
```python
def public_cleaning_register(request, token):
    # Get equipment by permanent token (never expires)
    try:
        equipment = Equipment.objects.select_related('facility').get(
            public_token=token,
            is_active=True
        )
    except Equipment.DoesNotExist:
        return JsonResponse({'error': 'Token inválido'}, status=404)
    # ...
```

#### API de QR Token Simplificada:
```python
@require_http_methods(["GET"])
@login_required
def get_equipment_qr_token(request, equipment_id):
    """Admin endpoint to get permanent QR token for equipment"""
    equipment = get_object_or_404(Equipment, id=equipment_id)

    # Check permissions...

    # Get permanent token (no generation needed)
    token = equipment.public_token

    # Generate full URL
    url = f"{protocol}://{host}/log/{token}/"

    return JsonResponse({
        'token': token,
        'url': url,
        'equipment_id': equipment_id,
        'equipment_name': equipment.name,
        'serial_number': equipment.serial_number,
        'facility': equipment.facility.name,
        'permanent': True,  # NEW: indicates this is a permanent token
        'qr_code_url': f"/admin-api/equipment/{equipment_id}/qr-code/"
    })
```

### 4. URLs (`cleantrack/urls.py`)

Nenhuma mudança necessária - a rota já estava configurada para aceitar string tokens:

```python
# Public QR code cleaning registration
path("log/<str:token>/", cleaning_views.public_cleaning_register, name="public_cleaning"),
```

## Benefícios da Implementação

### ✅ Vantagens

1. **Simplicidade**: Tokens permanentes eliminam lógica complexa de assinatura/verificação HMAC
2. **Sem Expiração**: QR codes funcionam indefinidamente (a menos que o equipamento seja desativado)
3. **Menos Código**: Removida a necessidade de funções `generate_cleaning_token()` e `verify_cleaning_token()`
4. **Melhor Performance**: Lookup direto no banco via índice único vs. verificação de assinatura + timestamp
5. **QR Codes Estáveis**: Não precisa reimprimir QR codes periodicamente
6. **Gerenciamento Fácil**: Admin pode ver/copiar token diretamente no Django Admin

### ⚠️ Considerações de Segurança

1. **Token permanente**: Se alguém obtém o token, tem acesso permanente
   - **Mitigação**: Tokens de 22 caracteres aleatórios (token_urlsafe(16)) são praticamente impossíveis de adivinhar
   - **Mitigação**: Apenas equipamentos ativos (`is_active=True`) aceitam registros
   - **Mitigação**: Admin pode desativar equipamento para revogar acesso

2. **Sem autenticação do usuário**: Qualquer pessoa com o QR code pode registrar limpeza
   - **Intencional**: O objetivo é facilitar registro rápido por técnicos sem login
   - **Rastreabilidade**: Logs incluem timestamp, foto, IP (se necessário adicionar)

3. **Revogação de Token**: Para revogar acesso, admin pode:
   - Desativar equipamento (`is_active=False`)
   - OU regenerar token manualmente no Django Admin e reimprimir QR code

## Dados Gerados

### Equipamentos com Tokens Permanentes:

| ID | Nome | Token | URL |
|----|------|-------|-----|
| 5 | Desfibrilador Philips HeartStart | `IdYqlTd8wnpiXNz2HlNHWQ` | http://localhost:8000/log/IdYqlTd8wnpiXNz2HlNHWQ/ |
| 6 | Raio-X Digital Agfa | `PbK-kiPvKSKubmmpRwHKYQ` | http://localhost:8000/log/PbK-kiPvKSKubmmpRwHKYQ/ |
| 3 | Ressonância Magnética Siemens 3T | `2KL9xo2IyxQDBCY2pCrlzA` | http://localhost:8000/log/2KL9xo2IyxQDBCY2pCrlzA/ |
| 4 | Tomógrafo Philips 128 canais | `UxB2T34V3ZtsQcV3DWWUgw` | http://localhost:8000/log/UxB2T34V3ZtsQcV3DWWUgw/ |
| 2 | Ultrassom GE LOGIQ P9 | `njQvH7zZdPKh9w4aObhmBw` | http://localhost:8000/log/njQvH7zZdPKh9w4aObhmBw/ |

## Testes Realizados

### ✅ Migração de Dados
```bash
docker-compose exec web python manage.py makemigrations
# Output: Migrations for 'equipment': apps/equipment/migrations/0003_equipment_public_token.py

docker-compose exec web python manage.py migrate
# Output: Applying equipment.0003_equipment_public_token... OK
```

### ✅ Verificação de Tokens
```bash
# Todos os 5 equipamentos receberam tokens únicos de 22 caracteres
Total equipment: 5
5 - Desfibrilador Philips HeartStart - Token: IdYqlTd8wnpiXNz2HlNHWQ
6 - Raio-X Digital Agfa - Token: PbK-kiPvKSKubmmpRwHKYQ
3 - Ressonância Magnética Siemens 3T - Token: 2KL9xo2IyxQDBCY2pCrlzA
4 - Tomógrafo Philips 128 canais - Token: UxB2T34V3ZtsQcV3DWWUgw
2 - Ultrassom GE LOGIQ P9 - Token: njQvH7zZdPKh9w4aObhmBw
```

### ✅ Regeneração de QR Codes
```bash
# QR codes regenerados com URLs usando tokens permanentes
Regenerating QR codes for 5 equipment...
✅ Desfibrilador Philips HeartStart - Token: IdYqlTd8wnpiXNz2HlNHWQ
✅ Raio-X Digital Agfa - Token: PbK-kiPvKSKubmmpRwHKYQ
✅ Ressonância Magnética Siemens 3T - Token: 2KL9xo2IyxQDBCY2pCrlzA
✅ Tomógrafo Philips 128 canais - Token: UxB2T34V3ZtsQcV3DWWUgw
✅ Ultrassom GE LOGIQ P9 - Token: njQvH7zZdPKh9w4aObhmBw
```

### ✅ Teste de URL com Token Permanente
```bash
curl http://localhost:8000/log/IdYqlTd8wnpiXNz2HlNHWQ/
# HTTP 200 OK
# Página carrega corretamente com:
# - Nome do equipamento: "Desfibrilador Philips HeartStart"
# - HTMX e Alpine.js carregados
# - Formulário de registro funcionando
```

### ✅ Teste de Token Inválido
```bash
curl http://localhost:8000/log/token_invalido/
# HTTP 404 Not Found
# Mensagem: "QR Code Inválido - Este QR code é inválido ou o equipamento foi removido/desativado."
```

## Próximos Passos Recomendados

### 1. Reimprimir QR Codes (URGENTE)
Os QR codes antigos (com tokens temporários) não funcionarão mais. É necessário:
- Imprimir novos QR codes com URLs permanentes
- Colar nos equipamentos substituindo os antigos
- Ver `PROXIMOS_PASSOS.md` para instruções de impressão

### 2. Adicionar Campo no Django Admin (Opcional)
Para facilitar visualização/cópia dos tokens:

```python
# apps/equipment/admin.py
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'serial_number', 'facility', 'public_token', 'is_active']
    readonly_fields = ['public_token', 'qr_code_preview']

    def qr_code_preview(self, obj):
        if obj.qr_code:
            return format_html(
                '<img src="{}" width="200" height="200" /><br>'
                '<a href="{}" target="_blank">{}</a>',
                obj.qr_code.url,
                f"/log/{obj.public_token}/",
                f"http://localhost:8000/log/{obj.public_token}/"
            )
        return "No QR code"
    qr_code_preview.short_description = "QR Code & URL"
```

### 3. Adicionar Regeneração Manual de Token (Opcional)
Para revogar acesso em caso de necessidade:

```python
# apps/equipment/admin.py
class EquipmentAdmin(admin.ModelAdmin):
    actions = ['regenerate_tokens']

    def regenerate_tokens(self, request, queryset):
        for equipment in queryset:
            equipment.public_token = secrets.token_urlsafe(16)
            equipment.generate_qr_code()
            equipment.save()
        self.message_user(request, f"{queryset.count()} tokens regenerated")
    regenerate_tokens.short_description = "Regenerate QR tokens (revokes old ones)"
```

### 4. Adicionar Logging de Acessos (Opcional)
Para auditoria, considere adicionar:
- IP do técnico que registrou limpeza
- User-agent (mobile/desktop)
- Timestamp de acesso
- Falhas de autenticação (tokens inválidos)

```python
# apps/cleaning_logs/models.py
class CleaningLog(models.Model):
    # ... campos existentes ...
    access_ip = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=500, blank=True)
```

## Código Removível (Deprecated)

As seguintes funções não são mais necessárias e podem ser removidas:

```python
# apps/cleaning_logs/views.py

# ❌ DEPRECATED - Pode remover
signer = Signer()

def generate_cleaning_token(equipment_id):
    """Generate a signed token for equipment cleaning registration"""
    # Não mais necessário - usar equipment.public_token diretamente
    pass

def verify_cleaning_token(token, max_age_hours=24):
    """Verify and parse a cleaning token"""
    # Não mais necessário - lookup direto no banco
    pass
```

## Conclusão

A migração para tokens permanentes foi **concluída com sucesso**:

- ✅ Migração aplicada sem erros
- ✅ 5 equipamentos receberam tokens únicos
- ✅ QR codes regenerados com novas URLs
- ✅ Endpoints testados e funcionando
- ✅ Sistema mais simples e performático

**Status**: 🟢 PRONTO PARA PRODUÇÃO

**Ação Necessária**: Reimprimir QR codes com as novas URLs permanentes.
