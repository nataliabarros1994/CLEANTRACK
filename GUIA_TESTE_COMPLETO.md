# 🧪 Guia de Teste Completo - Sistema de Limpeza via QR Code

## ✅ Checklist de Implementação

### Passo 1: Verificar Campo `public_token` no Model Equipment
- [x] ✅ Campo `public_token` adicionado ao modelo
- [x] ✅ Auto-geração de token no `save()`
- [x] ✅ Migração criada: `0003_equipment_public_token.py`
- [x] ✅ Migração aplicada com sucesso
- [x] ✅ 5 equipamentos com tokens únicos

**Verificação:**
```bash
docker-compose exec -T web python manage.py shell -c "
from apps.equipment.models import Equipment
eq = Equipment.objects.first()
print(f'Equipment: {eq.name}')
print(f'Token: {eq.public_token}')
print(f'Token único: {Equipment.objects.filter(public_token=eq.public_token).count() == 1}')
"
```

### Passo 2: Arquivos Criados
- [x] ✅ `apps/cleaning_logs/views.py` - Views simplificadas
- [x] ✅ `apps/cleaning_logs/urls.py` - Rotas públicas
- [x] ✅ `apps/cleaning_logs/forms.py` - Form de validação
- [x] ✅ `cleantrack/urls.py` - Include das rotas
- [x] ✅ `templates/cleaning_logs/public_log_form.html` - Template HTMX
- [x] ✅ `utils/generate_qr.py` - Script de geração de QR

### Passo 3: Migrações
- [x] ✅ Migração `0003_equipment_public_token.py` criada
- [x] ✅ Migração `0004_equipment_category_description_and_more.py` criada
- [x] ✅ Todas migrações aplicadas
- [x] ✅ Tokens gerados para equipamentos existentes

### Passo 4: QR Codes Gerados
- [x] ✅ 5 QR codes gerados em `media/qrcodes/`
- [x] ✅ Arquivos: eq_2.png, eq_3.png, eq_4.png, eq_5.png, eq_6.png

---

## 🎯 Teste Manual - Passo a Passo

### 📋 Preparação

#### 1. Obter Token de Teste
```bash
docker-compose exec -T web python manage.py shell -c "
from apps.equipment.models import Equipment
eq = Equipment.objects.first()
print('=' * 70)
print('TOKEN PARA TESTE')
print('=' * 70)
print(f'Equipamento: {eq.name}')
print(f'Token: {eq.public_token}')
print(f'URL: http://localhost:8000/log/{eq.public_token}/')
print('=' * 70)
print('Copie a URL acima e cole no navegador!')
print('=' * 70)
"
```

**Output esperado:**
```
======================================================================
TOKEN PARA TESTE
======================================================================
Equipamento: Desfibrilador Philips HeartStart
Token: 2r7Zgna2fTpX2-5LoYCE2w
URL: http://localhost:8000/log/2r7Zgna2fTpX2-5LoYCE2w/
======================================================================
Copie a URL acima e cole no navegador!
======================================================================
```

#### 2. Listar Todos os Tokens Disponíveis
```bash
docker-compose exec -T web python manage.py shell -c "
from apps.equipment.models import Equipment

print('=' * 70)
print('EQUIPAMENTOS DISPONÍVEIS PARA TESTE')
print('=' * 70)
print()

for eq in Equipment.objects.filter(is_active=True):
    print(f'📋 {eq.name}')
    print(f'   Token: {eq.public_token}')
    print(f'   URL: http://localhost:8000/log/{eq.public_token}/')
    print(f'   Facility: {eq.facility.name}')
    print()
"
```

---

## 🌐 Teste no Navegador

### Passo 1: Acessar a URL

1. Abra o navegador (Chrome, Firefox, Safari, etc.)
2. Cole a URL: `http://localhost:8000/log/2r7Zgna2fTpX2-5LoYCE2w/`
3. Pressione Enter

**✅ Resultado esperado:**
- Página carrega com título "Registrar Limpeza"
- Header azul com nome do equipamento
- Formulário com campo de foto
- Campo de observações
- Botão "Registrar Limpeza"

### Passo 2: Verificar Elementos da Página

Abra o console do navegador (F12) e execute:
```javascript
// Verificar HTMX
console.log('HTMX:', typeof htmx !== 'undefined' ? '✅ Carregado' : '❌ Faltando');

// Verificar Alpine.js
console.log('Alpine:', typeof Alpine !== 'undefined' ? '✅ Carregado' : '❌ Faltando');

// Verificar Bootstrap
console.log('Bootstrap:', typeof bootstrap !== 'undefined' ? '✅ Carregado' : '❌ Faltando');

// Verificar elementos do form
console.log('Form:', document.querySelector('form') ? '✅ Presente' : '❌ Faltando');
console.log('Input foto:', document.querySelector('input[type="file"]') ? '✅ Presente' : '❌ Faltando');
console.log('Textarea:', document.querySelector('textarea[name="notes"]') ? '✅ Presente' : '❌ Faltando');
console.log('Botão submit:', document.querySelector('button[type="submit"]') ? '✅ Presente' : '❌ Faltando');
```

**✅ Todos devem retornar "Carregado" ou "Presente"**

### Passo 3: Testar Upload de Foto

1. **Clicar no campo "Foto da Limpeza"**
   - Se estiver no desktop: abre seletor de arquivo
   - Se estiver no mobile: abre câmera (atributo `capture="environment"`)

2. **Selecionar uma imagem**
   - Pode usar qualquer foto de teste
   - Formatos: JPG, PNG, WebP
   - Tamanho máximo: 10MB

3. **Verificar Preview**
   - ✅ Preview da foto deve aparecer abaixo do campo
   - ✅ Imagem deve estar visível
   - ✅ Botão "X" para remover deve aparecer

### Passo 4: Adicionar Observações (Opcional)

1. Clicar no campo "Observações"
2. Digitar texto de teste:
   ```
   Limpeza realizada com álcool 70%
   Equipamento em perfeitas condições
   ```

### Passo 5: Enviar Formulário

1. **Clicar no botão "✅ Registrar Limpeza"**
2. **Observar:**
   - Botão muda para "⏳ Enviando..."
   - Botão fica desabilitado
   - Após 1-2 segundos, aparece mensagem de sucesso

**✅ Resultado esperado:**
```
✅ Limpeza registrada com sucesso!
[Registrar outra]
```

3. **Verificar que o form foi resetado:**
   - Preview da foto sumiu
   - Campo de observações está vazio
   - Campo de foto está vazio

### Passo 6: Verificar no Banco de Dados

```bash
docker-compose exec -T web python manage.py shell -c "
from apps.cleaning_logs.models import CleaningLog
from django.utils import timezone
from datetime import timedelta

# Buscar limpezas das últimas 5 minutos
recent = timezone.now() - timedelta(minutes=5)
logs = CleaningLog.objects.filter(cleaned_at__gte=recent).order_by('-cleaned_at')

print('=' * 70)
print('LIMPEZAS REGISTRADAS (últimos 5 minutos)')
print('=' * 70)
print()

if logs.exists():
    for log in logs:
        print(f'ID: {log.id}')
        print(f'Equipamento: {log.equipment.name}')
        print(f'Data/Hora: {log.cleaned_at.strftime(\"%d/%m/%Y %H:%M:%S\")}')
        print(f'Foto: {\"✅ Sim\" if log.photo else \"❌ Não\"}')
        print(f'Observações: {log.notes[:50] if log.notes else \"(vazio)\"}')
        print(f'Compliant: {\"✅\" if log.is_compliant else \"❌\"}')
        print()
else:
    print('❌ Nenhuma limpeza registrada nos últimos 5 minutos')
    print('Teste o upload novamente!')
"
```

**✅ Resultado esperado:**
```
======================================================================
LIMPEZAS REGISTRADAS (últimos 5 minutos)
======================================================================

ID: 15
Equipamento: Desfibrilador Philips HeartStart
Data/Hora: 21/11/2025 21:30:45
Foto: ✅ Sim
Observações: Limpeza realizada com álcool 70% Equipamento em...
Compliant: ✅
```

---

## 📱 Teste no Mobile (Opcional)

### Passo 1: Configurar Acesso Externo

Se quiser testar no celular:

1. **Descobrir IP do computador:**
```bash
# Linux/Mac
ip addr show | grep "inet " | grep -v 127.0.0.1

# Windows (PowerShell)
ipconfig | findstr IPv4
```

2. **Acessar no celular:**
```
http://SEU_IP:8000/log/2r7Zgna2fTpX2-5LoYCE2w/
```

Exemplo: `http://192.168.1.100:8000/log/2r7Zgna2fTpX2-5LoYCE2w/`

### Passo 2: Testar Câmera no Mobile

1. Abrir URL no navegador do celular
2. Clicar em "Foto da Limpeza"
3. **✅ Câmera traseira deve abrir automaticamente** (graças ao `capture="environment"`)
4. Tirar foto
5. Verificar preview
6. Enviar

---

## 🎨 Teste de Funcionalidades

### Teste 1: Preview de Foto ✅
- [ ] Selecionar foto
- [ ] Preview aparece
- [ ] Preview está visível e correto
- [ ] Botão de remover funciona
- [ ] Preview some ao remover

### Teste 2: Loading State ✅
- [ ] Clicar em "Registrar Limpeza"
- [ ] Botão muda para "Enviando..."
- [ ] Botão fica desabilitado
- [ ] Não é possível clicar novamente

### Teste 3: Validação de Foto Obrigatória ✅
- [ ] Tentar enviar sem foto
- [ ] Navegador bloqueia (HTML5 `required`)
- [ ] Mensagem de erro aparece

### Teste 4: Upload com Sucesso ✅
- [ ] Enviar form completo
- [ ] Mensagem de sucesso aparece
- [ ] Form é resetado
- [ ] Botão "Registrar outra" funciona

### Teste 5: Token Inválido ✅
- [ ] Acessar URL com token errado: `http://localhost:8000/log/token_invalido/`
- [ ] Página de erro 404 aparece
- [ ] Mensagem: "QR Code Inválido"

---

## 🔍 Troubleshooting

### Problema 1: Página não carrega (404)

**Sintoma:** "Page not found"

**Solução:**
```bash
# Verificar rotas
docker-compose exec web python manage.py show_urls | grep log

# Deve mostrar:
# /log/<str:token>/           cleaning_logs:public_log_form
# /log/<str:token>/submit/    cleaning_logs:public_log_submit
```

### Problema 2: HTMX/Alpine não funciona

**Sintoma:** Form recarrega a página ao enviar

**Solução:**
- Abrir console do navegador (F12)
- Verificar erros de JavaScript
- Verificar se scripts CDN carregaram (aba Network)

### Problema 3: Preview não aparece

**Sintoma:** Foto selecionada mas preview não mostra

**Solução:**
```javascript
// No console do navegador
document.querySelector('input[type="file"]').addEventListener('change', function(e) {
    console.log('File selected:', e.target.files[0]);
});
```

### Problema 4: Erro ao enviar

**Sintoma:** Mensagem de erro após clicar em Registrar

**Solução:**
```bash
# Verificar logs do Django
docker-compose logs -f web --tail=50

# Procurar por:
# - Error creating cleaning log
# - Form validation errors
```

### Problema 5: Token expirado

**Sintoma:** "QR Code Inválido" mesmo com token correto

**Solução:**
```bash
# Verificar se equipamento está ativo
docker-compose exec -T web python manage.py shell -c "
from apps.equipment.models import Equipment
eq = Equipment.objects.get(public_token='SEU_TOKEN')
print(f'Ativo: {eq.is_active}')
"

# Se inativo, ativar:
docker-compose exec -T web python manage.py shell -c "
from apps.equipment.models import Equipment
eq = Equipment.objects.get(public_token='SEU_TOKEN')
eq.is_active = True
eq.save()
print('✅ Equipamento ativado')
"
```

---

## 📊 Checklist Final de Testes

### Backend
- [x] ✅ Campo `public_token` existe no modelo
- [x] ✅ Tokens gerados automaticamente
- [x] ✅ Migrações aplicadas
- [x] ✅ Views funcionando
- [x] ✅ URLs configuradas
- [x] ✅ Form validation ativa

### Frontend
- [ ] Template carrega corretamente
- [ ] HTMX carregado
- [ ] Alpine.js carregado
- [ ] Bootstrap carregado
- [ ] Formulário visível
- [ ] Preview de foto funciona
- [ ] Loading state funciona
- [ ] Envio sem reload funciona
- [ ] Mensagem de sucesso aparece
- [ ] Form reseta após sucesso

### Database
- [ ] CleaningLog criado com sucesso
- [ ] Foto salva em media/photos/
- [ ] Observações salvas corretamente
- [ ] is_compliant = True
- [ ] cleaned_at preenchido
- [ ] equipment vinculado corretamente

---

## 🎯 Teste Completo em 5 Minutos

**Script rápido para testar tudo:**

```bash
# 1. Obter URL de teste
docker-compose exec -T web python manage.py shell -c "
from apps.equipment.models import Equipment
eq = Equipment.objects.first()
print(f'URL: http://localhost:8000/log/{eq.public_token}/')
"

# 2. Abrir no navegador e testar upload

# 3. Verificar resultado
docker-compose exec -T web python manage.py shell -c "
from apps.cleaning_logs.models import CleaningLog
log = CleaningLog.objects.last()
print(f'✅ Último registro: {log.equipment.name}')
print(f'✅ Foto: {bool(log.photo)}')
print(f'✅ Data: {log.cleaned_at}')
"
```

---

## 📚 Próximos Passos

Após testes bem-sucedidos:

1. **Gerar QR codes para todos equipamentos:**
   ```python
   from utils.generate_qr import generate_qr_for_all_equipment
   generate_qr_for_all_equipment()
   ```

2. **Imprimir QR codes**
3. **Colar nos equipamentos**
4. **Treinar equipe**
5. **Monitorar logs de limpeza**

---

**Data:** 21/11/2025
**Status:** ✅ Sistema pronto para teste
**Versão:** 1.0
