# 🛠️ CleanTrack Utilities

Utilitários do sistema CleanTrack.

## 📁 Conteúdo

### `print_labels.py`
Script para impressão de etiquetas térmicas em impressoras Brother QL-800/810/820.

**Uso:**
```bash
python utils/print_labels.py 1
```

**Documentação completa:** `../IMPRESSAO_ETIQUETAS_TERMICAS.md`

## 🔧 Instalação

```bash
pip install brother-ql pillow qrcode
sudo usermod -a -G lp $USER  # Linux
```

## 📖 Funções Disponíveis

### `print_equipment_label(equipment_id, ...)`
Imprime etiqueta térmica para um equipamento.

### `list_printers()`
Lista impressoras Brother QL disponíveis.

### `save_preview(equipment_id, output_path)`
Gera preview da etiqueta sem imprimir.

## 🚀 Exemplos

```python
from utils.print_labels import print_equipment_label, list_printers

# Listar impressoras
printers = list_printers()

# Imprimir etiqueta
success = print_equipment_label(1)
```

## 📚 Documentação

- **Guia Completo:** `../IMPRESSAO_ETIQUETAS_TERMICAS.md`
- **Guia Rápido:** `../GUIA_RAPIDO_IMPRESSAO.txt`
