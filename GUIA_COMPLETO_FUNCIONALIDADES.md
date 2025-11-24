# 📚 CleanTrack - Guia Completo de Funcionalidades

**Sistema de Rastreamento de Limpeza de Equipamentos Médicos**

---

## 📑 Índice

1. [Equipamentos](#-equipamentos)
2. [Sistema de QR Code](#-sistema-de-qr-code)
3. [Registro de Limpeza](#-registro-de-limpeza)
4. [Instalações](#-instalações)
5. [Usuários e Autenticação](#-usuários-e-autenticação)
6. [Dashboard e Relatórios](#-dashboard-e-relatórios)
7. [Cobrança e Stripe](#-cobrança-e-stripe)
8. [Notificações e Emails](#-notificações-e-emails)
9. [Geração de PDFs](#-geração-de-pdfs)
10. [API Admin](#-api-admin)
11. [Comandos de Gerenciamento](#-comandos-de-gerenciamento)
12. [Segurança](#-segurança)
13. [Configuração e Deploy](#-configuração-e-deploy)

---

## 🔧 Equipamentos

### Admin - Gerenciamento

| Funcionalidade | Como Usar | Endpoint/Comando |
|----------------|-----------|------------------|
| **QR no Admin** | Edite um equipamento → salve → veja QR code + token válido por 5 min | `/admin/equipment/equipment/` |
| **Token Expirável** | Após 5 min, o link mostra "expirado" (segurança contra uso indevido) | N/A |
| **PDF de Etiquetas** | Acesse `/equipment/labels/pdf/{facility_id}/` → baixe PDF com QR codes prontos para impressão | `/equipment/labels/pdf/<facility_id>/` |
| **Regenerar QR Codes em Massa** | Selecione equipamentos na lista → Actions → Regenerate QR Codes | Admin Action |
| **Gerar PDF Labels em Massa** | Selecione equipamentos → Actions → Generate PDF Labels | Admin Action |
| **Filtros Avançados** | Filtre por instalação/categoria/status ativo/data de criação | Admin: Sidebar filters |
| **Busca Inteligente** | Busque por nome/serial/descrição/localização | Admin: Search box |

### Modelos e Propriedades

| Funcionalidade | Como Usar | Detalhes |
|----------------|-----------|----------|
| **Categorias de Equipamento** | Diagnóstico/Monitoramento/Suporte à Vida/Cirúrgico/Laboratório/Outro | `category` field |
| **Frequências de Limpeza** | 1h/4h/8h/24h/Semanal (168h) | `cleaning_frequency_hours` field |
| **Status de Atraso** | Verifica automaticamente se limpeza está atrasada | `is_overdue` property |
| **Última Limpeza** | Retorna o registro mais recente de limpeza | `last_cleaning` property |
| **Localização Completa** | Instalação + Local específico | `full_location` property |

---

## 📱 Sistema de QR Code

### Geração de QR Codes

| Funcionalidade | Como Usar | Endpoint/Comando |
|----------------|-----------|------------------|
| **QR Code Permanente** | Token permanente gerado automaticamente ao criar equipamento | Auto-generated on save |
| **QR Code Temporário (5 min)** | Token HMAC válido por 5 minutos | `GET /admin-api/equipment/<id>/generate-temp-token/` |
| **Comando de Geração em Lote** | `python manage.py generate_qr_codes --facility-id=1 --output-dir=qr_codes` | Command: `generate_qr_codes` |
| **Nível de Correção de Erro** | Alta correção (30%) para escaneamento confiável | `generate_qr_code(error_correction='H')` |
| **Tamanho Customizável** | Configure box_size (8-12 pixels recomendado) | `generate_qr_code(size=10)` |

### Segurança de QR Codes

| Funcionalidade | Como Usar | Método |
|----------------|-----------|--------|
| **Rotação de Token** | Regenere token para revogar acesso ao QR antigo | `equipment.regenerate_token()` |
| **Validação de Token** | Verifica se token é válido e equipamento está ativo | `Equipment.validate_token(token)` |
| **Revogar Acesso** | Desativa equipamento para bloquear todos os QR codes | `equipment.revoke_access()` |
| **Log de Auditoria** | Rastreia criação/uso/expiração de tokens temporários | Model: `TemporaryTokenLog` |

---

## 🧹 Registro de Limpeza

### Registro Público (via QR Code)

| Funcionalidade | Como Usar | Endpoint |
|----------------|-----------|----------|
| **Formulário Público via QR** | Escaneie QR → abra formulário → tire foto → submeta | `/log/<token>/` |
| **Captura de Foto Obrigatória** | Use câmera do celular para tirar foto do equipamento limpo | Form field: `photo` (required) |
| **Notas Opcionais** | Adicione observações sobre a limpeza (máx 500 caracteres) | Form field: `notes` (optional) |
| **Validação de Formato de Foto** | Aceita JPEG/PNG/WebP até 10MB | Photo validation |
| **Confirmação de Sucesso** | Veja página de confirmação após registro bem-sucedido | `/cleaning/success/<equipment_id>/` |
| **Token Expirado** | Mensagem clara quando token de 5 min expira | `/temp-log/<expired_token>/` |

### Registro Autenticado

| Funcionalidade | Como Usar | Endpoint |
|----------------|-----------|----------|
| **Registro via Painel** | Login → `/cleaning/register/<equipment_id>/` → preencha formulário | `/cleaning/register/<equipment_id>/` |
| **Auto-preenchimento de Usuário** | Técnicos têm campo cleaned_by preenchido automaticamente | Admin auto-fill |

### Validação e Conformidade

| Funcionalidade | Como Usar | Detalhes |
|----------------|-----------|----------|
| **Prevenção de Duplicatas** | Bloqueia registros duplicados em intervalo de 1 hora | Model validation |
| **Rejeição de Datas Futuras** | Não permite registrar limpeza com data futura | Model validation |
| **Cálculo Automático de Conformidade** | Marca como não-conforme se limpeza feita após prazo | Auto-calculated on save |
| **Notificação de Não-Conformidade** | Envia email para gestores quando limpeza não-conforme é registrada | Auto-notification |

---

## 🏥 Instalações

### Admin - Gerenciamento

| Funcionalidade | Como Usar | Detalhes |
|----------------|-----------|----------|
| **Filtro por Status** | Veja instalações ativas/inativas (assinaturas válidas) | Admin: Active filter |
| **Hierarquia por Data** | Navegue por data de criação | Admin: Date hierarchy |
| **Acesso por Gestor** | Gestores veem apenas instalações atribuídas a eles | Permission-based queryset |
| **Somente Leitura para Técnicos** | Técnicos podem ver mas não editar instalações | `has_change_permission` override |

### Modelos

| Campo | Descrição |
|-------|-----------|
| **ID do Cliente Stripe** | Rastreia cliente Stripe para cobrança (`stripe_customer_id`) |
| **Status Ativo** | Ativado/desativado baseado em assinatura Stripe (`is_active`) |

---

## 👥 Usuários e Autenticação

### Autenticação

| Funcionalidade | Como Usar | Endpoint |
|----------------|-----------|----------|
| **Login por Email** | Use email (não username) para fazer login | `/accounts/login/` |
| **Redirecionamento por Papel** | Admins → admin site / Outros → dashboard | login_view redirect |
| **Backend Customizado** | EmailBackend para autenticação por email | `AUTHENTICATION_BACKENDS` |
| **Suporte a Parâmetro Next** | Retorna à página solicitada após login | `?next=/path/` |

### Papéis de Usuário

| Papel | Permissões | Role Value |
|-------|-----------|------------|
| **Admin** | Acesso total ao sistema | `admin` |
| **Gestor** | Acesso a instalações atribuídas | `manager` |
| **Técnico** | Somente leitura + registro de limpeza | `technician` |

### Decoradores de Permissão

| Decorador | Uso | Detalhes |
|-----------|-----|----------|
| **@admin_required** | Restringe views apenas para admins | View decorator |
| **@manager_or_admin_required** | Permite gestores e admins | View decorator |
| **@role_required** | Restrição genérica por papel | View decorator |
| **Instalações Gerenciadas** | Campo ManyToMany para multi-instalação | Field: `managed_facilities` |

---

## 📊 Dashboard e Relatórios

### Dashboard - Visão Geral

| Funcionalidade | Descrição | Endpoint |
|----------------|-----------|----------|
| **Total de Equipamentos** | Contador de todos os equipamentos ativos | `/accounts/dashboard/` |
| **Equipamentos Atrasados** | Lista equipamentos com limpeza vencida | `/accounts/dashboard/` |
| **Limpezas Recentes** | Exibe registros de limpeza mais recentes | `/accounts/dashboard/` |

### Relatórios

| Funcionalidade | Descrição | Endpoint |
|----------------|-----------|----------|
| **Estatísticas de Conformidade** | Total/atrasados/taxa de conformidade | `/accounts/reports/` |
| **Atividade Semanal** | Contagem de limpezas por semana | `/accounts/reports/` |
| **Acesso Restrito** | Apenas gestores e admins | `@manager_or_admin_required` |

---

## 💳 Cobrança e Stripe

### Webhooks Stripe

| Evento | Ação | Webhook |
|--------|------|---------|
| **Assinatura Criada** | Ativa conta quando assinatura inicia | `customer.subscription.created` |
| **Assinatura Atualizada** | Ativa/desativa baseado em status | `customer.subscription.updated` |
| **Assinatura Cancelada** | Desativa conta ao cancelar | `customer.subscription.deleted` |
| **Pagamento Bem-Sucedido** | Registra pagamento com valor | `invoice.payment_succeeded` |
| **Pagamento Falhou** | Registra falha para retry | `invoice.payment_failed` |
| **Checkout Completo** | Ativa instalação + define customer ID + envia boas-vindas | `checkout.session.completed` |

### Segurança

| Funcionalidade | Descrição |
|----------------|-----------|
| **Verificação de Assinatura** | Verifica assinatura Stripe via HMAC-SHA256 |

---

## 📧 Notificações e Emails

### Tipos de Email

| Email | Uso | Função |
|-------|-----|--------|
| **Alerta de Limpeza Atrasada** | Email HTML para equipamento vencido | `send_cleaning_alert(email, equipment)` |
| **Resumo de Conformidade Semanal** | Relatório com estatísticas para gestores | `send_compliance_summary(email, data)` |
| **Email de Boas-Vindas** | Onboarding após checkout Stripe | `send_welcome_email(email, name)` |
| **Notificação de Registro** | Email quando limpeza é registrada | `notify_cleaning_registered(log)` |

### Lógica Inteligente

| Funcionalidade | Descrição |
|----------------|-----------|
| **Seleção Inteligente de Destinatários** | Prioriza gestores da instalação → todos gestores → superusers |

### Comandos

| Comando | Uso | Detalhes |
|---------|-----|----------|
| **Alertas Atrasados** | `python manage.py send_overdue_alerts` | Command: `send_overdue_alerts` |
| **Relatórios de Conformidade** | `python manage.py send_compliance_reports` | Command: `send_compliance_reports` |
| **Modo Dry-Run** | Teste comandos sem enviar emails (`--dry-run`) | `--dry-run` flag |

### Integração Resend

| Funcionalidade | Detalhes |
|----------------|----------|
| **API Resend** | Serviço de email via Resend API (`RESEND_API_KEY`) |
| **Templates HTML** | Emails formatados em HTML profissional |
| **Tratamento de Erros** | Log de erros em falhas de envio |

---

## 📄 Geração de PDFs

### PDF de Etiquetas

| Funcionalidade | Como Usar | Endpoint |
|----------------|-----------|----------|
| **Layout A4 2x4** | 8 etiquetas por página (2 colunas x 4 linhas) | `/admin-api/equipment/generate-labels-pdf/` |
| **Informações por Etiqueta** | Nome/serial/instalação/localização/QR code | Label content |
| **Aviso de Validade** | Nota sobre expiração de 5 minutos | Footer note |
| **Instruções de Uso** | Como escanear e usar o QR code | Label instructions |
| **Filtro por IDs** | `?equipment_ids=1,2,3` para equipamentos específicos | Query param |
| **Filtro por Instalação** | `?facility_id=1` para toda a instalação | Query param |
| **Nome de Arquivo** | `etiquetas_{facility_name}.pdf` | Content-Disposition |

---

## 🔌 API Admin

### Endpoints

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| **Token de Equipamento** | GET | `/admin-api/equipment/<id>/qr-token/` |
| **Gerar Token Temporário** | GET | `/admin-api/equipment/<id>/generate-temp-token/` |
| **PDF de Etiquetas** | GET | `/admin-api/equipment/generate-labels-pdf/` |

### Características

| Funcionalidade | Detalhes |
|----------------|----------|
| **Resposta JSON** | Todas as APIs retornam JSON (`application/json`) |
| **Verificação de Permissões** | Requer autenticação e permissões |

---

## ⚙️ Comandos de Gerenciamento

### Comandos Disponíveis

| Comando | Uso | Opções |
|---------|-----|--------|
| **Gerar QR Codes** | `python manage.py generate_qr_codes` | `--equipment-id`, `--facility-id`, `--output-dir`, `--base-url`, `--size` |
| **Enviar Alertas Atrasados** | `python manage.py send_overdue_alerts` | `--dry-run` |
| **Enviar Relatórios de Conformidade** | `python manage.py send_compliance_reports` | `--dry-run` |

---

## 🔒 Segurança

### Tokens

| Funcionalidade | Detalhes |
|----------------|----------|
| **Tokens HMAC-SHA256** | Assinatura criptográfica para 5 min (`tokens.generate_expirable_token()`) |
| **Validação de Expiração** | Verifica timestamp antes de aceitar (`tokens.validate_expirable_token()`) |
| **Formato de Token** | `equipment_id:expiry:signature` |
| **Rastreamento de IP** | Registra IP em TemporaryTokenLog (`ip_address`) |
| **Contagem de Acessos** | Rastreia quantas vezes token foi acessado (`times_accessed`) |

### CSRF

| Funcionalidade | Detalhes |
|----------------|----------|
| **Proteção CSRF** | Ativada em todos os formulários (CSRF middleware) |
| **CSRF Exempt Público** | Endpoints públicos isentos para mobile (`@csrf_exempt`) |
| **Verificação de Assinatura** | Webhooks Stripe verificados via assinatura |

### Permissões

| Funcionalidade | Detalhes |
|----------------|----------|
| **Filtragem por Queryset** | Admin filtra dados baseado em instalações do usuário (`get_queryset` override) |
| **Controle de Campos** | Dropdown de instalação limitado ao usuário (`formfield_for_foreignkey`) |
| **Permissões de Mudança** | Gestores só editam suas instalações (`has_change_permission`) |
| **Permissões de Exclusão** | Gestores só excluem suas instalações (`has_delete_permission`) |

### Validação de Dados

| Funcionalidade | Detalhes |
|----------------|----------|
| **Validação de Foto** | Formato/tamanho/tipo de arquivo |
| **Limpeza de Notas** | Remove espaços/newlines extras (`notes` field `clean()`) |
| **Unicidade de Serial** | Número de série único por equipamento (`unique=True`) |
| **Email Único** | Um email por usuário (`unique=True`) |

---

## 🚀 Configuração e Deploy

### Variáveis de Ambiente

| Variável | Descrição |
|----------|-----------|
| **SECRET_KEY** | Chave secreta do Django |
| **DEBUG** | Modo de desenvolvimento |
| **DATABASE_URL** | URL do banco de dados |
| **RESEND_API_KEY** | Chave da API Resend |
| **STRIPE_TEST_SECRET_KEY** | Chave Stripe modo teste |
| **STRIPE_LIVE_SECRET_KEY** | Chave Stripe produção |
| **DJSTRIPE_WEBHOOK_SECRET** | Segredo webhook Stripe |

### Deploy para Produção

| Passo | Comando/Ação |
|-------|--------------|
| **Coletar Arquivos Estáticos** | `python manage.py collectstatic` |
| **Configurar PostgreSQL** | Alterar `DATABASES` em settings |
| **Configurar ALLOWED_HOSTS** | Adicionar domínio de produção |
| **Usar HTTPS** | Ativar `SECURE_SSL_REDIRECT` |
| **AWS S3 para Mídia** | `django-storages` + `boto3` (opcional) |
| **Gunicorn** | Servidor WSGI para produção |
| **WhiteNoise** | Servir arquivos estáticos (middleware) |

---

## 📈 Logs e Auditoria

### Rastreamento

| Funcionalidade | Modelo/Campo |
|----------------|--------------|
| **Log de Tokens Temporários** | `TemporaryTokenLog` model |
| **Log de Limpezas** | `CleaningLog` model |
| **Timestamps de Criação** | `created_at` (auto-added) |
| **Timestamps de Atualização** | `updated_at` (auto-updated) |
| **Rastreamento de IP** | `ip_address` em token logs |

---

## 📝 Modelos de Dados

### Relacionamentos Principais

```
User (Custom) ─┬─→ Account (M:M via managed_facilities)
               ├─→ CleaningLog (cleaned_by)
               ├─→ TemporaryTokenLog (created_by)
               └─→ Facility (M:M managers)

Facility ─┬─→ Equipment (1:M)
          └─→ User (M:M managers)

Equipment ─┬─→ Facility (M:1)
           └─→ CleaningLog (1:M)

CleaningLog ─┬─→ Equipment (M:1)
             └─→ User (cleaned_by)

TemporaryTokenLog ─┬─→ Equipment (M:1)
                   └─→ User (created_by)
```

### Campos Especiais

| Campo | Modelos | Tipo |
|-------|---------|------|
| **is_active** | Equipment, Facility, Account | Soft delete |
| **created_at** | Todos | Auto timestamp |
| **updated_at** | Todos | Auto timestamp |
| **stripe_customer_id** | Facility, Account | Integração Stripe |
| **public_token** | Equipment | Token permanente |
| **token_created_at** | Equipment | Timestamp de geração |

---

## 🎯 Casos de Uso Comuns

### 1. Registrar Limpeza via QR Code

1. Escaneie QR code com celular
2. Abra link no navegador
3. Tire foto do equipamento limpo
4. Adicione notas (opcional)
5. Clique em "Registrar Limpeza"
6. Veja confirmação de sucesso

### 2. Gerar Etiquetas para Impressão

```bash
# Via navegador
http://localhost:8000/equipment/labels/pdf/1/

# Via comando
python manage.py generate_qr_codes --facility-id=1 --output-dir=labels/
```

### 3. Enviar Relatório de Conformidade

```bash
# Produção
python manage.py send_compliance_reports

# Teste
python manage.py send_compliance_reports --dry-run
```

### 4. Gerenciar Acessos de Gestores

1. Vá para User admin
2. Selecione gestor
3. Adicione instalações em "Managed Facilities"
4. Gestor só verá dados dessas instalações

---

## 📞 Suporte

**Documentação Completa:** Este guia
**Logs de Auditoria:** TemporaryTokenLog, CleaningLog
**Comandos de Teste:** Use `--dry-run` em todos os comandos

---

**Desenvolvido com Django 5.0.6 | Python 3.12**
**Última Atualização:** 2025-11-23
