#!/usr/bin/env python
"""
Script para verificar e criar/atualizar o usuário Natália
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cleantrack.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Dados do usuário
email = 'natyssis23@gmail.com'
username = 'admin123'
password = 'admin'  # ALTERE PARA SUA SENHA REAL!
first_name = 'Natalia'
last_name = 'Barros'

print("=" * 60)
print("VERIFICAÇÃO E CRIAÇÃO DE USUÁRIO")
print("=" * 60)

# Verificar se usuário existe por email
user_by_email = User.objects.filter(email=email).first()
user_by_username = User.objects.filter(username=username).first()

if user_by_email:
    print(f"\n✓ Usuário encontrado por EMAIL: {email}")
    print(f"  - ID: {user_by_email.id}")
    print(f"  - Username: {user_by_email.username}")
    print(f"  - Nome: {user_by_email.get_full_name()}")
    print(f"  - Is superuser: {user_by_email.is_superuser}")
    print(f"  - Is staff: {user_by_email.is_staff}")
    print(f"  - Is active: {user_by_email.is_active}")

    # Atualizar senha
    print(f"\n🔄 Atualizando senha...")
    user_by_email.set_password(password)
    user_by_email.is_superuser = True
    user_by_email.is_staff = True
    user_by_email.is_active = True
    user_by_email.save()
    print("✓ Senha atualizada com sucesso!")

elif user_by_username:
    print(f"\n✓ Usuário encontrado por USERNAME: {username}")
    print(f"  - ID: {user_by_username.id}")
    print(f"  - Email: {user_by_username.email}")
    print(f"  - Nome: {user_by_username.get_full_name()}")

    # Atualizar email e senha
    print(f"\n🔄 Atualizando email e senha...")
    user_by_username.email = email
    user_by_username.set_password(password)
    user_by_username.is_superuser = True
    user_by_username.is_staff = True
    user_by_username.is_active = True
    user_by_username.save()
    print("✓ Email e senha atualizados com sucesso!")

else:
    print(f"\n⚠️  Usuário NÃO encontrado. Criando novo...")
    user = User.objects.create_superuser(
        email=email,
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    print(f"✓ Superusuário criado com sucesso!")
    print(f"  - ID: {user.id}")
    print(f"  - Email: {user.email}")
    print(f"  - Username: {user.username}")

print("\n" + "=" * 60)
print("CREDENCIAIS DE LOGIN")
print("=" * 60)
print(f"URL: http://127.0.0.1:8000/admin/")
print(f"Email: {email}")
print(f"Senha: {password}")
print("\n⚠️  IMPORTANTE: Você pode logar usando EMAIL ou USERNAME")
print("=" * 60)
