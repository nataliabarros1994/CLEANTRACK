#!/bin/bash

# Script de Teste Completo - Webhooks do Stripe
# Testa todos os 8 eventos implementados

set -e

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║        TESTE COMPLETO - 8 EVENTOS DE WEBHOOK                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Verificar se Stripe CLI está disponível
if ! command -v stripe &> /dev/null; then
    echo "❌ Stripe CLI não encontrado!"
    echo ""
    echo "Instale com:"
    echo "  - macOS: brew install stripe/stripe-cli/stripe"
    echo "  - Linux: https://stripe.com/docs/stripe-cli"
    echo ""
    exit 1
fi

echo "✅ Stripe CLI encontrado: $(stripe --version)"
echo ""

# Array de eventos
eventos=(
  "checkout.session.completed"
  "customer.subscription.created"
  "customer.subscription.updated"
  "customer.subscription.deleted"
  "invoice.payment_succeeded"
  "invoice.payment_failed"
  "customer.subscription.trial_will_end"
  "charge.refunded"
)

# Descrições dos eventos
declare -A descricoes
descricoes["checkout.session.completed"]="Ativa facility após pagamento"
descricoes["customer.subscription.created"]="Ativa facility quando subscription criada"
descricoes["customer.subscription.updated"]="Atualiza status da facility"
descricoes["customer.subscription.deleted"]="Desativa facility após cancelamento"
descricoes["invoice.payment_succeeded"]="Confirma facility ativa após pagamento"
descricoes["invoice.payment_failed"]="Desativa facility após 3 falhas"
descricoes["customer.subscription.trial_will_end"]="Alerta 3 dias antes do fim do trial"
descricoes["charge.refunded"]="Registra reembolso"

# Contador de sucessos
sucesso=0
falhas=0

# Loop pelos eventos
for i in "${!eventos[@]}"; do
  numero=$((i + 1))
  evento="${eventos[$i]}"
  descricao="${descricoes[$evento]}"

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Teste $numero/8: $evento"
  echo "Ação: $descricao"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Executar trigger
  if stripe trigger "$evento" > /dev/null 2>&1; then
    echo "✅ Evento enviado com sucesso"
    ((sucesso++))
  else
    echo "❌ Erro ao enviar evento"
    ((falhas++))
  fi

  echo ""

  # Aguardar entre eventos
  if [ $numero -lt 8 ]; then
    sleep 2
  fi
done

# Resumo final
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                      RESUMO DOS TESTES                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "  Total de eventos: 8"
echo "  ✅ Sucessos: $sucesso"
echo "  ❌ Falhas: $falhas"
echo ""

if [ $falhas -eq 0 ]; then
    echo "  🎉 TODOS OS TESTES FORAM EXECUTADOS COM SUCESSO!"
else
    echo "  ⚠️  Alguns testes falharam. Verifique a configuração."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PRÓXIMOS PASSOS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Verificar o terminal do Stripe listener:"
echo "   Deve ter 8x [200] POST /billing/webhook/stripe/"
echo ""
echo "2. Verificar logs do Django:"
echo "   docker-compose logs web | grep 'Handling'"
echo ""
echo "3. Verificar no Admin Django:"
echo "   http://localhost:8000/admin/facilities/facility/"
echo "   - Deve ter facilities criadas"
echo "   - stripe_customer_id preenchido"
echo "   - Status is_active variando conforme eventos"
echo ""
echo "4. Verificar no Django shell:"
echo "   docker-compose exec web python manage.py shell"
echo ""
echo "   from apps.facilities.models import Facility"
echo "   print(f'Total: {Facility.objects.count()}')"
echo "   for f in Facility.objects.all():"
echo "       print(f'{f.name} - Active: {f.is_active} - Customer: {f.stripe_customer_id}')"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Retornar código de saída baseado nas falhas
if [ $falhas -eq 0 ]; then
    exit 0
else
    exit 1
fi
