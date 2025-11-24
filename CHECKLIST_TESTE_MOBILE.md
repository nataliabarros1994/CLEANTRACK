# 📱 Checklist de Teste Mobile - CleanTrack QR Code

**Data:** 21 de Novembro de 2025
**Sistema:** CleanTrack - Registro de Limpeza por QR Code
**Tester:** _______________________

---

## 🎯 Objetivo

Validar o fluxo completo de registro de limpeza via QR code em dispositivo móvel real.

---

## 📋 Pré-requisitos

- [ ] Servidor rodando: `http://localhost:8000`
- [ ] QR codes gerados e prontos para teste
- [ ] Celular com câmera funcional
- [ ] Celular conectado na mesma rede Wi-Fi
- [ ] Admin do CleanTrack acessível

---

## 🔗 URLs de Teste

**Equipamento 1 - Desfibrilador:**
```
http://localhost:8000/log/5:1763755273:4srW8F9vurgjQ1W4S_Uqgu_gb23EvbK-b6E60C8l2dw/
```

**Equipamento 2 - Raio-X:**
```
http://localhost:8000/log/6:1763755273:KgjkHiOv2tlCg8QBWjkULhSpR1kmZRwRdKAMsAWZqoQ/
```

**Equipamento 3 - Ressonância:**
```
http://localhost:8000/log/3:1763755273:esBcRVV2SVlh5euc37vGdQl_2GIgkF2mOgx4NIpbqe0/
```

**Equipamento 4 - Tomógrafo:**
```
http://localhost:8000/log/4:1763755273:ihzEvnkPvjIRo0j8V3tirdSfniJvUMKpD-LrZNpMt4Q/
```

**Equipamento 5 - Ultrassom:**
```
http://localhost:8000/log/2:1763755273:DDgQyvuo0MSOElTb5q-7G0IKcsou2o2W2MYZxksHjgQ/
```

---

## 📱 PARTE 1: Teste de QR Code Scanning

### Teste 1.1: Escanear QR Code Impresso
- [ ] Imprimir QR code do Desfibrilador
- [ ] Abrir câmera nativa do celular
- [ ] Apontar para o QR code impresso
- [ ] Verificar se link aparece na tela
- [ ] Tocar no link
- [ ] Página abre corretamente?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

### Teste 1.2: Escanear QR Code na Tela do Computador
- [ ] Abrir `QR_CODES_PARA_IMPRESSAO.html` no computador
- [ ] Escanear QR code diretamente da tela
- [ ] Link aparece?
- [ ] Página abre corretamente?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

## 📱 PARTE 2: Interface Mobile

### Teste 2.1: Carregamento da Página
- [ ] Página carrega em menos de 3 segundos?
- [ ] Layout está responsivo (não quebrado)?
- [ ] Texto legível sem zoom?
- [ ] Botões grandes o suficiente para tocar?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

### Teste 2.2: Informações do Equipamento
- [ ] Nome do equipamento aparece correto?
- [ ] Número de série aparece correto?
- [ ] Nome da facility aparece correto?
- [ ] Visual está bonito (gradiente, cores)?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

## 📷 PARTE 3: Upload de Foto

### Teste 3.1: Ativar Câmera
- [ ] Tocar no botão "📸 Tirar foto"
- [ ] Câmera nativa abre automaticamente?
- [ ] Consegue tirar foto?
- [ ] Foto aparece no preview?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

### Teste 3.2: Preview da Foto
- [ ] Foto aparece na tela após tirar?
- [ ] Preview está nítido?
- [ ] Tamanho adequado?
- [ ] Botão "Remover" aparece?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

### Teste 3.3: Remover Foto
- [ ] Tocar no botão "Remover"
- [ ] Foto desaparece?
- [ ] Botão "Tirar foto" volta a aparecer?
- [ ] Pode tirar outra foto?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

### Teste 3.4: Validação de Foto Obrigatória
- [ ] Tentar submeter sem foto
- [ ] Botão está desabilitado?
- [ ] Não envia o formulário?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

## 📝 PARTE 4: Campo de Observações

### Teste 4.1: Adicionar Observações
- [ ] Tocar no campo de observações
- [ ] Teclado virtual abre?
- [ ] Consegue digitar texto?
- [ ] Texto aparece corretamente?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

### Teste 4.2: Observações Opcionais
- [ ] Deixar observações em branco
- [ ] Consegue submeter normalmente?
- [ ] Sistema aceita sem observações?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

## ✅ PARTE 5: Submissão do Formulário

### Teste 5.1: Submissão HTMX
- [ ] Tirar foto
- [ ] Adicionar observações (opcional)
- [ ] Tocar em "✓ Registrar Limpeza"
- [ ] Loading spinner aparece?
- [ ] Página NÃO recarrega (HTMX)?
- [ ] Mensagem de sucesso aparece?

**Status:** ✅ PASS / ❌ FAIL
**Tempo de resposta:** _______ segundos
**Notas:** _______________________________________

---

### Teste 5.2: Mensagem de Sucesso
- [ ] Aparece "✅ Limpeza Registrada!"?
- [ ] Nome do equipamento está correto?
- [ ] Data e hora estão corretas?
- [ ] Mensagem "Você pode fechar esta página"?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

## 🖥️ PARTE 6: Verificação no Admin

### Teste 6.1: Limpeza Registrada
- [ ] Abrir admin: `http://localhost:8000/admin`
- [ ] Login com usuário admin
- [ ] Ir para "Cleaning Logs"
- [ ] Nova limpeza aparece na lista?
- [ ] Equipamento correto?
- [ ] Data/hora corretas?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

### Teste 6.2: Foto Salva
- [ ] Abrir o cleaning log criado
- [ ] Foto aparece no preview?
- [ ] Foto está nítida?
- [ ] Link da foto funciona?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

### Teste 6.3: Observações Salvas
- [ ] Observações aparecem corretas?
- [ ] Texto completo (não cortado)?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

### Teste 6.4: Registro Anônimo
- [ ] Campo "Cleaned by" está vazio?
- [ ] Sistema identifica como registro via QR?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

## ⚠️ PARTE 7: Testes de Erro

### Teste 7.1: Token Expirado
- [ ] Usar token antigo/inválido
- [ ] Página de erro aparece?
- [ ] Mensagem em português?
- [ ] Mensagem amigável?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

### Teste 7.2: Sem Conexão
- [ ] Desabilitar Wi-Fi/dados
- [ ] Tentar acessar URL
- [ ] Erro de conexão aparece?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

### Teste 7.3: Foto Muito Grande
- [ ] Tirar foto de alta resolução (se possível)
- [ ] Tentar enviar foto > 10MB
- [ ] Sistema rejeita?
- [ ] Mensagem de erro clara?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

## 🔄 PARTE 8: Teste de Múltiplas Limpezas

### Teste 8.1: Registrar 3 Limpezas Seguidas
- [ ] Escanear QR do Desfibrilador → Registrar
- [ ] Escanear QR do Raio-X → Registrar
- [ ] Escanear QR da Ressonância → Registrar
- [ ] Todas registraram com sucesso?

**Status:** ✅ PASS / ❌ FAIL
**Tempo total:** _______ minutos
**Notas:** _______________________________________

---

### Teste 8.2: Mesmo Equipamento Duas Vezes
- [ ] Registrar limpeza do Ultrassom
- [ ] Registrar novamente o mesmo Ultrassom
- [ ] Sistema aceita?
- [ ] Cria dois registros separados?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

## 📊 PARTE 9: Performance Mobile

### Teste 9.1: Velocidade
- [ ] Página carrega em < 3 segundos
- [ ] Foto faz upload em < 5 segundos
- [ ] HTMX responde em < 2 segundos
- [ ] Experiência é fluida?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

### Teste 9.2: Consumo de Dados
- [ ] Verificar uso de dados do teste
- [ ] Página é leve (< 500KB)?
- [ ] Upload de foto usa dados moderados?

**Status:** ✅ PASS / ❌ FAIL
**Consumo estimado:** _______ KB
**Notas:** _______________________________________

---

## 🌐 PARTE 10: Compatibilidade

### Teste 10.1: Diferentes Navegadores

**Chrome Mobile:**
- [ ] Funciona corretamente?

**Safari (iOS):**
- [ ] Funciona corretamente?

**Firefox Mobile:**
- [ ] Funciona corretamente?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

### Teste 10.2: Diferentes Tamanhos de Tela

**Celular pequeno (< 5"):**
- [ ] Layout responsivo?
- [ ] Botões tocáveis?

**Celular médio (5-6"):**
- [ ] Layout responsivo?
- [ ] Visual adequado?

**Tablet:**
- [ ] Layout responsivo?
- [ ] Usa espaço bem?

**Status:** ✅ PASS / ❌ FAIL
**Notas:** _______________________________________

---

## 🎯 PARTE 11: Experiência do Usuário

### Teste 11.1: Usabilidade
- [ ] Sistema é intuitivo?
- [ ] Não precisa de explicação?
- [ ] Fluxo é natural?
- [ ] Técnico leigo consegue usar?

**Status:** ✅ PASS / ❌ FAIL
**Nota (1-10):** _______
**Feedback:** _______________________________________

---

### Teste 11.2: Tempo de Conclusão
- [ ] Escanear → Foto → Registrar em < 60 segundos?
- [ ] Processo é rápido?

**Status:** ✅ PASS / ❌ FAIL
**Tempo médio:** _______ segundos
**Notas:** _______________________________________

---

## 📝 Resumo Final

**Total de Testes:** 35
**Testes Passou:** _______
**Testes Falhou:** _______
**Taxa de Sucesso:** _______%

---

## ✅ Critérios de Aceitação

Para o sistema ser considerado **PRONTO PARA PRODUÇÃO**, deve ter:

- [ ] **100%** dos testes críticos passando (Parte 1-6)
- [ ] **> 90%** de todos os testes passando
- [ ] **< 60 segundos** para completar uma limpeza
- [ ] **UX Score > 8/10**
- [ ] Funciona em pelo menos 2 navegadores
- [ ] Foto upload funciona consistentemente

---

## 🐛 Bugs Encontrados

**Bug #1:**
- Descrição: _______________________________________
- Severidade: 🔴 Alta / 🟡 Média / 🟢 Baixa
- Passos para reproduzir: _______________________________________

**Bug #2:**
- Descrição: _______________________________________
- Severidade: 🔴 Alta / 🟡 Média / 🟢 Baixa
- Passos para reproduzir: _______________________________________

**Bug #3:**
- Descrição: _______________________________________
- Severidade: 🔴 Alta / 🟡 Média / 🟢 Baixa
- Passos para reproduzir: _______________________________________

---

## 💡 Melhorias Sugeridas

1. _______________________________________
2. _______________________________________
3. _______________________________________

---

## ✍️ Assinaturas

**Tester:**
Nome: _______________________
Data: ____/____/______
Assinatura: _______________________

**Aprovador:**
Nome: _______________________
Data: ____/____/______
Assinatura: _______________________

---

## 📸 Screenshots (Opcional)

Cole aqui screenshots dos testes realizados:

- Screenshot da página inicial
- Screenshot do preview de foto
- Screenshot da mensagem de sucesso
- Screenshot do admin com registro

---

**Preparado por:** CleanTrack Team
**Versão:** 1.0
**Data:** 21/11/2025
**Status:** Pronto para teste ✅
