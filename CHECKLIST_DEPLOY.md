# ✅ Checklist de Deploy - CleanTrack Landing Page

Use este checklist para garantir que tudo está configurado antes de divulgar sua landing page.

---

## 📋 FASE 1: Configurações Obrigatórias

### ☐ 1. Configurar Calendly (5 minutos)

**Passo a passo:**
1. [ ] Acesse [calendly.com](https://calendly.com) e crie conta gratuita
2. [ ] Clique em "+ New Event Type"
3. [ ] Configure:
   - Nome: "CleanTrack - Onboarding Piloto"
   - Duração: 30 minutos
   - Descrição: "Sessão exclusiva para conhecer o CleanTrack e iniciar seu período de teste gratuito"
4. [ ] Copie o link de agendamento (ex: `https://calendly.com/joaosilva/cleantrack-onboarding`)
5. [ ] Abra o arquivo `index.html`
6. [ ] Na **linha 170**, substitua:
   ```html
   ANTES: data-url="https://calendly.com/seu-usuario/cleantrack-onboarding"
   DEPOIS: data-url="https://calendly.com/SEU-LINK-REAL/cleantrack-onboarding"
   ```
7. [ ] Salve o arquivo

**Testar:** Abra o index.html localmente e veja se o calendário aparece.

---

### ☐ 2. Configurar Formspree (3 minutos)

**Passo a passo:**
1. [ ] Acesse [formspree.io](https://formspree.io) e crie conta gratuita
2. [ ] Clique em "+ New Form"
3. [ ] Nome do formulário: "CleanTrack - Leads Piloto"
4. [ ] Copie o endpoint (ex: `https://formspree.io/f/xwpkabcd`)
5. [ ] Abra o arquivo `index.html`
6. [ ] Na **linha 264**, substitua:
   ```html
   ANTES: action="https://formspree.io/f/seu-form-id"
   DEPOIS: action="https://formspree.io/f/SEU-ID-REAL"
   ```
7. [ ] Salve o arquivo

**Configurar notificações no Formspree:**
1. [ ] Acesse "Settings" do formulário
2. [ ] Configure e-mail para receber notificações de novos leads
3. [ ] Ative notificações por e-mail

**Testar:** Envie um formulário de teste e veja se recebe o e-mail.

---

### ☐ 3. Atualizar Informações de Contato

**Abra o arquivo `index.html` e edite:**

**Linha 326-334 (Footer):**
1. [ ] E-mail:
   ```html
   ANTES: contato@cleantrack.com.br
   DEPOIS: seu-email-real@gmail.com
   ```

2. [ ] WhatsApp:
   ```html
   ANTES: (XX) XXXXX-XXXX
   DEPOIS: (11) 98765-4321  ← seu número real
   ```

3. [ ] Salve o arquivo

---

### ☐ 4. Links de Redes Sociais (Opcional)

**Linha 337-339 (Footer):**
1. [ ] LinkedIn: Substitua `#` pelo seu perfil
2. [ ] Instagram: Substitua `#` pelo seu perfil
3. [ ] YouTube: Substitua `#` pelo seu canal

**OU remova** se ainda não tiver redes sociais:
```html
<!-- Comentar estas linhas se não tiver redes sociais ainda
<div class="mt-3">
  <a href="#" class="text-white me-3"><i class="bi bi-linkedin fs-4"></i></a>
  <a href="#" class="text-white me-3"><i class="bi bi-instagram fs-4"></i></a>
  <a href="#" class="text-white"><i class="bi bi-youtube fs-4"></i></a>
</div>
-->
```

---

### ☐ 5. Link do Vídeo Demo (Opcional)

Se você tiver um vídeo demonstrativo do CleanTrack:

**Linha 107:**
1. [ ] Faça upload do vídeo no YouTube
2. [ ] Copie o link
3. [ ] Substitua:
   ```html
   ANTES: href="https://youtu.be/demo-cleantrack"
   DEPOIS: href="https://youtu.be/SEU-VIDEO-ID"
   ```

**OU remova o botão** se não tiver vídeo ainda:
```html
<!-- Comentar se não tiver vídeo demo
<a href="https://youtu.be/demo-cleantrack" class="btn btn-outline-secondary btn-lg" target="_blank">
  <i class="bi bi-play-circle"></i> Assistir Demo
</a>
-->
```

---

## 📋 FASE 2: Testes Locais

### ☐ 6. Testar Localmente

1. [ ] Abra o arquivo `index.html` no navegador
2. [ ] Verifique se o calendário Calendly carrega
3. [ ] Teste o formulário de contato (envie dados de teste)
4. [ ] Verifique se recebeu o e-mail do Formspree
5. [ ] Teste em mobile:
   - Abra DevTools (F12)
   - Clique no ícone de celular
   - Teste em iPhone e Android
6. [ ] Verifique todos os links (redes sociais, vídeo demo)
7. [ ] Confirme que todos os textos estão corretos

---

## 📋 FASE 3: Deploy no Netlify

### ☐ 7. Deploy via Drag & Drop

1. [ ] Acesse [app.netlify.com/drop](https://app.netlify.com/drop)
2. [ ] Faça login (ou crie conta com GitHub/Google)
3. [ ] Arraste a pasta `CleanTrack` para o site
4. [ ] Aguarde o deploy (10-30 segundos)
5. [ ] Copie a URL gerada (ex: `https://random-name-123.netlify.app`)

### ☐ 8. Personalizar Nome do Site

1. [ ] No painel do Netlify, clique em "Site settings"
2. [ ] Clique em "Change site name"
3. [ ] Escolha um nome:
   - `cleantrack-brasil`
   - `cleantrack-piloto`
   - `cleantrack-app`
4. [ ] Nova URL: `https://cleantrack-brasil.netlify.app`

### ☐ 9. Configurar Domínio Próprio (Opcional)

Se você tiver um domínio (ex: `cleantrack.com.br`):

1. [ ] No Netlify: "Domain settings" > "Add custom domain"
2. [ ] Digite seu domínio
3. [ ] Configure DNS conforme instruções do Netlify
4. [ ] Aguarde propagação (até 24h)

---

## 📋 FASE 4: Testes no Ar

### ☐ 10. Testar Site Publicado

1. [ ] Acesse a URL do Netlify
2. [ ] Teste em diferentes dispositivos:
   - [ ] Desktop (Chrome)
   - [ ] Desktop (Firefox/Safari)
   - [ ] Celular (Chrome Android)
   - [ ] Celular (Safari iOS)
3. [ ] Teste o agendamento Calendly
4. [ ] Envie formulário de teste
5. [ ] Verifique se recebeu e-mail do Formspree
6. [ ] Clique em todos os links
7. [ ] Teste scroll suave entre seções

---

## 📋 FASE 5: SEO e Analytics (Recomendado)

### ☐ 11. Google Analytics (Opcional)

1. [ ] Crie conta em [analytics.google.com](https://analytics.google.com)
2. [ ] Crie propriedade "CleanTrack Landing Page"
3. [ ] Copie o código de tracking
4. [ ] Adicione antes do `</head>` no index.html:
   ```html
   <!-- Google Analytics -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', 'G-XXXXXXXXXX');
   </script>
   ```
5. [ ] Faça novo deploy no Netlify

### ☐ 12. Meta Tags para Redes Sociais

Adicione antes do `</head>` no index.html:

```html
<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://cleantrack-brasil.netlify.app/">
<meta property="og:title" content="CleanTrack - Conformidade Médica Automatizada">
<meta property="og:description" content="Automatize registros de limpeza de equipamentos médicos. Teste grátis por 3 meses.">
<meta property="og:image" content="https://cleantrack-brasil.netlify.app/og-image.jpg">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://cleantrack-brasil.netlify.app/">
<meta property="twitter:title" content="CleanTrack - Conformidade Médica Automatizada">
<meta property="twitter:description" content="Automatize registros de limpeza de equipamentos médicos. Teste grátis por 3 meses.">
<meta property="twitter:image" content="https://cleantrack-brasil.netlify.app/og-image.jpg">
```

---

## 📋 FASE 6: Divulgação

### ☐ 13. Preparar Material de Divulgação

1. [ ] Copie a URL final do site
2. [ ] Faça screenshots do site para posts
3. [ ] Prepare textos para divulgação:

**LinkedIn:**
```
🚀 Lançando o CleanTrack!

Solução para automatizar registros de limpeza de equipamentos médicos.

✅ Conformidade ANVISA
✅ Relatórios em 1 clique
✅ Mobile-first

Programa Piloto: 10 vagas gratuitas por 3 meses.

Agende uma demo: [SEU-LINK]

#SaúdeDigital #GestãoHospitalar #Tecnologia
```

**WhatsApp:**
```
Olá! 👋

Estou lançando o CleanTrack, uma solução para automatizar registros de limpeza de equipamentos médicos.

Estou oferecendo 10 vagas no programa piloto (3 meses grátis + suporte dedicado).

Quer conhecer? [SEU-LINK]
```

### ☐ 14. Canais de Divulgação

- [ ] LinkedIn (poste + compartilhe em grupos de gestão hospitalar)
- [ ] WhatsApp (grupos de profissionais da saúde)
- [ ] E-mail (contatos diretos de clínicas/hospitais)
- [ ] Grupos no Facebook de gestores de saúde
- [ ] Fóruns especializados

---

## 📋 FASE 7: Acompanhamento

### ☐ 15. Monitorar Leads

**Diariamente:**
- [ ] Verificar e-mails do Formspree
- [ ] Verificar agendamentos no Calendly
- [ ] Responder em até 24h

**Semanalmente:**
- [ ] Ver estatísticas no Google Analytics
- [ ] Ajustar mensagens se conversão baixa

**Mensalmente:**
- [ ] Avaliar taxa de conversão (visitantes → leads → clientes)
- [ ] Coletar feedback dos primeiros clientes

---

## 📊 Métricas de Sucesso

**Metas para os primeiros 30 dias:**
- [ ] 100+ visitantes
- [ ] 20+ formulários preenchidos
- [ ] 10 agendamentos realizados
- [ ] 5-10 clientes piloto confirmados

---

## 🆘 Troubleshooting

### Problema: Calendly não aparece
- Verifique a URL na linha 170
- Teste a URL diretamente no navegador
- Limpe cache (Ctrl + Shift + R)

### Problema: Formulário não envia
- Verifique endpoint do Formspree (linha 264)
- Veja console do navegador (F12)
- Confirme que não excedeu 50 envios/mês (plano free)

### Problema: Site não carrega no Netlify
- Verifique logs em "Deploys"
- Confirme que index.html está na raiz da pasta
- Tente fazer redeploy

### Problema: CSS quebrado
- Verifique conexão com CDN do Bootstrap
- Teste em navegador anônimo
- Limpe cache do Netlify: Site Settings > Build & Deploy > Clear cache

---

## 📞 Suporte

**Documentação:**
- Netlify: [docs.netlify.com](https://docs.netlify.com)
- Calendly: [help.calendly.com](https://help.calendly.com)
- Formspree: [help.formspree.io](https://help.formspree.io)

**Comunidades:**
- Netlify Community: [answers.netlify.com](https://answers.netlify.com)
- Stack Overflow (tag: netlify, formspree, calendly)

---

## ✅ Checklist Final

Antes de compartilhar o link:

- [ ] Calendly configurado e funcionando
- [ ] Formspree configurado e testado
- [ ] E-mail e WhatsApp reais no footer
- [ ] Links de redes sociais corretos (ou removidos)
- [ ] Site testado em mobile e desktop
- [ ] Formulário testado e recebendo e-mails
- [ ] URL personalizada no Netlify
- [ ] Google Analytics instalado (opcional)
- [ ] Meta tags para redes sociais (opcional)

---

## 🎯 Próximos Passos Após 10 Clientes Piloto

1. **Coletar Feedback:**
   - O que funcionou bem?
   - Quais problemas enfrentaram?
   - Que recursos faltaram?

2. **Desenvolver MVP:**
   - Backend da API (conforme sua documentação)
   - App mobile para técnicos
   - Dashboard administrativo

3. **Pricing:**
   - Definir planos (ex: R$ 200/mês até 50 equipamentos)
   - Oferecer desconto para clientes piloto

4. **Escalar:**
   - Automatizar onboarding
   - Criar tutoriais em vídeo
   - Implementar chat de suporte

---

**Boa sorte com o lançamento! 🚀**

---

_Última atualização: 2025-11-23_
