# 🚀 Deploy CleanTrack AGORA - 3 Comandos

## ⚡ DEPLOY RÁPIDO (10 minutos)

### Passo 1: Push para GitHub (2 min)

**Abra o terminal e execute:**

```bash
cd /home/nataliabarros1994/Desktop/CleanTrack

# Se ainda não adicionou o remote:
git remote add origin https://github.com/SEU-USUARIO/cleantrack-backend.git

# Push
git push -u origin main
```

**IMPORTANTE:** Substitua `SEU-USUARIO` pelo seu username do GitHub!

Se pedir credenciais:
- Username: seu-usuario-github
- Password: [Personal Access Token - não a senha]

---

### Passo 2: Deploy no Render (5 min)

1. **Abrir:** https://dashboard.render.com
2. **Login** com GitHub
3. **New +** (canto superior direito)
4. **Blueprint**
5. **Conectar** ao repositório `cleantrack-backend`
6. **Apply**
7. **Aguardar** 3-5 minutos

**Render criará automaticamente:**
- ✅ PostgreSQL database
- ✅ Django web service
- ✅ Variáveis de ambiente

---

### Passo 3: Configurar SECRET_KEY (2 min)

```
1. Render > cleantrack-api > Environment
2. Editar: SECRET_KEY
3. Colar: rv2o%rw13na2+j3zsciqqu4pfu_fw=jv05c1%0ivauwgi&u7v5
4. Save
5. Aguardar redeploy (1 min)
```

---

### Passo 4: Criar Superuser (1 min)

```
1. Render > cleantrack-api > Shell
2. Executar:
   python manage.py createsuperuser

3. Preencher:
   Username: admin
   Email: natalia@email.com
   Password: (senha forte)
```

---

## ✅ PRONTO! Acesse:

**Admin:** https://cleantrack-api.onrender.com/admin/
- Username: admin
- Password: (a que você criou)

**API:** https://cleantrack-api.onrender.com/api/

---

## 🎯 Próximo: Landing Page (5 min)

### Passo 5: Deploy Landing Page

```
1. Abrir: https://app.netlify.com/drop
2. Arrastar pasta CleanTrack
3. Aguardar upload
4. Pronto! URL: https://nome-aleatorio.netlify.app
```

**Antes de arrastar, configure:**

1. **Editar index.html:**

**Linha 170 (Calendly):**
- Se não tiver Calendly ainda, comente estas linhas:
```html
<!-- Calendly temporariamente desabilitado
<div class="calendly-inline-widget" data-url="..."></div>
-->
```

**Linha 264 (Formspree):**
- Crie conta: https://formspree.io
- Copie ID do form
- Cole no action

---

## 📝 Credenciais para Teste

### Após deploy, você terá:

**Backend (Django Admin):**
```
URL: https://cleantrack-api.onrender.com/admin/
Username: admin
Password: [sua senha]
```

**Criar Usuário de Teste:**
```
1. Admin > Facilities > Add Facility
   - Nome: Hospital Teste
   - Salvar

2. Admin > Users > Add User
   - Username: tecnico1
   - Email: tecnico@teste.com
   - Password: teste123
   - Facility: Hospital Teste
   - Role: Technician

3. Admin > Equipment > Add Equipment
   - Nome: Ultrassom Portátil
   - Serial: US-001
   - Facility: Hospital Teste
   - Gerar QR Code
```

**Testar Fluxo:**
```
1. Copiar QR code token
2. Acessar: https://cleantrack-api.onrender.com/log/{token}
3. Preencher formulário de limpeza
4. Upload foto
5. Submeter
6. Ver no dashboard
```

---

## 🔧 Troubleshooting

### "Permission denied" no git push:
```bash
git remote set-url origin https://github.com/SEU-USUARIO/cleantrack-backend.git
git push -u origin main
```

### Build falha no Render:
```
1. Ver logs: Render > Logs
2. Verificar requirements.txt existe
3. Manual rebuild
```

### Admin sem CSS:
```
Aguardar deploy completo (collectstatic demora 1-2 min)
```

---

## 📞 URLs Finais

Após seguir todos os passos:

```
Landing Page: https://cleantrack-[seu-nome].netlify.app
Backend API: https://cleantrack-api.onrender.com
Admin: https://cleantrack-api.onrender.com/admin/
```

**Compartilhe estas URLs comigo para eu testar!** 🎉

---

_Tempo total: ~20 minutos_
_Custo: R$ 0 (tudo free tier)_
