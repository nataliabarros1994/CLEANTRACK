from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    """
    Homepage simples mostrando que o CleanTrack está rodando
    """
    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CleanTrack - Sistema de Gestão de Limpeza</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 60px 40px;
                max-width: 600px;
                text-align: center;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                color: #667eea;
                font-size: 3em;
                margin-bottom: 20px;
            }
            .status {
                display: inline-block;
                background: #10b981;
                color: white;
                padding: 10px 20px;
                border-radius: 50px;
                font-weight: bold;
                margin: 20px 0;
                font-size: 1.1em;
            }
            .status::before {
                content: "✓ ";
                font-size: 1.3em;
            }
            p {
                color: #666;
                font-size: 1.2em;
                line-height: 1.8;
                margin: 20px 0;
            }
            .links {
                margin-top: 40px;
                display: flex;
                gap: 20px;
                justify-content: center;
                flex-wrap: wrap;
            }
            .btn {
                display: inline-block;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 10px;
                font-weight: bold;
                transition: all 0.3s;
            }
            .btn-primary {
                background: #667eea;
                color: white;
            }
            .btn-primary:hover {
                background: #5568d3;
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102,126,234,0.3);
            }
            .btn-secondary {
                background: #f3f4f6;
                color: #667eea;
            }
            .btn-secondary:hover {
                background: #e5e7eb;
            }
            .info {
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
                border-left: 4px solid #667eea;
            }
            .info p {
                font-size: 0.9em;
                color: #555;
                margin: 5px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>CleanTrack</h1>
            <div class="status">Servidor Online</div>
            <p>Sistema de Gestão de Limpeza de Equipamentos Médicos</p>
            <p>O backend Django está rodando com sucesso!</p>

            <div class="links">
                <a href="/admin/" class="btn btn-primary">Acessar Painel Admin</a>
            </div>

            <div class="info">
                <p><strong>Credenciais de Acesso:</strong></p>
                <p>Email: admin@cleantrack.com</p>
                <p>Senha: admin</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)
