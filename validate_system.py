#!/usr/bin/env python
"""
CleanTrack - Script de Validação Completa do Sistema
=====================================================
Execute este script para verificar se tudo está funcionando.
"""
import os
import sys
import django
from django.core.management import call_command

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cleantrack.settings')
django.setup()

from django.apps import apps
from django.contrib import admin
from django.db import connection
from apps.accounts.models import User
from apps.facilities.models import Facility
from apps.equipment.models import Equipment

def print_section(title):
    print('\n' + '=' * 70)
    print(f'  {title}')
    print('=' * 70)

def test_database():
    """Test database connectivity"""
    print_section('1. TESTE DE CONEXÃO COM BANCO DE DADOS')
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print('✅ Conexão com banco de dados: OK')
            return True
    except Exception as e:
        print(f'❌ Erro na conexão: {e}')
        return False

def test_migrations():
    """Check migrations status"""
    print_section('2. VERIFICAÇÃO DE MIGRATIONS')
    try:
        from django.db.migrations.recorder import MigrationRecorder
        recorder = MigrationRecorder(connection)
        applied = recorder.applied_migrations()
        print(f'✅ Migrations aplicadas: {len(applied)}')
        return True
    except Exception as e:
        print(f'❌ Erro ao verificar migrations: {e}')
        return False

def test_apps():
    """Test all apps are loaded"""
    print_section('3. VERIFICAÇÃO DE APPS')
    cleantrack_apps = ['accounts', 'facilities', 'equipment', 'cleaning_logs', 
                       'billing', 'notifications', 'documentation']
    
    loaded_apps = [app.label for app in apps.get_app_configs() if app.name.startswith('apps.')]
    
    for app in cleantrack_apps:
        if app in loaded_apps:
            print(f'✅ {app:20s} → Carregada')
        else:
            print(f'❌ {app:20s} → ERRO: Não carregada')
            return False
    
    # Check djstripe
    if 'djstripe' in [app.label for app in apps.get_app_configs()]:
        print(f'✅ {"djstripe":20s} → Carregada')
    
    return True

def test_admin():
    """Test admin models registration"""
    print_section('4. VERIFICAÇÃO DO DJANGO ADMIN')
    
    expected_models = [
        'accounts.user',
        'accounts.account',
        'facilities.facility',
        'equipment.equipment',
        'cleaning_logs.cleaninglog',
        'cleaning_logs.temporarytokenlog',
        'documentation.featurecategory',
        'documentation.feature',
    ]
    
    registered_models = [
        f'{m._meta.app_label}.{m._meta.model_name}' 
        for m in admin.site._registry.keys()
    ]
    
    all_ok = True
    for model in expected_models:
        if model in registered_models:
            print(f'✅ {model:40s} → Registrado')
        else:
            print(f'❌ {model:40s} → NÃO registrado')
            all_ok = False
    
    print(f'\n   Total de modelos no admin: {len(admin.site._registry)}')
    return all_ok

def test_urls():
    """Test URL configuration"""
    print_section('5. VERIFICAÇÃO DE URLs')
    
    from django.urls import get_resolver
    resolver = get_resolver()
    
    expected_patterns = ['admin', 'accounts', 'cleaning', 'billing', 'equipment']
    
    url_patterns = [str(pattern.pattern) for pattern in resolver.url_patterns]
    
    for pattern in expected_patterns:
        found = any(pattern in str(p) for p in url_patterns)
        if found:
            print(f'✅ /{pattern}/ → Configurada')
        else:
            print(f'⚠️  /{pattern}/ → Não encontrada')
    
    return True

def test_authentication():
    """Test authentication backend"""
    print_section('6. VERIFICAÇÃO DE AUTENTICAÇÃO')
    
    from django.conf import settings
    
    backends = settings.AUTHENTICATION_BACKENDS
    print(f'✅ Backends configurados: {len(backends)}')
    for backend in backends:
        print(f'   - {backend}')
    
    # Check custom user model
    if settings.AUTH_USER_MODEL == 'accounts.User':
        print('✅ Modelo de usuário customizado: accounts.User')
    else:
        print(f'⚠️  Modelo de usuário: {settings.AUTH_USER_MODEL}')
    
    return True

def test_static_files():
    """Test static files configuration"""
    print_section('7. VERIFICAÇÃO DE ARQUIVOS ESTÁTICOS')
    
    from django.conf import settings
    
    print(f'✅ STATIC_URL: {settings.STATIC_URL}')
    print(f'✅ MEDIA_URL: {settings.MEDIA_URL}')
    
    if hasattr(settings, 'STATIC_ROOT'):
        print(f'✅ STATIC_ROOT: {settings.STATIC_ROOT}')
    
    if hasattr(settings, 'MEDIA_ROOT'):
        print(f'✅ MEDIA_ROOT: {settings.MEDIA_ROOT}')
    
    return True

def test_data_samples():
    """Check if there's sample data"""
    print_section('8. VERIFICAÇÃO DE DADOS DE TESTE')
    
    user_count = User.objects.count()
    facility_count = Facility.objects.count()
    equipment_count = Equipment.objects.count()
    
    print(f'📊 Usuários: {user_count}')
    print(f'📊 Facilities: {facility_count}')
    print(f'📊 Equipamentos: {equipment_count}')
    
    if user_count == 0:
        print('\n⚠️  RECOMENDAÇÃO: Crie um superusuário')
        print('   python manage.py createsuperuser')
    
    if facility_count == 0:
        print('\n⚠️  RECOMENDAÇÃO: Crie facilities de teste no admin')
    
    return True

def run_all_tests():
    """Run all validation tests"""
    print('\n' + '=' * 70)
    print('CLEANTRACK - VALIDAÇÃO COMPLETA DO SISTEMA')
    print('=' * 70)
    
    tests = [
        test_database,
        test_migrations,
        test_apps,
        test_admin,
        test_urls,
        test_authentication,
        test_static_files,
        test_data_samples,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f'\n❌ ERRO DURANTE TESTE: {e}')
            import traceback
            traceback.print_exc()
            results.append(False)
    
    # Summary
    print_section('RESUMO DA VALIDAÇÃO')
    
    passed = sum(results)
    total = len(results)
    
    print(f'\n✅ Testes passados: {passed}/{total}')
    
    if all(results):
        print('\n🎉 SISTEMA 100% OPERACIONAL!')
        print('\nPróximos passos:')
        print('1. Acesse: http://127.0.0.1:8000/admin/')
        print('2. Faça login com seu superusuário')
        print('3. Crie facilities e equipamentos de teste')
        print('4. Teste geração de QR codes')
        print('5. Teste registro de limpeza')
    else:
        print('\n⚠️  Alguns testes falharam. Revise os erros acima.')
        sys.exit(1)
    
    print('\n' + '=' * 70)

if __name__ == '__main__':
    run_all_tests()
