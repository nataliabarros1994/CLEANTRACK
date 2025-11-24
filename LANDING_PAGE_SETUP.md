# CleanTrack - Landing Page Setup Guide

## Configuração Rápida (10 minutos)

### 1. Configurar Calendly

1. Crie uma conta gratuita em [Calendly.com](https://calendly.com)
2. Configure um evento chamado "CleanTrack - Onboarding"
3. Duração sugerida: 30 minutos
4. Copie o link de agendamento (ex: `https://calendly.com/seu-usuario/cleantrack-onboarding`)
5. No arquivo `index.html`, linha 156, substitua:
   ```html
   data-url="https://calendly.com/seu-usuario/cleantrack-onboarding"
   ```

### 2. Configurar Formspree

1. Crie conta gratuita em [Formspree.io](https://formspree.io)
2. Crie um novo formulário
3. Copie o endpoint (ex: `https://formspree.io/f/xwpkabcd`)
4. No arquivo `index.html`, linha 264, substitua:
   ```html
   action="https://formspree.io/f/seu-form-id"
   ```

### 3. Personalizar Informações de Contato

Edite o arquivo `index.html` na seção de Footer (linhas 326-334):
- E-mail: contato@cleantrack.com.br
- WhatsApp: (XX) XXXXX-XXXX
- Links de redes sociais (LinkedIn, Instagram, YouTube)

### 4. Adicionar Link do Vídeo Demo (Opcional)

Se você tiver um vídeo demonstrativo:
- Linha 107: substitua `https://youtu.be/demo-cleantrack` pelo link real do YouTube

---

## Deploy na Netlify (Recomendado)

### Opção A: Deploy via Git (Recomendado)

1. **Criar repositório Git:**
   ```bash
   cd /home/nataliabarros1994/Desktop/CleanTrack
   git init
   git add .
   git commit -m "Initial commit - CleanTrack landing page"
   ```

2. **Subir para GitHub:**
   - Crie um repositório em [GitHub.com](https://github.com/new)
   - Execute:
     ```bash
     git remote add origin https://github.com/seu-usuario/cleantrack-landing.git
     git branch -M main
     git push -u origin main
     ```

3. **Deploy no Netlify:**
   - Acesse [app.netlify.com](https://app.netlify.com)
   - Clique em "Add new site" > "Import an existing project"
   - Conecte ao GitHub e selecione o repositório
   - Deploy automático! URL: `https://seu-site.netlify.app`

### Opção B: Deploy Manual (Drag & Drop)

1. Acesse [app.netlify.com/drop](https://app.netlify.com/drop)
2. Arraste a pasta `CleanTrack` para a área de upload
3. Pronto! Netlify fornecerá uma URL instantaneamente

### Opção C: Deploy via CLI

```bash
# Instalar Netlify CLI
npm install -g netlify-cli

# Fazer login
netlify login

# Deploy
cd /home/nataliabarros1994/Desktop/CleanTrack
netlify deploy --prod
```

---

## Deploy Alternativo - Vercel

1. Instale Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Deploy:
   ```bash
   cd /home/nataliabarros1994/Desktop/CleanTrack
   vercel --prod
   ```

---

## Deploy Alternativo - Render

1. Crie conta em [render.com](https://render.com)
2. "New" > "Static Site"
3. Conecte ao GitHub ou faça upload manual
4. Configuração:
   - Build Command: (deixe vazio)
   - Publish Directory: `.`

---

## Checklist Pré-Lançamento

- [ ] Calendly configurado e link atualizado
- [ ] Formspree configurado e endpoint atualizado
- [ ] Informações de contato (e-mail, WhatsApp) atualizadas
- [ ] Link do vídeo demo atualizado (se disponível)
- [ ] Links de redes sociais atualizados
- [ ] Testado em mobile (Chrome DevTools)
- [ ] Testado formulário de contato
- [ ] Testado agendamento Calendly
- [ ] Site deployado e acessível

---

## Próximos Passos

### 1. Tracking & Analytics
Adicione Google Analytics ou Plausible para monitorar:
- Visitantes
- Taxa de conversão
- Origem do tráfego

### 2. SEO
- Configure meta tags Open Graph para compartilhamento em redes sociais
- Crie arquivo `sitemap.xml`
- Configure Google Search Console

### 3. Marketing
- Compartilhe em grupos de gestores de saúde no LinkedIn
- Participe de fóruns de gestão hospitalar
- Entre em contato direto com clínicas locais

---

## Estrutura de Arquivos

```
CleanTrack/
├── index.html              # Landing page principal
├── netlify.toml           # Configuração Netlify
├── LANDING_PAGE_SETUP.md  # Este arquivo
└── API_REST_DOCUMENTACAO_FASE2.md  # Documentação da API
```

---

## Suporte Técnico

**Problemas comuns:**

1. **Calendly não aparece:**
   - Verifique se o link está correto
   - Teste o link diretamente no navegador
   - Aguarde 2-3 segundos para o widget carregar

2. **Formspree não envia:**
   - Verifique o endpoint no console do navegador
   - Confirme que o plano gratuito não excedeu limite (50 envios/mês)

3. **Deploy falhou:**
   - Netlify: verifique logs em "Deploys"
   - Certifique-se que `index.html` está na raiz

---

## Melhorias Implementadas

A landing page criada inclui melhorias em relação ao template original:

- Navegação fixa responsiva
- Ícones Bootstrap Icons para melhor visual
- Seção de estatísticas impactantes
- Seção de benefícios expandida
- Formulário mais completo com campos adicionais
- Animações suaves de hover
- Footer expandido com informações de contato
- Smooth scroll entre seções
- Design mobile-first otimizado
- Badges e CTAs mais visíveis

---

## Custo Estimado

- **Netlify/Vercel:** Grátis (plano free)
- **Calendly:** Grátis (até 1 tipo de evento)
- **Formspree:** Grátis (até 50 envios/mês)
- **Total:** R$ 0/mês

---

**Boa sorte com o lançamento do CleanTrack!**
