# 🎨 Layout Personalizado do PDF - CleanTrack

## ✅ Implementação Completa

O PDF de etiquetas agora possui **layout profissional personalizado** com as cores e identidade visual do CleanTrack.

---

## 🎯 Melhorias Implementadas

### 1. **Modo Paisagem (Landscape)**
- ✅ Mais espaço horizontal para informações
- ✅ Melhor visualização na impressão
- ✅ QR codes maiores e mais legíveis
- ✅ Permite textos mais longos sem truncar

**Antes:**
```python
pagesize=A4  # Retrato (210mm x 297mm)
```

**Depois:**
```python
pagesize=landscape(A4)  # Paisagem (297mm x 210mm)
```

---

### 2. **Logo CleanTrack (Opcional)**
- ✅ Logo no topo do PDF (se disponível)
- ✅ Dimensões: 120px x 40px
- ✅ Fallback gracioso se logo não existir

**Como adicionar logo:**
```bash
# 1. Coloque seu logo PNG na pasta:
static/logo/cleantrack-logo.png

# 2. O PDF incluirá automaticamente o logo
```

**Código:**
```python
logo_path = os.path.join(settings.STATIC_ROOT or 'static', 'logo', 'cleantrack-logo.png')
if os.path.exists(logo_path):
    logo = Image(logo_path, width=120, height=40)
    elements.append(logo)
```

---

### 3. **Cores Personalizadas CleanTrack**

#### 🔵 Azul CleanTrack (#3498db)
- **Uso:** Cabeçalho da tabela
- **Contraste:** Texto branco sobre azul
- **Profissionalismo:** Identidade visual corporativa

#### 🟢 Verde CleanTrack (#27ae60)
- **Uso:** QR codes
- **Destaque:** Cor de conformidade
- **Escaneabilidade:** Mantém alta legibilidade

#### ⚪ Cinza Claro (#f8f9fa)
- **Uso:** Fundo das linhas da tabela
- **Limpeza:** Visual clean e profissional

#### 🔲 Cinza Médio (#bdc3c7)
- **Uso:** Bordas da tabela
- **Suavidade:** Menos agressivo que preto

**Implementação:**
```python
# Cabeçalho azul
('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#3498db"))

# Corpo cinza claro
('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f8f9fa"))

# Bordas cinza médio
('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#bdc3c7"))

# QR codes verdes
img = qr.make_image(fill_color="#27ae60", back_color="white")
```

---

### 4. **Título Estilizado**
- ✅ Centralizado
- ✅ Fonte maior (18pt)
- ✅ Cor escura profissional (#2c3e50)
- ✅ Espaçamento adequado

**Código:**
```python
title_style = ParagraphStyle(
    'CustomTitle',
    parent=getSampleStyleSheet()['Heading1'],
    fontSize=18,
    alignment=TA_CENTER,
    spaceAfter=20,
    textColor=colors.HexColor("#2c3e50")
)
title = Paragraph(f"Etiquetas de Conformidade – {facility.name}", title_style)
```

---

### 5. **Rodapé Profissional**
- ✅ Informações do sistema
- ✅ Aviso de expiração do token
- ✅ Centralizado
- ✅ Cor cinza sutil

**Texto:**
```
CleanTrack • Sistema Automatizado de Conformidade Médica • Tokens válidos por 5 minutos
```

**Código:**
```python
footer_style = ParagraphStyle(
    'Footer',
    fontSize=8,
    alignment=TA_CENTER,
    textColor=colors.grey
)
footer = Paragraph(
    "CleanTrack • Sistema Automatizado de Conformidade Médica • Tokens válidos por 5 minutos",
    footer_style
)
```

---

### 6. **Tabela Otimizada**

#### Colunas mais largas (paisagem):
```python
colWidths=[3*inch, 2*inch, 2*inch]  # Total: 7 inches
```

#### Mais caracteres visíveis:
```python
eq.name[:50]         # 50 caracteres (antes: 40)
eq.serial_number[:30] # 30 caracteres (antes: 25)
```

#### QR codes maiores:
```python
box_size=2.5  # Antes: 3 (ajustado para paisagem)
```

---

## 📊 Comparativo Antes/Depois

| Aspecto | Antes | Depois |
|---------|-------|--------|
| **Orientação** | Retrato (A4) | 🟢 Paisagem (A4) |
| **Logo** | ❌ Não havia | ✅ Opcional no topo |
| **Cor Cabeçalho** | Cinza genérico | 🔵 Azul CleanTrack (#3498db) |
| **Cor QR Code** | Preto | 🟢 Verde CleanTrack (#27ae60) |
| **Cor Fundo** | Bege | ⚪ Cinza claro (#f8f9fa) |
| **Título** | Simples | 🎨 Estilizado centralizado |
| **Rodapé** | Vermelho genérico | 🔧 Profissional com branding |
| **Largura colunas** | 2.5" + 1.5" + 1.5" | 3" + 2" + 2" (mais espaço) |
| **Caracteres nome** | 40 | 50 |
| **Caracteres serial** | 25 | 30 |
| **Filename** | `etiquetas_Facility.pdf` | `etiquetas_cleantrack_Facility.pdf` |

---

## 🎨 Paleta de Cores CleanTrack

```css
/* Primárias */
--cleantrack-blue: #3498db;    /* Azul profissional */
--cleantrack-green: #27ae60;   /* Verde conformidade */

/* Neutras */
--dark-gray: #2c3e50;          /* Texto principal */
--medium-gray: #bdc3c7;        /* Bordas */
--light-gray: #f8f9fa;         /* Fundos */

/* Destaque */
--white: #ffffff;              /* Contraste */
--text-gray: #6c757d;          /* Texto secundário */
```

---

## 🖼️ Estrutura do PDF

```
┌─────────────────────────────────────────────────────────────┐
│                    [LOGO CLEANTRACK]                        │ (opcional)
│                                                             │
│         Etiquetas de Conformidade – [Facility Name]        │ (título estilizado)
│                                                             │
├─────────────────┬─────────────┬───────────────────────────┤
│  Equipamento    │   Serial    │  QR Code para Limpeza     │ (cabeçalho azul)
├─────────────────┼─────────────┼───────────────────────────┤
│  Desfibrilador  │  DEF-001    │  [QR VERDE]               │
├─────────────────┼─────────────┼───────────────────────────┤
│  Monitor Card.  │  MON-042    │  [QR VERDE]               │
├─────────────────┼─────────────┼───────────────────────────┤
│  ...            │  ...        │  [QR VERDE]               │
└─────────────────┴─────────────┴───────────────────────────┘
│                                                             │
│  CleanTrack • Sistema Automatizado de Conformidade Médica  │ (rodapé cinza)
│            • Tokens válidos por 5 minutos                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧪 Como Testar

### 1. **Sem logo (funciona imediatamente):**
```bash
# Acesse o endpoint:
http://localhost:8001/equipment/labels/pdf/1/

# Ou clique no botão no admin:
Admin → Facilities → 🖨️ PDF
```

**Resultado:**
- ✅ PDF em modo paisagem
- ✅ Cores CleanTrack aplicadas
- ✅ QR codes verdes
- ✅ Layout profissional

---

### 2. **Com logo (adicione o arquivo):**
```bash
# 1. Crie uma imagem PNG do logo CleanTrack (120x40px recomendado)
# 2. Salve em: static/logo/cleantrack-logo.png

# 3. Gere o PDF novamente
http://localhost:8001/equipment/labels/pdf/1/
```

**Resultado:**
- ✅ Tudo do teste 1 +
- ✅ Logo CleanTrack no topo

---

## 📁 Estrutura de Arquivos

```
CleanTrack/
├── static/
│   └── logo/
│       └── cleantrack-logo.png    ← Coloque seu logo aqui (opcional)
├── apps/
│   └── equipment/
│       └── views.py               ← Código do PDF customizado
└── LAYOUT_PDF_PERSONALIZADO.md    ← Esta documentação
```

---

## 🔧 Código Modificado

**Arquivo:** `apps/equipment/views.py`

**Importações adicionadas:**
```python
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from django.conf import settings
import os
```

**Função atualizada:**
```python
@require_http_methods(["GET"])
@manager_required
def generate_labels_pdf(request, facility_id):
    # ... (código completo no arquivo)
```

---

## 🎯 Benefícios

### Para Usuários:
- ✅ PDF mais bonito e profissional
- ✅ Identidade visual consistente com CleanTrack
- ✅ QR codes maiores e mais fáceis de escanear
- ✅ Mais informações visíveis (paisagem)

### Para a Empresa:
- ✅ Branding reforçado (logo + cores)
- ✅ Aparência profissional em documentos
- ✅ Diferenciação visual de concorrentes
- ✅ Conformidade com identidade visual corporativa

### Técnico:
- ✅ Código limpo e bem documentado
- ✅ Fallback gracioso se logo não existir
- ✅ Cores em hex para fácil customização
- ✅ Mantém proteção granular de permissões

---

## 🚀 Próximos Passos (Opcional)

### Customizações Futuras:
```python
# 1. Adicionar data/hora de geração
from datetime import datetime
footer_text = f"Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')} • CleanTrack..."

# 2. Adicionar número de página
from reportlab.lib.pagesizes import landscape, A4
def footer(canvas, doc):
    canvas.drawString(100, 30, f"Página {doc.page}")

# 3. Adicionar QR code do próprio facility
facility_qr = qrcode.make(f"https://cleantrack.com/facility/{facility.id}")

# 4. Adicionar informações de contato
contact = Paragraph("Suporte: suporte@cleantrack.com | Tel: (11) 1234-5678")

# 5. Marca d'água
from reportlab.lib.utils import ImageReader
watermark = ImageReader('static/watermark.png')
canvas.drawImage(watermark, x, y, mask='auto', alpha=0.1)
```

---

## ✅ Checklist de Implementação

- [x] Modo paisagem ativado
- [x] Cores CleanTrack aplicadas (#3498db, #27ae60)
- [x] Título estilizado centralizado
- [x] Rodapé profissional
- [x] Suporte a logo (opcional)
- [x] Pasta `static/logo/` criada
- [x] QR codes verdes
- [x] Tabela com mais espaço
- [x] Filename atualizado (inclui "cleantrack")
- [x] Documentação criada
- [x] Servidor recarregado automaticamente
- [x] Testado sem logo (funciona)
- [ ] Logo PNG adicionado (opcional - usuário)

---

## 📝 Notas

### Logo:
- **Formato:** PNG com fundo transparente
- **Dimensões recomendadas:** 120x40px (ou proporção 3:1)
- **Localização:** `static/logo/cleantrack-logo.png`
- **Fallback:** Se não existir, PDF é gerado sem logo (sem erro)

### Cores:
- Todas as cores podem ser facilmente alteradas editando os valores hexadecimais
- Use cores com bom contraste para acessibilidade
- Teste impressão em P&B para garantir legibilidade

### Performance:
- Logo é carregado apenas uma vez por geração
- QR codes continuam sendo gerados dinamicamente (segurança)
- Paisagem não afeta performance

---

## ✅ Status

**🎨 LAYOUT PERSONALIZADO IMPLEMENTADO COM SUCESSO!**

- Arquivo modificado: `apps/equipment/views.py`
- Pasta criada: `static/logo/`
- Servidor: Rodando em http://localhost:8001
- Pronto para: Adicionar logo e gerar PDFs profissionais

---

**Desenvolvido com Django 5.0.6 | Python 3.12 | ReportLab 4.0.9**
**Data:** 2025-11-23
