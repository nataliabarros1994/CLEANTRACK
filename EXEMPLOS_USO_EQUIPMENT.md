# 📖 Exemplos Práticos de Uso - Equipment Model

## 🎯 Guia Rápido de Uso

Este documento contém exemplos práticos e casos de uso reais para o modelo Equipment melhorado.

---

## 1️⃣ Criar e Configurar Equipamento

### Exemplo Básico
```python
from apps.equipment.models import Equipment
from apps.facilities.models import Facility

# Criar equipamento completo
equipment = Equipment.objects.create(
    facility=Facility.objects.first(),
    name="Ultrassom GE LOGIQ E9",
    serial_number="ULT-2024-001",
    description="Ultrassom de última geração com Doppler colorido",
    category="diagnostic",
    location="Sala 203, Ala de Imagem",
    cleaning_frequency_hours=8,
    is_active=True
)

# Token e QR code são gerados automaticamente!
print(f"Token gerado: {equipment.public_token}")
print(f"URL: {equipment.public_url}")
print(f"QR Code: {equipment.qr_code.url if equipment.qr_code else 'Gerando...'}")
```

### Exemplo com Categorias
```python
# Criar equipamentos de diferentes categorias
equipments = [
    {
        'name': 'Monitor Cardíaco Philips',
        'serial_number': 'MON-001',
        'category': 'monitoring',
        'location': 'UTI - Leito 5'
    },
    {
        'name': 'Ventilador Pulmonar Dräger',
        'serial_number': 'VEN-001',
        'category': 'life_support',
        'location': 'UTI - Leito 3'
    },
    {
        'name': 'Bisturi Elétrico Valleylab',
        'serial_number': 'BIS-001',
        'category': 'surgical',
        'location': 'Centro Cirúrgico - Sala 1'
    }
]

facility = Facility.objects.first()
for eq_data in equipments:
    Equipment.objects.create(facility=facility, **eq_data)
    print(f"✅ Criado: {eq_data['name']}")
```

---

## 2️⃣ Validar Tokens e Processar Registros

### Na View (Exemplo Real)
```python
from django.http import JsonResponse
from apps.equipment.models import Equipment

def process_qr_cleaning(request, token):
    # Validar token (método seguro)
    equipment = Equipment.validate_token(token)

    if not equipment:
        return JsonResponse({
            'error': 'Token inválido ou equipamento inativo'
        }, status=404)

    # Processar limpeza
    photo = request.FILES.get('photo')
    notes = request.POST.get('notes', '')

    cleaning_log = CleaningLog.objects.create(
        equipment=equipment,
        photo=photo,
        notes=notes,
        cleaned_at=timezone.now()
    )

    return JsonResponse({
        'success': True,
        'equipment': equipment.name,
        'location': equipment.full_location,
        'message': f'Limpeza registrada para {equipment.name}'
    })
```

### Script de Validação em Massa
```python
# Validar múltiplos tokens
tokens = [
    '2r7Zgna2fTpX2-5LoYCE2w',
    'IdYqlTd8wnpiXNz2HlNHWQ',
    'token_invalido_123',
]

results = []
for token in tokens:
    equipment = Equipment.validate_token(token)
    results.append({
        'token': token[:8] + '...',
        'valid': equipment is not None,
        'equipment': equipment.name if equipment else None
    })

# Exibir resultados
for result in results:
    status = "✅" if result['valid'] else "❌"
    print(f"{status} {result['token']} - {result['equipment'] or 'INVÁLIDO'}")
```

---

## 3️⃣ Regenerar Tokens (Segurança)

### Caso 1: QR Code Comprometido
```python
# QR code foi fotografado e compartilhado indevidamente
equipment = Equipment.objects.get(serial_number='ULT-2024-001')

print(f"Token antigo: {equipment.public_token}")
print(f"URL antiga: {equipment.public_url}")

# Regenerar token e QR code
new_token = equipment.regenerate_token()

print(f"\n🔄 Token regenerado!")
print(f"Token novo: {new_token}")
print(f"URL nova: {equipment.public_url}")
print("\n⚠️ AÇÃO: Reimprimir QR code e substituir no equipamento")
```

### Caso 2: Rotação Periódica (Management Command)
```python
# apps/equipment/management/commands/rotate_old_tokens.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.equipment.models import Equipment

class Command(BaseCommand):
    help = 'Rotacionar tokens de equipamentos não atualizados há 90 dias'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=90,
            help='Número de dias para considerar token "antigo"'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular sem aplicar mudanças'
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']

        threshold = timezone.now() - timedelta(days=days)
        old_equipment = Equipment.objects.filter(
            updated_at__lt=threshold,
            is_active=True
        )

        count = old_equipment.count()
        self.stdout.write(f"🔍 Encontrados {count} equipamentos com tokens antigos")

        if dry_run:
            for eq in old_equipment:
                self.stdout.write(f"   - {eq.name} (atualizado: {eq.updated_at.date()})")
            self.stdout.write(self.style.WARNING("\n⚠️ DRY RUN - Nenhuma mudança aplicada"))
            return

        # Regenerar tokens
        for eq in old_equipment:
            old_token = eq.public_token[:8]
            new_token = eq.regenerate_token()
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ {eq.name}: {old_token}... → {new_token[:8]}..."
                )
            )

        self.stdout.write(self.style.SUCCESS(f"\n✅ {count} tokens regenerados"))
```

**Uso:**
```bash
# Simular (dry run)
python manage.py rotate_old_tokens --dry-run

# Aplicar para tokens com 60+ dias
python manage.py rotate_old_tokens --days=60

# Aplicar para tokens com 90+ dias (padrão)
python manage.py rotate_old_tokens
```

---

## 4️⃣ Revogar Acesso

### Caso 1: Equipamento em Manutenção
```python
# Equipamento será enviado para manutenção externa
equipment = Equipment.objects.get(serial_number='ULT-2024-001')

# Revogar acesso temporariamente
equipment.revoke_access()

print(f"🚫 Acesso revogado para: {equipment.name}")
print(f"Status: {'Ativo' if equipment.is_active else 'Inativo'}")

# Agora validate_token retorna None
result = Equipment.validate_token(equipment.public_token)
print(f"Token válido: {result is not None}")  # False
```

### Caso 2: Reativar Após Manutenção
```python
# Equipamento voltou da manutenção
equipment = Equipment.objects.get(serial_number='ULT-2024-001')

# Reativar equipamento
equipment.is_active = True
equipment.save()

# IMPORTANTE: Regenerar token por segurança
equipment.regenerate_token()

print(f"✅ Equipamento reativado: {equipment.name}")
print(f"🔄 Novo token: {equipment.public_token}")
print("\n⚠️ AÇÃO: Gerar e colar novo QR code")
```

---

## 5️⃣ Gerar QR Codes Personalizados

### Diferentes Tamanhos e Qualidades
```python
equipment = Equipment.objects.get(serial_number='ULT-2024-001')

# Padrão: Alta qualidade (H), tamanho 10
equipment.generate_qr_code()

# QR code GRANDE para impressão em banner
equipment.generate_qr_code(size=15, border=6, error_correction='H')

# QR code MÉDIO para etiquetas padrão
equipment.generate_qr_code(size=10, border=4, error_correction='H')

# QR code PEQUENO (menor tamanho de arquivo)
equipment.generate_qr_code(size=8, border=3, error_correction='M')

print(f"QR Code gerado: {equipment.qr_code.url}")
print(f"Tamanho do arquivo: {equipment.qr_code.size / 1024:.1f} KB")
```

### Regenerar QR Codes em Massa
```python
# Regenerar QR codes de todos equipamentos ativos
equipments = Equipment.objects.filter(is_active=True)

for eq in equipments:
    eq.generate_qr_code(size=12, error_correction='H')
    eq.save(update_fields=['qr_code'])
    print(f"✅ QR regenerado: {eq.name}")

print(f"\n✅ Total: {equipments.count()} QR codes regenerados")
```

---

## 6️⃣ Consultas e Relatórios

### Equipamentos por Categoria
```python
from django.db.models import Count

# Contar por categoria
categories = Equipment.objects.values('category').annotate(
    total=Count('id')
).order_by('-total')

print("📊 Equipamentos por Categoria:\n")
for cat in categories:
    category_name = dict(Equipment.EQUIPMENT_CATEGORIES).get(cat['category'], 'Outro')
    print(f"  {category_name}: {cat['total']}")
```

### Equipamentos por Localização
```python
# Listar equipamentos com localização específica
located = Equipment.objects.exclude(location='').select_related('facility')

print("📍 Equipamentos com Localização Específica:\n")
for eq in located:
    print(f"  • {eq.name}")
    print(f"    Localização: {eq.full_location}")
    print()
```

### Equipamentos Vencidos (Overdue)
```python
# Encontrar equipamentos que precisam limpeza urgente
from django.utils import timezone

overdue_equipment = [eq for eq in Equipment.objects.all() if eq.is_overdue]

print(f"🚨 {len(overdue_equipment)} equipamentos precisam limpeza:\n")
for eq in overdue_equipment:
    last = eq.last_cleaning
    if last:
        days = (timezone.now() - last.cleaned_at).days
        print(f"  • {eq.name}")
        print(f"    Última limpeza: {days} dias atrás")
        print(f"    QR Code: {eq.public_url}")
    else:
        print(f"  • {eq.name}")
        print(f"    Última limpeza: NUNCA")
        print(f"    QR Code: {eq.public_url}")
    print()
```

---

## 7️⃣ Integração com Admin

### Admin Customizado Completo
```python
# apps/equipment/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Equipment

@admin.action(description='🔄 Regenerar tokens selecionados')
def regenerate_tokens_action(modeladmin, request, queryset):
    count = 0
    for equipment in queryset:
        old = equipment.public_token[:8]
        new = equipment.regenerate_token()
        modeladmin.message_user(
            request,
            f"{equipment.name}: {old}... → {new[:8]}..."
        )
        count += 1
    modeladmin.message_user(request, f"✅ {count} tokens regenerados")

@admin.action(description='🖨️ Regenerar QR codes selecionados')
def regenerate_qr_codes_action(modeladmin, request, queryset):
    for equipment in queryset:
        equipment.generate_qr_code(size=12, error_correction='H')
        equipment.save(update_fields=['qr_code'])
    modeladmin.message_user(request, f"✅ {queryset.count()} QR codes regenerados")

@admin.action(description='🚫 Revogar acesso dos selecionados')
def revoke_access_action(modeladmin, request, queryset):
    count = queryset.update(is_active=False)
    modeladmin.message_user(request, f"🚫 {count} equipamentos desativados")

class EquipmentAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'serial_number',
        'category_display_colored',
        'full_location',
        'status_badge',
        'qr_link'
    ]
    list_filter = ['category', 'is_active', 'facility', 'cleaning_frequency_hours']
    search_fields = ['name', 'serial_number', 'description', 'location']
    readonly_fields = ['public_token', 'public_url', 'qr_code_preview', 'created_at', 'updated_at']
    actions = [regenerate_tokens_action, regenerate_qr_codes_action, revoke_access_action]

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('facility', 'name', 'serial_number', 'description')
        }),
        ('Classificação', {
            'fields': ('category', 'location')
        }),
        ('Configuração de Limpeza', {
            'fields': ('cleaning_frequency_hours', 'is_active')
        }),
        ('QR Code & Token', {
            'fields': ('public_token', 'public_url', 'qr_code_preview'),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def category_display_colored(self, obj):
        colors = {
            'diagnostic': '#2196F3',
            'monitoring': '#4CAF50',
            'life_support': '#F44336',
            'surgical': '#FF9800',
            'laboratory': '#9C27B0',
            'other': '#757575',
        }
        color = colors.get(obj.category, '#757575')
        return format_html(
            '<span style="color: {}; font-weight: bold;">●</span> {}',
            color,
            obj.category_display
        )
    category_display_colored.short_description = 'Categoria'

    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✅ Ativo</span>')
        return format_html('<span style="color: red;">❌ Inativo</span>')
    status_badge.short_description = 'Status'

    def qr_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank">🔗 Abrir</a>',
            obj.public_url
        )
    qr_link.short_description = 'QR Link'

    def qr_code_preview(self, obj):
        if obj.qr_code:
            return format_html(
                '<div style="text-align: center;">'
                '<img src="{}" width="250" style="border: 2px solid #ddd; padding: 10px;"><br>'
                '<strong>URL:</strong> <a href="{}" target="_blank">{}</a><br>'
                '<strong>Token:</strong> <code>{}</code>'
                '</div>',
                obj.qr_code.url,
                obj.public_url,
                obj.public_url,
                obj.public_token
            )
        return "QR Code não gerado"
    qr_code_preview.short_description = "QR Code"

admin.site.register(Equipment, EquipmentAdmin)
```

---

## 8️⃣ API REST (Exemplo com DRF)

### Serializer
```python
# apps/equipment/serializers.py
from rest_framework import serializers
from .models import Equipment

class EquipmentSerializer(serializers.ModelSerializer):
    public_url = serializers.ReadOnlyField()
    category_display = serializers.ReadOnlyField()
    full_location = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()

    class Meta:
        model = Equipment
        fields = [
            'id',
            'name',
            'serial_number',
            'description',
            'category',
            'category_display',
            'location',
            'full_location',
            'cleaning_frequency_hours',
            'is_active',
            'public_url',
            'qr_code',
            'is_overdue',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['public_token', 'qr_code', 'created_at', 'updated_at']
```

### ViewSet
```python
# apps/equipment/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Equipment
from .serializers import EquipmentSerializer

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    @action(detail=True, methods=['post'])
    def regenerate_token(self, request, pk=None):
        """Regenerar token do equipamento"""
        equipment = self.get_object()
        new_token = equipment.regenerate_token()
        return Response({
            'success': True,
            'message': f'Token regenerado para {equipment.name}',
            'new_token': new_token,
            'new_url': equipment.public_url
        })

    @action(detail=True, methods=['post'])
    def revoke(self, request, pk=None):
        """Revogar acesso ao equipamento"""
        equipment = self.get_object()
        equipment.revoke_access()
        return Response({
            'success': True,
            'message': f'Acesso revogado para {equipment.name}'
        })

    @action(detail=False, methods=['post'])
    def validate_token(self, request):
        """Validar um token"""
        token = request.data.get('token')
        equipment = Equipment.validate_token(token)

        if equipment:
            return Response({
                'valid': True,
                'equipment': EquipmentSerializer(equipment).data
            })
        return Response({
            'valid': False,
            'message': 'Token inválido ou equipamento inativo'
        }, status=status.HTTP_404_NOT_FOUND)
```

---

## 🎯 Resumo dos Casos de Uso

| Caso de Uso | Método/Propriedade | Exemplo |
|-------------|-------------------|---------|
| Obter URL pública | `equipment.public_url` | `http://app.com/log/token123/` |
| Validar token | `Equipment.validate_token(token)` | Retorna equipment ou None |
| Regenerar token | `equipment.regenerate_token()` | Retorna novo token |
| Revogar acesso | `equipment.revoke_access()` | Desativa equipamento |
| Gerar QR customizado | `equipment.generate_qr_code(size=12)` | QR maior/menor |
| Localização completa | `equipment.full_location` | "Hospital - Sala 101" |
| Nome categoria | `equipment.category_display` | "Diagnóstico" |
| Verificar vencimento | `equipment.is_overdue` | True/False |

---

## 📚 Referências

- [EQUIPMENT_MODEL_IMPROVEMENTS.md](EQUIPMENT_MODEL_IMPROVEMENTS.md) - Documentação técnica completa
- [PERMANENT_TOKENS_IMPLEMENTATION.md](PERMANENT_TOKENS_IMPLEMENTATION.md) - Implementação de tokens
- [Django Documentation](https://docs.djangoproject.com/) - Framework Django

---

**Data**: 21/11/2025
**Autor**: Claude Code
**Status**: ✅ Pronto para uso
