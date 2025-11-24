#!/usr/bin/env python
"""
Generate printable QR codes with permanent tokens
Run: docker-compose exec web python generate_permanent_qr_codes.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cleantrack.settings')
django.setup()

from apps.equipment.models import Equipment

print("=" * 70)
print("GERANDO QR CODES COM TOKENS PERMANENTES")
print("=" * 70)
print()

equipment_list = Equipment.objects.filter(is_active=True).select_related('facility')

print(f"📋 Encontrados {equipment_list.count()} equipamentos ativos\n")

html_parts = ["""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Codes - Tokens Permanentes - CleanTrack</title>
    <style>
        @page {
            size: A4;
            margin: 20mm;
        }

        @media print {
            .no-print {
                display: none;
            }
            .page-break {
                page-break-after: always;
            }
        }

        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
        }

        .qr-card {
            background: white;
            border: 3px solid #333;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }

        .qr-card h2 {
            color: #667eea;
            margin: 0 0 10px 0;
            font-size: 24px;
        }

        .qr-card .facility {
            color: #666;
            font-size: 14px;
            margin-bottom: 20px;
        }

        .qr-card img {
            width: 300px;
            height: 300px;
            border: 2px solid #ddd;
            border-radius: 5px;
            margin: 20px auto;
        }

        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 20px;
            text-align: left;
        }

        .info-item {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            font-size: 12px;
        }

        .info-item strong {
            color: #667eea;
            display: block;
            margin-bottom: 5px;
        }

        .token-display {
            background: #fff3cd;
            border: 2px dashed #ffc107;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            font-family: monospace;
            word-break: break-all;
            font-size: 14px;
        }

        .instructions {
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 5px;
        }

        .instructions h3 {
            margin-top: 0;
            color: #2196F3;
        }

        .instructions ol {
            margin: 10px 0;
            padding-left: 20px;
        }

        .instructions li {
            margin: 8px 0;
        }

        .btn-print {
            background: #667eea;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            margin: 20px 0;
        }

        .btn-print:hover {
            background: #5568d3;
        }

        .warning {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }

        .warning strong {
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔒 QR Codes - Tokens Permanentes</h1>
        <p>CleanTrack - Sistema de Gestão de Conformidade</p>
    </div>

    <div class="no-print">
        <div class="instructions">
            <h3>📋 Instruções de Impressão</h3>
            <ol>
                <li><strong>Configure a impressora:</strong> Papel A4, orientação retrato</li>
                <li><strong>Clique no botão "Imprimir" abaixo</strong></li>
                <li><strong>Corte os QR codes</strong> com margem de segurança</li>
                <li><strong>Cole nos equipamentos</strong> em local visível e protegido</li>
                <li><strong>Proteja com plástico transparente</strong> para durabilidade</li>
            </ol>
        </div>

        <div class="warning">
            <strong>⚠️ IMPORTANTE:</strong> Estes QR codes contêm tokens permanentes.
            Qualquer pessoa com acesso ao QR code pode registrar limpezas.
            Guarde este documento de forma segura.
        </div>

        <center>
            <button class="btn-print" onclick="window.print()">🖨️ Imprimir QR Codes</button>
        </center>
    </div>
"""]

for i, equipment in enumerate(equipment_list, 1):
    # Get QR code URL
    qr_url = equipment.qr_code.url if equipment.qr_code else None
    token = equipment.public_token
    url = f"http://localhost:8000/log/{token}/"

    print(f"{i}. {equipment.name}")
    print(f"   Token: {token}")
    print(f"   URL: {url}")
    print(f"   QR Code: {qr_url or 'Not generated'}")
    print()

    # Add page break before each equipment (except first)
    page_break_class = "page-break" if i > 1 else ""

    html_parts.append(f"""
    <div class="qr-card {page_break_class}">
        <h2>{equipment.name}</h2>
        <div class="facility">📍 {equipment.facility.name}</div>

        {f'<img src="{qr_url}" alt="QR Code">' if qr_url else '<p>⚠️ QR Code não gerado</p>'}

        <div class="info-grid">
            <div class="info-item">
                <strong>Número de Série</strong>
                {equipment.serial_number}
            </div>
            <div class="info-item">
                <strong>Frequência de Limpeza</strong>
                {dict(equipment.CLEANING_FREQUENCIES).get(equipment.cleaning_frequency_hours, 'N/A')}
            </div>
            <div class="info-item">
                <strong>ID do Equipamento</strong>
                #{equipment.id}
            </div>
            <div class="info-item">
                <strong>Status</strong>
                {'✅ Ativo' if equipment.is_active else '❌ Inativo'}
            </div>
        </div>

        <div class="token-display">
            <strong>🔑 Token Permanente:</strong><br>
            {token}<br><br>
            <strong>🔗 URL de Acesso:</strong><br>
            {url}
        </div>
    </div>
    """)

html_parts.append("""
    <div class="no-print" style="text-align: center; margin-top: 40px; padding: 20px; background: white; border-radius: 10px;">
        <h3>✅ Documento Gerado com Sucesso</h3>
        <p>Total de QR codes: """ + str(equipment_list.count()) + """</p>
        <p>Data de geração: """ + str(django.utils.timezone.now().strftime('%d/%m/%Y %H:%M:%S')) + """</p>
    </div>
</body>
</html>
""")

html_content = ''.join(html_parts)

# Save HTML file
output_file = 'QR_CODES_PERMANENTES.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("=" * 70)
print(f"✅ Arquivo gerado: {output_file}")
print(f"📄 Total de QR codes: {equipment_list.count()}")
print()
print("Para visualizar e imprimir:")
print(f"  1. Abra o arquivo no navegador: file://{os.path.abspath(output_file)}")
print("  2. Clique no botão 'Imprimir QR Codes'")
print("  3. Configure impressora: A4, retrato")
print("=" * 70)
