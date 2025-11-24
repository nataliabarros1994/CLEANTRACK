#!/bin/bash

# Script de Ativação do Webhook do Stripe - CleanTrack
# Uso: ./activate_stripe_webhook.sh

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║    🔔 ATIVAÇÃO DO WEBHOOK DO STRIPE - CLEANTRACK           ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Verificar se Stripe CLI está instalado
if ! command -v stripe &> /dev/null; then
    echo "❌ Stripe CLI não está instalado!"
    echo ""
    echo "Para instalar:"
    echo "  macOS:  brew install stripe/stripe-cli/stripe"
    echo "  Linux:  wget https://github.com/stripe/stripe-cli/releases/latest/download/stripe_*_linux_x86_64.tar.gz"
    echo ""
    exit 1
fi

echo "✅ Stripe CLI encontrado: $(stripe --version)"
echo ""

# Passo 1: Login no Stripe
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASSO 1: Login no Stripe"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Verificando status do login..."

if stripe config --list &> /dev/null; then
    echo "✅ Você já está logado no Stripe CLI"
else
    echo "⚠️  Você precisa fazer login no Stripe CLI"
    echo ""
    echo "Executando: stripe login"
    echo ""
    stripe login
fi

echo ""

# Passo 2: Verificar se o servidor Django está rodando
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASSO 2: Verificar Servidor Django"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo "✅ Servidor Django está rodando em http://localhost:8000"
else
    echo "⚠️  Servidor Django NÃO está rodando"
    echo ""
    echo "Por favor, inicie o servidor em outro terminal:"
    echo "  Com Docker:  docker-compose up"
    echo "  Sem Docker:  python manage.py runserver"
    echo ""
    read -p "Pressione ENTER quando o servidor estiver rodando..."
fi

echo ""

# Passo 3: Iniciar listener e capturar webhook secret
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASSO 3: Obter Webhook Secret"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Iniciando Stripe listener..."
echo ""

# Criar arquivo temporário para capturar output
TEMP_FILE=$(mktemp)

# Iniciar listener em background por 3 segundos para capturar secret
timeout 3s stripe listen --forward-to localhost:8000/billing/webhook/stripe/ > "$TEMP_FILE" 2>&1 || true

# Extrair o webhook secret do output
WEBHOOK_SECRET=$(grep -o "whsec_[a-zA-Z0-9]*" "$TEMP_FILE" | head -1)

if [ -z "$WEBHOOK_SECRET" ]; then
    echo "❌ Não foi possível obter o webhook secret automaticamente."
    echo ""
    echo "Por favor, execute manualmente em outro terminal:"
    echo "  stripe listen --forward-to localhost:8000/billing/webhook/stripe/"
    echo ""
    echo "Copie o 'whsec_...' que aparecer e execute:"
    echo "  nano .env"
    echo ""
    echo "Adicione a linha:"
    echo "  STRIPE_WEBHOOK_SECRET=whsec_seu_secret_aqui"
    rm "$TEMP_FILE"
    exit 1
fi

echo "✅ Webhook Secret obtido:"
echo "   $WEBHOOK_SECRET"
echo ""

# Limpar arquivo temp
rm "$TEMP_FILE"

# Passo 4: Atualizar .env
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASSO 4: Atualizar .env"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Fazer backup do .env
cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
echo "✅ Backup do .env criado"

# Atualizar ou adicionar STRIPE_WEBHOOK_SECRET
if grep -q "^STRIPE_WEBHOOK_SECRET=" .env; then
    # Substituir linha existente
    sed -i "s|^STRIPE_WEBHOOK_SECRET=.*|STRIPE_WEBHOOK_SECRET=$WEBHOOK_SECRET|" .env
    echo "✅ STRIPE_WEBHOOK_SECRET atualizado no .env"
else
    # Adicionar nova linha
    echo "" >> .env
    echo "STRIPE_WEBHOOK_SECRET=$WEBHOOK_SECRET" >> .env
    echo "✅ STRIPE_WEBHOOK_SECRET adicionado ao .env"
fi

echo ""

# Passo 5: Reiniciar servidor
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASSO 5: Reiniciar Servidor"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⚠️  Por favor, reinicie o servidor Django para carregar a nova configuração:"
echo ""
echo "  Com Docker:"
echo "    docker-compose restart web"
echo ""
echo "  Sem Docker:"
echo "    Ctrl+C no terminal do runserver e rodar novamente:"
echo "    python manage.py runserver"
echo ""

read -p "Pressione ENTER quando o servidor estiver reiniciado..."

echo ""

# Passo 6: Instruções finais
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASSO 6: Iniciar Listener Permanente"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Agora você precisa manter o listener rodando em um terminal separado:"
echo ""
echo "  stripe listen --forward-to localhost:8000/billing/webhook/stripe/"
echo ""
echo "Deixe este terminal aberto enquanto estiver desenvolvendo."
echo ""

# Passo 7: Testar
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASSO 7: Testar Webhooks"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Em um terceiro terminal, teste os webhooks:"
echo ""
echo "  stripe trigger checkout.session.completed"
echo "  stripe trigger invoice.payment_succeeded"
echo "  stripe trigger customer.subscription.deleted"
echo ""
echo "Verifique os logs:"
echo "  tail -f logs/cleantrack.log | grep billing"
echo ""

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                  ✅ CONFIGURAÇÃO COMPLETA!                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Resumo do que foi feito:"
echo "  ✅ Webhook secret obtido: $WEBHOOK_SECRET"
echo "  ✅ .env atualizado com STRIPE_WEBHOOK_SECRET"
echo "  ✅ Backup do .env criado"
echo ""
echo "Próximos passos:"
echo "  1. Inicie o listener: stripe listen --forward-to localhost:8000/billing/webhook/stripe/"
echo "  2. Teste com: stripe trigger checkout.session.completed"
echo "  3. Verifique logs: tail -f logs/cleantrack.log | grep billing"
echo ""
echo "Documentação completa: STRIPE_WEBHOOK_ACTIVATION.md"
echo ""
