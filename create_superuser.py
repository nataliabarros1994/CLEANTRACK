#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cleantrack.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

email = 'admin@cleantrack.com'
password = 'admin'
username = 'admin'

if User.objects.filter(email=email).exists():
    print(f'User with email {email} already exists!')
else:
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name='Admin',
        last_name='User'
    )
    print(f'Superuser created successfully!')
    print(f'Email: {email}')
    print(f'Password: {password}')
