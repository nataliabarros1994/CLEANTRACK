# 📱 Guia de Geração de QR Codes

## 🎯 Visão Geral

Este guia documenta como usar o script `utils/generate_qr.py` para gerar QR codes para equipamentos.

---

## 📦 Instalação

O script já está incluído no projeto. Não é necessária instalação adicional.

**Dependências:**
- ✅ `qrcode` (já instalado)
- ✅ `PIL/Pillow` (já instalado)
- ✅ Django (já instalado)

---

## 🚀 Uso Básico

### 1. Gerar QR Code para Um Equipamento

```python
# Abrir Django shell
docker-compose exec web python manage.py shell

# Importar função
from utils.generate_qr import generate_qr_for_equipment

# Gerar QR code
filepath = generate_qr_for_equipment(1)
# ✅ QR code gerado para: Desfibrilador Philips HeartStart
#    URL: http://localhost:8000/log/2r7Zgna2fTpX2-5LoYCE2w/
#    Arquivo: /app/media/qrcodes/eq_1.png
```

### 2. Gerar QR Codes para Todos os Equipamentos

```python
from utils.generate_qr import generate_qr_for_all_equipment

# Gerar para todos equipamentos ativos
paths = generate_qr_for_all_equipment()
# Gerando QR codes para 5 equipamentos...
# ✅ Total: 5 QR codes gerados com sucesso!

print(f"{len(paths)} arquivos criados")
```

### 3. Gerar QR Code Customizado

```python
from utils.generate_qr import generate_qr_with_custom_settings

# QR grande para impressão (banner)
filepath = generate_qr_with_custom_settings(
    equipment_id=1,
    base_url='https://app.cleantrack.com',
    size=15,
    border=3,
    error_correction='H'
)
```

### 4. Obter Informações do QR Code

```python
from utils.generate_qr import get_qr_info

# Obter informações
info = get_qr_info(1)

print(info['url'])          # URL do QR code
print(info['token'])        # Token do equipamento
print(info['qr_file'])      # Caminho do arquivo
```

---

## 📚 Referência de Funções

### `generate_qr_for_equipment(equipment_id, base_url)`

Gera QR code padrão para um equipamento.

**Parâmetros:**
- `equipment_id` (int): ID do equipamento
- `base_url` (str, opcional): URL base (padrão: `http://localhost:8000`)

**Retorna:**
- `str`: Caminho do arquivo gerado

**Exemplo:**
```python
filepath = generate_qr_for_equipment(1)
# Retorna: '/app/media/qrcodes/eq_1.png'
```

---

### `generate_qr_for_all_equipment(base_url)`

Gera QR codes para todos equipamentos ativos.

**Parâmetros:**
- `base_url` (str, opcional): URL base (padrão: `http://localhost:8000`)

**Retorna:**
- `list`: Lista de caminhos dos arquivos gerados

**Exemplo:**
```python
paths = generate_qr_for_all_equipment()
# Retorna: ['/app/media/qrcodes/eq_1.png', '/app/media/qrcodes/eq_2.png', ...]
```

---

### `generate_qr_with_custom_settings(equipment_id, base_url, size, border, error_correction)`

Gera QR code com configurações personalizadas.

**Parâmetros:**
- `equipment_id` (int): ID do equipamento
- `base_url` (str, opcional): URL base
- `size` (int, opcional): Tamanho do box (padrão: 10)
- `border` (int, opcional): Tamanho da borda (padrão: 5)
- `error_correction` (str, opcional): Nível de correção ('L', 'M', 'Q', 'H')

**Níveis de Correção:**
| Nível | Correção | Uso Recomendado |
|-------|----------|-----------------|
| `L` | 7% | QR limpo, ambiente controlado |
| `M` | 15% | Uso geral |
| `Q` | 25% | Ambiente com sujeira leve |
| `H` | 30% | Máxima durabilidade (padrão) |

**Retorna:**
- `str`: Caminho do arquivo gerado

**Exemplo:**
```python
# QR grande para banner
filepath = generate_qr_with_custom_settings(1, size=20, border=2, error_correction='H')

# QR pequeno para etiqueta
filepath = generate_qr_with_custom_settings(1, size=8, border=3, error_correction='M')
```

---

### `get_qr_info(equipment_id)`

Obtém informações do QR code de um equipamento.

**Parâmetros:**
- `equipment_id` (int): ID do equipamento

**Retorna:**
- `dict`: Dicionário com informações

**Estrutura do retorno:**
```python
{
    'equipment_id': 1,
    'equipment_name': 'Desfibrilador Philips HeartStart',
    'serial_number': 'DF-PHILIPS-2024-001',
    'facility': 'Hospital Central',
    'token': '2r7Zgna2fTpX2-5LoYCE2w',
    'url': 'http://localhost:8000/log/2r7Zgna2fTpX2-5LoYCE2w/',
    'qr_file': '/app/media/qrcodes/eq_1.png'
}
```

---

## 📋 Casos de Uso

### Caso 1: Gerar QR para Novo Equipamento

```python
# Após criar equipamento no admin
from utils.generate_qr import generate_qr_for_equipment

# Gerar QR para produção
filepath = generate_qr_for_equipment(
    equipment_id=10,
    base_url='https://app.cleantrack.com'
)

print(f"QR code salvo em: {filepath}")
# Imprimir e colar no equipamento
```

### Caso 2: Regenerar QR Após Trocar Token

```python
from apps.equipment.models import Equipment
from utils.generate_qr import generate_qr_for_equipment

# Regenerar token do equipamento
equipment = Equipment.objects.get(id=5)
equipment.regenerate_token()

# Gerar novo QR code
filepath = generate_qr_for_equipment(5)
print("⚠️ AÇÃO: Reimprimir e substituir QR code no equipamento")
```

### Caso 3: Gerar QR para Impressão em Diferentes Tamanhos

```python
from utils.generate_qr import generate_qr_with_custom_settings

equipment_id = 1

# Etiqueta pequena (5x5cm)
generate_qr_with_custom_settings(equipment_id, size=8, border=3)

# Etiqueta média (10x10cm)
generate_qr_with_custom_settings(equipment_id, size=12, border=4)

# Banner grande (A4)
generate_qr_with_custom_settings(equipment_id, size=20, border=2)
```

### Caso 4: Migração de Desenvolvimento para Produção

```python
from utils.generate_qr import generate_qr_for_all_equipment

# Desenvolvimento
generate_qr_for_all_equipment(base_url='http://localhost:8000')

# Produção
generate_qr_for_all_equipment(base_url='https://app.cleantrack.com')
```

### Caso 5: Auditoria de QR Codes

```python
from apps.equipment.models import Equipment
from utils.generate_qr import get_qr_info
import os

# Listar todos equipamentos e verificar QR codes
equipments = Equipment.objects.filter(is_active=True)

print("📊 Auditoria de QR Codes\n")
for eq in equipments:
    info = get_qr_info(eq.id)
    qr_exists = os.path.exists(info['qr_file'])
    status = "✅" if qr_exists else "❌"
    print(f"{status} {eq.name}")
    print(f"   Token: {info['token']}")
    print(f"   Arquivo: {'Existe' if qr_exists else 'FALTANDO'}")
    print()
```

---

## 🖨️ Guia de Impressão

### Tamanhos Recomendados

| Uso | Size | Border | Tamanho Final |
|-----|------|--------|---------------|
| **Etiqueta pequena** | 8 | 3 | 5x5 cm |
| **Etiqueta padrão** | 10 | 4 | 7x7 cm |
| **Etiqueta grande** | 12 | 4 | 10x10 cm |
| **Banner/Cartaz** | 20 | 2 | 20x20 cm |

### Configurações de Impressão

```python
# Etiqueta padrão (recomendado)
generate_qr_with_custom_settings(
    equipment_id=1,
    size=10,
    border=4,
    error_correction='H'  # Alta durabilidade
)
```

**Configurações da impressora:**
- Papel: Branco comum ou adesivo
- Qualidade: Alta (mínimo 300 DPI)
- Cores: Preto e branco
- Proteção: Laminação ou plástico transparente

---

## 🔧 Management Command (Opcional)

Você pode criar um management command para facilitar:

```python
# apps/equipment/management/commands/generate_qr_codes.py
from django.core.management.base import BaseCommand
from utils.generate_qr import generate_qr_for_all_equipment

class Command(BaseCommand):
    help = 'Generate QR codes for all equipment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--base-url',
            type=str,
            default='http://localhost:8000',
            help='Base URL for QR codes'
        )

    def handle(self, *args, **options):
        base_url = options['base_url']
        self.stdout.write(f"Gerando QR codes com base URL: {base_url}")

        paths = generate_qr_for_all_equipment(base_url)

        self.stdout.write(
            self.style.SUCCESS(f"✅ {len(paths)} QR codes gerados")
        )
```

**Uso:**
```bash
# Desenvolvimento
docker-compose exec web python manage.py generate_qr_codes

# Produção
docker-compose exec web python manage.py generate_qr_codes --base-url=https://app.cleantrack.com
```

---

## 📂 Estrutura de Arquivos

```
media/
└── qrcodes/
    ├── eq_1.png                        # QR padrão
    ├── eq_2.png
    ├── eq_1_size15_border3_H.png      # QR customizado
    └── ...
```

---

## 🧪 Testes

### Teste 1: Gerar QR Individual ✅
```python
from utils.generate_qr import generate_qr_for_equipment
filepath = generate_qr_for_equipment(5)
# ✅ QR code gerado para: Desfibrilador Philips HeartStart
```

### Teste 2: Gerar QR para Todos ✅
```python
from utils.generate_qr import generate_qr_for_all_equipment
paths = generate_qr_for_all_equipment()
# ✅ Total: 5 QR codes gerados com sucesso!
```

### Teste 3: QR Customizado ✅
```python
from utils.generate_qr import generate_qr_with_custom_settings
filepath = generate_qr_with_custom_settings(5, size=15, border=3, error_correction='H')
# ✅ QR code customizado gerado
```

### Teste 4: Obter Informações ✅
```python
from utils.generate_qr import get_qr_info
info = get_qr_info(5)
print(info['url'])
# http://localhost:8000/log/2r7Zgna2fTpX2-5LoYCE2w/
```

---

## 📊 Exemplo de Output

```
======================================================================
Gerando QR codes para 5 equipamentos...
======================================================================
✅ QR code gerado para: Desfibrilador Philips HeartStart
   URL: http://localhost:8000/log/2r7Zgna2fTpX2-5LoYCE2w/
   Arquivo: /app/media/qrcodes/eq_5.png

✅ QR code gerado para: Raio-X Digital Agfa
   URL: http://localhost:8000/log/PbK-kiPvKSKubmmpRwHKYQ/
   Arquivo: /app/media/qrcodes/eq_6.png

✅ QR code gerado para: Ressonância Magnética Siemens 3T
   URL: http://localhost:8000/log/2KL9xo2IyxQDBCY2pCrlzA/
   Arquivo: /app/media/qrcodes/eq_3.png

✅ QR code gerado para: Tomógrafo Philips 128 canais
   URL: http://localhost:8000/log/UxB2T34V3ZtsQcV3DWWUgw/
   Arquivo: /app/media/qrcodes/eq_4.png

✅ QR code gerado para: Ultrassom GE LOGIQ P9
   URL: http://localhost:8000/log/njQvH7zZdPKh9w4aObhmBw/
   Arquivo: /app/media/qrcodes/eq_2.png

======================================================================
✅ Total: 5 QR codes gerados com sucesso!
```

---

## 🎯 Boas Práticas

1. **Sempre use HTTPS em produção:**
   ```python
   generate_qr_for_equipment(1, base_url='https://app.cleantrack.com')
   ```

2. **Use alta correção de erros para durabilidade:**
   ```python
   error_correction='H'  # 30% de correção
   ```

3. **Proteja QR codes impressos:**
   - Laminação
   - Plástico transparente
   - Evite áreas de alta abrasão

4. **Regenere QR codes após trocar tokens:**
   ```python
   equipment.regenerate_token()
   generate_qr_for_equipment(equipment.id)
   ```

5. **Faça backup dos QR codes:**
   ```bash
   tar -czf qrcodes_backup_$(date +%Y%m%d).tar.gz media/qrcodes/
   ```

---

## 📚 Arquivos Relacionados

- **Script**: `utils/generate_qr.py`
- **Model**: `apps/equipment/models.py`
- **Documentação**: `EQUIPMENT_MODEL_IMPROVEMENTS.md`
- **Guia de uso**: `EXEMPLOS_USO_EQUIPMENT.md`

---

**Data**: 21/11/2025
**Versão**: 1.0
**Status**: ✅ Funcional
