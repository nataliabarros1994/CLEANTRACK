# 🖨️ Impressão de Etiquetas Térmicas - Brother QL-800

## ✅ Script Implementado

Script profissional para impressão de etiquetas térmicas em impressoras Brother QL-800/810/820.

---

## 📋 Características

### Funcionalidades:
- ✅ Impressão direta em impressoras Brother QL
- ✅ QR code de alta qualidade (error correction H)
- ✅ Layout otimizado para etiquetas 29mm x 90mm
- ✅ Informações do equipamento (nome, serial, facility)
- ✅ Suporte a logo CleanTrack (opcional)
- ✅ Preview de etiquetas sem imprimir
- ✅ Detecção automática de impressoras
- ✅ Integração com Django models

### Compatibilidade:
- Brother QL-800
- Brother QL-810
- Brother QL-820

### Tamanhos de Etiqueta Suportados:
- 29mm (padrão)
- 38mm
- 62mm

---

## 🔧 Instalação

### 1. Instalar Dependências

```bash
pip install brother-ql pillow qrcode
```

### 2. Configurar Permissões USB (Linux)

```bash
# Adicionar usuário ao grupo lp (line printer)
sudo usermod -a -G lp $USER

# Reiniciar sessão ou executar:
newgrp lp

# Verificar se impressora está conectada
lsusb | grep Brother
```

**Saída esperada:**
```
Bus 001 Device 005: ID 04f9:2015 Brother Industries, Ltd
```

---

## 📖 Uso

### Comando Básico

```bash
# Imprimir etiqueta para equipamento ID 1
python utils/print_labels.py 1
```

---

### Opções Avançadas

```bash
# Imprimir com impressora específica
python utils/print_labels.py 5 --printer usb://0x04f9:0x2015

# Usar modelo diferente
python utils/print_labels.py 3 --model QL-810

# Usar tamanho de etiqueta diferente
python utils/print_labels.py 7 --size 38

# Especificar URL personalizada
python utils/print_labels.py 2 --url https://cleantrack.seudominio.com

# Listar impressoras disponíveis
python utils/print_labels.py --list

# Gerar preview sem imprimir
python utils/print_labels.py 4 --preview label_4.png
```

---

### Exemplos Práticos

#### Exemplo 1: Impressão Simples
```bash
$ python utils/print_labels.py 1

✅ Etiqueta impressa com sucesso!
   Equipamento: Desfibrilador XYZ
   Serial: DEF-001-2025
   Facility: Hospital Central
   QR URL: http://app.cleantrack.com/log/abc123def456/
   Token válido por: 5 minutos
```

#### Exemplo 2: Listar Impressoras
```bash
$ python utils/print_labels.py --list

🖨️  Impressoras Brother QL encontradas:
   1. usb://0x04f9:0x2015
```

#### Exemplo 3: Preview
```bash
$ python utils/print_labels.py 3 --preview label_preview.png

✅ Preview salvo em: label_preview.png
   Equipamento: Monitor Cardíaco
   Tamanho: 342x1063px (29x90mm)
```

---

## 🎨 Layout da Etiqueta

```
┌────────────────────────────┐
│                            │
│     ┌────────────────┐     │  ← QR Code (280x280px)
│     │                │     │
│     │   [QR CODE]    │     │
│     │                │     │
│     └────────────────┘     │
│                            │
│   Desfibrilador XYZ        │  ← Nome (centralizado)
│                            │
│   SN: DEF-001-2025         │  ← Serial (centralizado)
│                            │
│   Hospital Central         │  ← Facility (centralizado)
│                            │
│ Escaneie para registrar    │  ← Instruções (cinza)
│                            │
│ ─────────────────────────  │  ← Linha separadora
│                            │
│    [CleanTrack Logo]       │  ← Logo (opcional)
│                            │
└────────────────────────────┘
     29mm x 90mm (342x1063px)
```

---

## 🔍 Detalhes Técnicos

### Dimensões e Resolução

| Especificação | Valor |
|---------------|-------|
| **Largura física** | 29mm |
| **Altura física** | 90mm |
| **Resolução** | 300 DPI |
| **Largura (pixels)** | 342px |
| **Altura (pixels)** | 1063px |
| **QR Code** | 280x280px |
| **Rotação** | 90° (impressão correta) |

### QR Code

| Propriedade | Valor |
|-------------|-------|
| **Error correction** | High (H) - 30% |
| **Box size** | 8 |
| **Border** | 2 |
| **Cores** | Preto/Branco |

### Fontes

```python
Nome do equipamento: DejaVuSans-Bold, 28pt
Serial number:       DejaVuSans, 20pt
Facility:            DejaVuSans, 18pt
Instruções:          DejaVuSans, 14pt
```

**Fallback:** Se fontes não disponíveis, usa fonte padrão do Pillow.

---

## 🖼️ Logo Opcional

Para incluir logo CleanTrack nas etiquetas:

### 1. Criar Logo para Impressão Térmica

**Especificações:**
- Formato: PNG com fundo transparente
- Dimensões: 300x90 pixels
- Cores: Preto e branco (impressora térmica)
- Nome: `cleantrack-logo-thermal.png`

### 2. Salvar no Local Correto

```bash
static/logo/cleantrack-logo-thermal.png
```

### 3. Verificar

```bash
ls -lh static/logo/cleantrack-logo-thermal.png
```

O script detecta automaticamente e inclui o logo no rodapé da etiqueta.

---

## 📊 Parâmetros da Função

### `print_equipment_label()`

```python
def print_equipment_label(
    equipment_id,                              # ID do equipamento (obrigatório)
    printer_id='usb://0x04f9:0x2015',         # URI da impressora
    model='QL-800',                            # Modelo da impressora
    label_size='29',                           # Tamanho da etiqueta (mm)
    base_url='http://app.cleantrack.com'      # URL base do sistema
):
```

**Retorna:** `bool` (True se sucesso, False se erro)

---

### `list_printers()`

```python
def list_printers():
    """Lista impressoras Brother QL disponíveis via USB"""
```

**Retorna:** `list` de printer IDs

---

### `save_preview()`

```python
def save_preview(equipment_id, output_path='label_preview.png'):
    """Salva preview da etiqueta sem imprimir"""
```

**Retorna:** `bool` (True se sucesso, False se erro)

---

## 🧪 Testes

### Teste 1: Verificar Impressora Conectada

```bash
# Listar dispositivos USB
lsusb | grep Brother

# Resultado esperado:
# Bus 001 Device 005: ID 04f9:2015 Brother Industries, Ltd
```

---

### Teste 2: Listar Impressoras via Script

```bash
python utils/print_labels.py --list

# Resultado esperado:
# 🖨️  Impressoras Brother QL encontradas:
#    1. usb://0x04f9:0x2015
```

---

### Teste 3: Gerar Preview

```bash
python utils/print_labels.py 1 --preview test_preview.png

# Abrir preview:
xdg-open test_preview.png  # Linux
open test_preview.png       # macOS
```

**Verificar:**
- ✓ QR code legível
- ✓ Nome do equipamento
- ✓ Serial number
- ✓ Nome da facility
- ✓ Instruções de uso

---

### Teste 4: Impressão Real

```bash
# Certifique-se de ter etiquetas na impressora!
python utils/print_labels.py 1

# Resultado esperado:
# ✅ Etiqueta impressa com sucesso!
```

**Verificar:**
- ✓ Etiqueta impressa corretamente
- ✓ QR code escaneável
- ✓ Texto legível
- ✓ Layout centralizado

---

## 🐛 Troubleshooting

### Erro: "No module named 'brother_ql'"

**Solução:**
```bash
pip install brother-ql pillow qrcode
```

---

### Erro: "Permission denied" ao acessar USB

**Solução:**
```bash
# Adicionar usuário ao grupo lp
sudo usermod -a -G lp $USER

# Reiniciar sessão ou:
newgrp lp
```

---

### Erro: "Nenhuma impressora encontrada"

**Diagnóstico:**
```bash
# Verificar se impressora está conectada
lsusb | grep Brother

# Verificar drivers
dpkg -l | grep cups

# Verificar permissões
ls -l /dev/usb/lp*
```

**Solução:**
```bash
# Instalar CUPS (se necessário)
sudo apt-get install cups libcups2-dev

# Reiniciar serviço
sudo systemctl restart cups
```

---

### Erro: "Equipment matching query does not exist"

**Solução:**
```bash
# Verificar se equipamento existe
python manage.py shell
>>> from apps.equipment.models import Equipment
>>> Equipment.objects.filter(id=1).exists()
>>> Equipment.objects.all().values_list('id', 'name')
```

---

### Erro: Font "DejaVuSans-Bold.ttf not found"

**Solução (Linux):**
```bash
# Instalar fontes DejaVu
sudo apt-get install fonts-dejavu fonts-dejavu-core fonts-dejavu-extra

# Verificar instalação
fc-list | grep DejaVu
```

**Solução (macOS):**
```bash
brew install --cask font-dejavu
```

**Solução (Windows):**
- Baixar DejaVu fonts de https://dejavu-fonts.github.io/
- Instalar manualmente

**Nota:** O script funciona com fonte padrão se DejaVu não estiver disponível.

---

## 🔧 Integração com Django

### Uso Programático

```python
# Em um Django management command ou view
from utils.print_labels import print_equipment_label

# Imprimir etiqueta
success = print_equipment_label(
    equipment_id=1,
    printer_id='usb://0x04f9:0x2015'
)

if success:
    print("Etiqueta impressa!")
else:
    print("Erro ao imprimir")
```

---

### Management Command (Opcional)

Criar `apps/equipment/management/commands/print_label.py`:

```python
from django.core.management.base import BaseCommand
from utils.print_labels import print_equipment_label

class Command(BaseCommand):
    help = 'Imprime etiqueta térmica para equipamento'

    def add_arguments(self, parser):
        parser.add_argument('equipment_id', type=int)

    def handle(self, *args, **options):
        equipment_id = options['equipment_id']
        success = print_equipment_label(equipment_id)

        if success:
            self.stdout.write(self.style.SUCCESS('Etiqueta impressa!'))
        else:
            self.stdout.write(self.style.ERROR('Erro ao imprimir'))
```

**Uso:**
```bash
python manage.py print_label 1
```

---

## 📦 Impressão em Lote

Para imprimir múltiplas etiquetas:

```bash
# Bash script simples
for id in 1 2 3 4 5; do
    python utils/print_labels.py $id
    sleep 2  # Aguardar 2 segundos entre impressões
done
```

Ou criar script Python:

```python
# batch_print.py
from utils.print_labels import print_equipment_label
from apps.equipment.models import Equipment

# Imprimir etiquetas para todos equipamentos ativos
equipment_list = Equipment.objects.filter(is_active=True)

for equipment in equipment_list:
    print(f"Imprimindo {equipment.name}...")
    print_equipment_label(equipment.id)
    # time.sleep(2)  # Aguardar entre impressões
```

---

## 🌐 Configuração de URL em Produção

### Desenvolvimento:
```bash
python utils/print_labels.py 1 --url http://localhost:8001
```

### Produção:
```bash
python utils/print_labels.py 1 --url https://cleantrack.seudominio.com
```

### Configurar URL Padrão:

Editar `utils/print_labels.py`:
```python
# Linha ~83
def print_equipment_label(
    equipment_id,
    printer_id='usb://0x04f9:0x2015',
    model='QL-800',
    label_size='29',
    base_url='https://cleantrack.seudominio.com'  # ← Alterar aqui
):
```

---

## ✅ Checklist de Implementação

- [x] Script `utils/print_labels.py` criado
- [x] Função `print_equipment_label()` implementada
- [x] Função `list_printers()` implementada
- [x] Função `save_preview()` implementada
- [x] CLI com argparse
- [x] Suporte a logo opcional
- [x] Layout otimizado para 29mm x 90mm
- [x] QR code de alta qualidade
- [x] Documentação completa
- [ ] Dependências instaladas (usuário)
- [ ] Permissões USB configuradas (usuário)
- [ ] Impressora Brother QL conectada (usuário)
- [ ] Teste de impressão real (usuário)
- [ ] Logo thermal PNG criado (opcional)

---

## 🚀 Próximos Passos (Opcional)

1. **Interface Web para Impressão:**
   - Criar view Django para imprimir via navegador
   - Botão "Imprimir Etiqueta" no admin

2. **Fila de Impressão:**
   - Implementar Celery task para impressão assíncrona
   - Evitar bloqueio da interface

3. **Impressão de Múltiplas Cópias:**
   - Adicionar parâmetro `--copies N`

4. **Histórico de Impressões:**
   - Criar model `PrintLog`
   - Registrar quando/quem imprimiu cada etiqueta

5. **Impressão via Rede:**
   - Suporte a impressoras em rede
   - `tcp://192.168.1.100:9100`

---

## 📚 Referências

- **Brother QL Python Library:** https://github.com/pklaus/brother_ql
- **Pillow Documentation:** https://pillow.readthedocs.io/
- **QRCode Library:** https://github.com/lincolnloop/python-qrcode
- **Brother QL-800 Manual:** https://support.brother.com/

---

## ✅ Status

**🖨️ SCRIPT DE IMPRESSÃO IMPLEMENTADO COM SUCESSO!**

- Arquivo criado: `utils/print_labels.py`
- Package criado: `utils/__init__.py`
- Funcionalidades: Impressão, Preview, Listar impressoras
- Compatível com: Brother QL-800/810/820
- Pronto para: Instalação de dependências e teste

---

**Desenvolvido com Python 3.12 | Brother QL Library | Pillow | QRCode**
**Data:** 2025-11-23
