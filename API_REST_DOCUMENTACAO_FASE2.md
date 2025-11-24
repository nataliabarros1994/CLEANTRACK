# 🔌 CleanTrack API REST - Documentação Completa

## 📋 **VISÃO GERAL**

```
Status:         PLANEJADO (Fase 2 - Q1/2026)
Versão:         v1.0.0
Base URL:       https://api.cleantrack.com/v1
Autenticação:   Bearer Token (JWT)
Formato:        JSON (application/json)
Rate Limit:     1.000 requisições/hora
Charset:        UTF-8
CORS:           Habilitado (origens autorizadas)
HTTPS:          Obrigatório (TLS 1.2+)
```

---

## 🔑 **AUTENTICAÇÃO**

### **Bearer Token (JWT)**

```http
POST /auth/token/
Content-Type: application/json

{
  "email": "admin@hospital.com",
  "password": "senha_segura"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "id": 123,
    "email": "admin@hospital.com",
    "role": "admin",
    "facility_id": 456
  }
}
```

**Uso em Requisições:**
```http
GET /equipment/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

### **Refresh Token**

```http
POST /auth/refresh/
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600
}
```

---

### **Revoke Token (Logout)**

```http
POST /auth/revoke/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (204 No Content)**

---

## 📊 **ENDPOINTS PRINCIPAIS**

### **1. FACILITIES (Instalações)**

#### **GET /facilities/**
Lista todas as facilities do usuário autenticado.

**Request:**
```http
GET /facilities/
Authorization: Bearer {token}
```

**Query Parameters:**
```
?page=1              # Número da página (default: 1)
?page_size=20        # Itens por página (default: 20, max: 100)
?is_active=true      # Filtrar por status ativo
?search=Hospital     # Buscar por nome
?ordering=-created_at # Ordenar (created_at, name, -created_at)
```

**Response (200 OK):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 456,
      "name": "Hospital Memorial",
      "address": "Rua das Flores, 123",
      "city": "São Paulo",
      "state": "SP",
      "country": "Brasil",
      "is_active": true,
      "created_at": "2025-01-15T10:00:00Z",
      "updated_at": "2025-01-20T15:30:00Z",
      "equipment_count": 45,
      "managers": [
        {
          "id": 123,
          "name": "João Silva",
          "email": "joao@hospital.com"
        }
      ]
    }
  ]
}
```

---

#### **GET /facilities/{id}/**
Detalhes de uma facility específica.

**Request:**
```http
GET /facilities/456/
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "id": 456,
  "name": "Hospital Memorial",
  "address": "Rua das Flores, 123",
  "city": "São Paulo",
  "state": "SP",
  "zip_code": "01234-567",
  "country": "Brasil",
  "phone": "+55 11 1234-5678",
  "email": "contato@hospitalmemorial.com",
  "is_active": true,
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-20T15:30:00Z",
  "stripe_customer_id": "cus_ABC123",
  "subscription_status": "active",
  "equipment_count": 45,
  "cleaning_logs_count": 1234,
  "compliance_rate": 92.5,
  "managers": [
    {
      "id": 123,
      "name": "João Silva",
      "email": "joao@hospital.com",
      "role": "manager"
    }
  ]
}
```

---

#### **POST /facilities/**
Cria uma nova facility (admin only).

**Request:**
```http
POST /facilities/
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Clínica São José",
  "address": "Av. Principal, 456",
  "city": "Rio de Janeiro",
  "state": "RJ",
  "zip_code": "20000-000",
  "country": "Brasil",
  "phone": "+55 21 9876-5432",
  "email": "contato@clinicasaojose.com"
}
```

**Response (201 Created):**
```json
{
  "id": 789,
  "name": "Clínica São José",
  "address": "Av. Principal, 456",
  "city": "Rio de Janeiro",
  "state": "RJ",
  "zip_code": "20000-000",
  "country": "Brasil",
  "phone": "+55 21 9876-5432",
  "email": "contato@clinicasaojose.com",
  "is_active": true,
  "created_at": "2025-01-22T14:00:00Z",
  "updated_at": "2025-01-22T14:00:00Z",
  "stripe_customer_id": null,
  "subscription_status": "trial"
}
```

---

### **2. EQUIPMENT (Equipamentos)**

#### **GET /facilities/{id}/equipment/**
Lista equipamentos de uma facility.

**Request:**
```http
GET /facilities/456/equipment/
Authorization: Bearer {token}
```

**Query Parameters:**
```
?page=1
?page_size=20
?is_active=true
?category=diagnostic     # Categoria (diagnostic, monitoring, life_support, surgical, lab, other)
?is_overdue=false       # Filtrar atrasados
?search=Desfibrilador   # Buscar por nome/serial
?ordering=-created_at
```

**Response (200 OK):**
```json
{
  "count": 45,
  "next": "https://api.cleantrack.com/v1/facilities/456/equipment/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Desfibrilador XYZ",
      "serial_number": "DEF-001-2025",
      "category": "life_support",
      "description": "Desfibrilador para emergências",
      "location": "UTI - Sala 3",
      "cleaning_frequency_hours": 24,
      "is_active": true,
      "is_overdue": false,
      "last_cleaning": {
        "id": 567,
        "cleaned_at": "2025-01-21T08:30:00Z",
        "cleaned_by": {
          "id": 234,
          "name": "Maria Santos"
        }
      },
      "next_cleaning_due": "2025-01-22T08:30:00Z",
      "compliance_status": "compliant",
      "qr_code_url": "https://api.cleantrack.com/v1/equipment/1/qr/?format=svg",
      "public_token": "a3b7c9d1e2f4g5h6i7j8k9l0m1n2o3p4",
      "created_at": "2025-01-10T09:00:00Z",
      "updated_at": "2025-01-21T08:30:00Z"
    }
  ]
}
```

---

#### **GET /equipment/{id}/**
Detalhes de um equipamento específico.

**Request:**
```http
GET /equipment/1/
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "facility": {
    "id": 456,
    "name": "Hospital Memorial"
  },
  "name": "Desfibrilador XYZ",
  "serial_number": "DEF-001-2025",
  "category": "life_support",
  "category_display": "Suporte à Vida",
  "description": "Desfibrilador para emergências",
  "location": "UTI - Sala 3",
  "manufacturer": "Philips Healthcare",
  "model": "HeartStart XL",
  "purchase_date": "2024-05-15",
  "cleaning_frequency_hours": 24,
  "cleaning_protocol": {
    "id": 10,
    "name": "Protocolo Desfibrilador",
    "steps": [
      "Desligar equipamento",
      "Limpar superfície com álcool 70%",
      "Aguardar secar (5 min)",
      "Ligar e testar"
    ]
  },
  "is_active": true,
  "is_overdue": false,
  "last_cleaning": {
    "id": 567,
    "cleaned_at": "2025-01-21T08:30:00Z",
    "cleaned_by": {
      "id": 234,
      "name": "Maria Santos",
      "email": "maria@hospital.com"
    },
    "photo_url": "https://media.cleantrack.com/cleaning/567.jpg",
    "notes": "Limpeza completa, equipamento funcionando"
  },
  "next_cleaning_due": "2025-01-22T08:30:00Z",
  "compliance_status": "compliant",
  "total_cleanings": 34,
  "qr_code_url": "https://api.cleantrack.com/v1/equipment/1/qr/?format=svg",
  "public_token": "a3b7c9d1e2f4g5h6i7j8k9l0m1n2o3p4",
  "token_created_at": "2025-01-10T09:00:00Z",
  "created_at": "2025-01-10T09:00:00Z",
  "updated_at": "2025-01-21T08:30:00Z"
}
```

---

#### **POST /equipment/**
Cria um novo equipamento.

**Request:**
```http
POST /equipment/
Authorization: Bearer {token}
Content-Type: application/json

{
  "facility_id": 456,
  "name": "Ventilador ABC",
  "serial_number": "VEN-023-2025",
  "category": "life_support",
  "description": "Ventilador mecânico para CTI",
  "location": "CTI - Leito 5",
  "manufacturer": "GE Healthcare",
  "model": "Engström Carestation",
  "purchase_date": "2024-08-20",
  "cleaning_frequency_hours": 8
}
```

**Response (201 Created):**
```json
{
  "id": 46,
  "facility": {
    "id": 456,
    "name": "Hospital Memorial"
  },
  "name": "Ventilador ABC",
  "serial_number": "VEN-023-2025",
  "category": "life_support",
  "description": "Ventilador mecânico para CTI",
  "location": "CTI - Leito 5",
  "manufacturer": "GE Healthcare",
  "model": "Engström Carestation",
  "purchase_date": "2024-08-20",
  "cleaning_frequency_hours": 8,
  "is_active": true,
  "is_overdue": false,
  "qr_code_url": "https://api.cleantrack.com/v1/equipment/46/qr/?format=svg",
  "public_token": "z9y8x7w6v5u4t3s2r1q0p9o8n7m6l5k4",
  "created_at": "2025-01-22T15:00:00Z",
  "updated_at": "2025-01-22T15:00:00Z"
}
```

---

#### **PATCH /equipment/{id}/**
Atualiza um equipamento (parcial).

**Request:**
```http
PATCH /equipment/1/
Authorization: Bearer {token}
Content-Type: application/json

{
  "location": "UTI - Sala 5",
  "cleaning_frequency_hours": 12
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Desfibrilador XYZ",
  "location": "UTI - Sala 5",
  "cleaning_frequency_hours": 12,
  "updated_at": "2025-01-22T16:00:00Z"
}
```

---

#### **DELETE /equipment/{id}/**
Soft-delete de um equipamento (is_active=False).

**Request:**
```http
DELETE /equipment/1/
Authorization: Bearer {token}
```

**Response (204 No Content)**

---

### **3. QR CODES**

#### **GET /equipment/{id}/qr/**
Gera QR code para um equipamento.

**Request:**
```http
GET /equipment/1/qr/?format=svg&size=10
Authorization: Bearer {token}
```

**Query Parameters:**
```
format=svg          # Formato (svg, png, jpeg) - default: svg
size=10             # Tamanho (1-50) - default: 10
error_correction=H  # Nível (L, M, Q, H) - default: H
token_type=permanent # Tipo (permanent, temporary) - default: permanent
```

**Response (200 OK) - SVG:**
```xml
Content-Type: image/svg+xml

<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400">
  <!-- QR code SVG content -->
</svg>
```

**Response (200 OK) - PNG:**
```
Content-Type: image/png
Content-Disposition: inline; filename="equipment_1_qr.png"

[Binary PNG data]
```

---

#### **POST /equipment/{id}/qr/regenerate/**
Regenera token permanente (invalida QR code anterior).

**Request:**
```http
POST /equipment/1/qr/regenerate/
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "public_token": "new_token_abc123xyz789",
  "token_created_at": "2025-01-22T17:00:00Z",
  "qr_code_url": "https://api.cleantrack.com/v1/equipment/1/qr/?format=svg"
}
```

---

#### **GET /equipment/{id}/qr/temporary/**
Gera token temporário (5 min) para uso único.

**Request:**
```http
GET /equipment/1/qr/temporary/
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "temporary_token": "1:1737570000:a1b2c3d4e5f6g7h8i9j0",
  "expires_at": "2025-01-22T17:05:00Z",
  "expires_in_seconds": 300,
  "url": "https://app.cleantrack.com/temp-log/1:1737570000:a1b2c3d4e5f6g7h8i9j0/",
  "qr_code_url": "https://api.cleantrack.com/v1/equipment/1/qr/?format=svg&token_type=temporary"
}
```

---

### **4. CLEANING LOGS**

#### **GET /cleaning-logs/**
Lista registros de limpeza.

**Request:**
```http
GET /cleaning-logs/?facility_id=456&page=1
Authorization: Bearer {token}
```

**Query Parameters:**
```
facility_id=456          # Facility (obrigatório para managers)
equipment_id=1           # Equipamento específico
cleaned_by=234           # Técnico
start_date=2025-01-01    # Data início (ISO 8601)
end_date=2025-01-31      # Data fim
is_compliant=true        # Filtrar por conformidade
page=1
page_size=20
ordering=-cleaned_at     # Ordenar por data
```

**Response (200 OK):**
```json
{
  "count": 1234,
  "next": "https://api.cleantrack.com/v1/cleaning-logs/?page=2",
  "previous": null,
  "results": [
    {
      "id": 567,
      "equipment": {
        "id": 1,
        "name": "Desfibrilador XYZ",
        "serial_number": "DEF-001-2025"
      },
      "facility": {
        "id": 456,
        "name": "Hospital Memorial"
      },
      "cleaned_by": {
        "id": 234,
        "name": "Maria Santos",
        "email": "maria@hospital.com"
      },
      "cleaned_at": "2025-01-21T08:30:00Z",
      "photo": "https://media.cleantrack.com/cleaning/567.jpg",
      "notes": "Limpeza completa, equipamento funcionando",
      "is_compliant": true,
      "duration_minutes": 8,
      "created_at": "2025-01-21T08:30:00Z"
    }
  ]
}
```

---

#### **GET /cleaning-logs/{id}/**
Detalhes de um registro de limpeza.

**Request:**
```http
GET /cleaning-logs/567/
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "id": 567,
  "equipment": {
    "id": 1,
    "name": "Desfibrilador XYZ",
    "serial_number": "DEF-001-2025",
    "category": "life_support",
    "location": "UTI - Sala 3"
  },
  "facility": {
    "id": 456,
    "name": "Hospital Memorial"
  },
  "cleaned_by": {
    "id": 234,
    "name": "Maria Santos",
    "email": "maria@hospital.com",
    "role": "technician"
  },
  "cleaned_at": "2025-01-21T08:30:00Z",
  "photo": "https://media.cleantrack.com/cleaning/567.jpg",
  "photo_thumbnail": "https://media.cleantrack.com/cleaning/567_thumb.jpg",
  "notes": "Limpeza completa, equipamento funcionando",
  "is_compliant": true,
  "duration_minutes": 8,
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0...)",
  "created_at": "2025-01-21T08:30:00Z",
  "updated_at": "2025-01-21T08:30:00Z"
}
```

---

#### **POST /cleaning-logs/**
Cria um novo registro de limpeza via API.

**Suporta 2 formatos de envio de foto:**

##### **Opção 1: Multipart/Form-Data (Recomendado para uploads de arquivos)**

**Request:**
```http
POST /cleaning-logs/
Authorization: Bearer {token}
Content-Type: multipart/form-data

{
  "equipment_id": 1,
  "cleaned_at": "2025-01-22T09:00:00Z",
  "photo": [binary image data],
  "notes": "Limpeza de rotina"
}
```

**Response (201 Created):**
```json
{
  "id": 568,
  "equipment": {
    "id": 1,
    "name": "Desfibrilador XYZ",
    "serial_number": "DEF-001-2025"
  },
  "facility": {
    "id": 456,
    "name": "Hospital Memorial"
  },
  "cleaned_by": {
    "id": 123,
    "name": "João Silva",
    "email": "joao@hospital.com"
  },
  "cleaned_at": "2025-01-22T09:00:00Z",
  "photo": "https://media.cleantrack.com/cleaning/568.jpg",
  "photo_thumbnail": "https://media.cleantrack.com/cleaning/568_thumb.jpg",
  "notes": "Limpeza de rotina",
  "is_compliant": true,
  "duration_minutes": null,
  "created_at": "2025-01-22T09:00:00Z"
}
```

---

##### **Opção 2: JSON com Base64 (Para mobile apps e integrações)**

**Request:**
```http
POST /cleaning-logs/
Authorization: Bearer {token}
Content-Type: application/json

{
  "equipment_id": 1,
  "cleaned_at": "2025-01-22T09:00:00Z",
  "photo_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBD...",
  "notes": "Limpeza de rotina",
  "duration_minutes": 8
}
```

**Formato da foto em Base64:**
```
data:image/{format};base64,{base64_encoded_data}

Formatos suportados:
- image/jpeg
- image/png
- image/webp

Tamanho máximo: 5 MB
Resolução recomendada: 1920x1080 (será redimensionada se maior)
```

**Response (201 Created):**
```json
{
  "id": 569,
  "equipment": {
    "id": 1,
    "name": "Desfibrilador XYZ",
    "serial_number": "DEF-001-2025"
  },
  "facility": {
    "id": 456,
    "name": "Hospital Memorial"
  },
  "cleaned_by": {
    "id": 123,
    "name": "João Silva",
    "email": "joao@hospital.com"
  },
  "cleaned_at": "2025-01-22T09:00:00Z",
  "photo": "https://media.cleantrack.com/cleaning/569.jpg",
  "photo_thumbnail": "https://media.cleantrack.com/cleaning/569_thumb.jpg",
  "notes": "Limpeza de rotina",
  "is_compliant": true,
  "duration_minutes": 8,
  "created_at": "2025-01-22T09:00:00Z"
}
```

---

##### **Validações e Regras de Negócio**

```json
{
  "equipment_id": "Obrigatório - Equipamento deve existir e estar ativo",
  "cleaned_at": "Opcional - Default: now(). Não pode ser futuro",
  "photo ou photo_base64": "Obrigatório - Pelo menos um dos dois",
  "notes": "Opcional - Máximo 500 caracteres",
  "duration_minutes": "Opcional - Inteiro positivo (1-999)"
}
```

**Erros comuns:**

```json
// 400 Bad Request - Foto muito grande
{
  "error": "validation_error",
  "message": "Tamanho da foto excede o limite de 5 MB",
  "details": {
    "photo": ["Arquivo muito grande (7.2 MB). Máximo: 5 MB"]
  }
}

// 400 Bad Request - Formato inválido
{
  "error": "validation_error",
  "message": "Formato de imagem não suportado",
  "details": {
    "photo_base64": ["Formato inválido. Use: image/jpeg, image/png ou image/webp"]
  }
}

// 400 Bad Request - Base64 inválido
{
  "error": "validation_error",
  "message": "Dados Base64 inválidos",
  "details": {
    "photo_base64": ["String Base64 malformada. Formato esperado: data:image/{format};base64,{data}"]
  }
}

// 404 Not Found - Equipamento não encontrado
{
  "error": "resource_not_found",
  "message": "Equipamento com id=999 não encontrado"
}

// 403 Forbidden - Sem permissão para este equipamento
{
  "error": "permission_denied",
  "message": "Você não tem permissão para registrar limpeza neste equipamento"
}
```

---

#### **GET /equipment/{id}/cleaning-logs/**
Lista histórico de limpezas de um equipamento específico.

**Request:**
```http
GET /equipment/1/cleaning-logs/?page=1&page_size=20
Authorization: Bearer {token}
```

**Query Parameters:**
```
page=1                      # Número da página (default: 1)
page_size=20                # Itens por página (default: 20, max: 100)
start_date=2025-01-01       # Data início (ISO 8601)
end_date=2025-01-31         # Data fim
cleaned_by=234              # Filtrar por técnico
is_compliant=true           # Filtrar por conformidade
ordering=-cleaned_at        # Ordenar (cleaned_at, -cleaned_at, duration_minutes)
include_photos=false        # Incluir URLs das fotos (default: true)
```

**Response (200 OK):**
```json
{
  "count": 34,
  "next": "https://api.cleantrack.com/v1/equipment/1/cleaning-logs/?page=2",
  "previous": null,
  "equipment": {
    "id": 1,
    "name": "Desfibrilador XYZ",
    "serial_number": "DEF-001-2025",
    "category": "life_support",
    "location": "UTI - Sala 3",
    "cleaning_frequency_hours": 24
  },
  "statistics": {
    "total_cleanings": 34,
    "compliant_cleanings": 33,
    "non_compliant_cleanings": 1,
    "compliance_rate": 97.1,
    "avg_duration_minutes": 12,
    "last_cleaning": "2025-01-21T08:30:00Z",
    "next_cleaning_due": "2025-01-22T08:30:00Z"
  },
  "results": [
    {
      "id": 567,
      "cleaned_at": "2025-01-21T08:30:00Z",
      "cleaned_by": {
        "id": 234,
        "name": "Maria Santos",
        "email": "maria@hospital.com"
      },
      "photo": "https://media.cleantrack.com/cleaning/567.jpg",
      "photo_thumbnail": "https://media.cleantrack.com/cleaning/567_thumb.jpg",
      "notes": "Limpeza completa, equipamento funcionando",
      "is_compliant": true,
      "duration_minutes": 8,
      "created_at": "2025-01-21T08:30:00Z"
    },
    {
      "id": 545,
      "cleaned_at": "2025-01-20T09:15:00Z",
      "cleaned_by": {
        "id": 234,
        "name": "Maria Santos",
        "email": "maria@hospital.com"
      },
      "photo": "https://media.cleantrack.com/cleaning/545.jpg",
      "photo_thumbnail": "https://media.cleantrack.com/cleaning/545_thumb.jpg",
      "notes": "Rotina diária",
      "is_compliant": true,
      "duration_minutes": 10,
      "created_at": "2025-01-20T09:15:00Z"
    }
  ]
}
```

---

#### **Exemplo: Criar limpeza com foto Base64 (Python)**

```python
import requests
import base64
from datetime import datetime

# Autenticar
auth_response = requests.post(
    "https://api.cleantrack.com/v1/auth/token/",
    json={
        "email": "tecnico@hospital.com",
        "password": "senha123"
    }
)
token = auth_response.json()["access_token"]

# Ler foto e converter para Base64
with open("limpeza_foto.jpg", "rb") as f:
    photo_bytes = f.read()
    photo_base64 = base64.b64encode(photo_bytes).decode()
    photo_data_uri = f"data:image/jpeg;base64,{photo_base64}"

# Criar registro de limpeza
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

cleaning_data = {
    "equipment_id": 1,
    "cleaned_at": datetime.now().isoformat(),
    "photo_base64": photo_data_uri,
    "notes": "Limpeza completa - equipamento testado e funcionando",
    "duration_minutes": 12
}

response = requests.post(
    "https://api.cleantrack.com/v1/cleaning-logs/",
    headers=headers,
    json=cleaning_data
)

if response.status_code == 201:
    cleaning = response.json()
    print(f"✅ Limpeza registrada com sucesso!")
    print(f"   ID: {cleaning['id']}")
    print(f"   Foto: {cleaning['photo']}")
else:
    print(f"❌ Erro: {response.json()}")
```

---

#### **Exemplo: Criar limpeza com foto Base64 (JavaScript/React Native)**

```javascript
import * as ImagePicker from 'expo-image-picker';
import * as FileSystem from 'expo-file-system';

// Função para converter imagem em Base64
async function uploadCleaningLog(equipmentId) {
  // Capturar foto
  const result = await ImagePicker.launchCameraAsync({
    mediaTypes: ImagePicker.MediaTypeOptions.Images,
    quality: 0.8, // Compressão para reduzir tamanho
    base64: true,
  });

  if (result.cancelled) return;

  // Preparar dados
  const photoBase64 = `data:image/jpeg;base64,${result.base64}`;

  const cleaningData = {
    equipment_id: equipmentId,
    cleaned_at: new Date().toISOString(),
    photo_base64: photoBase64,
    notes: 'Limpeza registrada via mobile app',
    duration_minutes: 10
  };

  // Enviar para API
  try {
    const response = await fetch('https://api.cleantrack.com/v1/cleaning-logs/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(cleaningData)
    });

    if (response.ok) {
      const cleaning = await response.json();
      console.log('✅ Limpeza registrada:', cleaning.id);
      Alert.alert('Sucesso', 'Limpeza registrada com sucesso!');
    } else {
      const error = await response.json();
      console.error('❌ Erro:', error);
      Alert.alert('Erro', error.message);
    }
  } catch (err) {
    console.error('❌ Erro de rede:', err);
    Alert.alert('Erro', 'Não foi possível conectar ao servidor');
  }
}
```

---

#### **Exemplo: Consultar histórico de limpezas**

```python
import requests
from datetime import datetime, timedelta

# Autenticar
token = "your_access_token"
headers = {"Authorization": f"Bearer {token}"}

# Buscar limpezas dos últimos 30 dias
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

response = requests.get(
    "https://api.cleantrack.com/v1/equipment/1/cleaning-logs/",
    headers=headers,
    params={
        "start_date": start_date.date().isoformat(),
        "end_date": end_date.date().isoformat(),
        "page_size": 100,
        "ordering": "-cleaned_at"
    }
)

if response.status_code == 200:
    data = response.json()
    stats = data["statistics"]

    print(f"📊 Estatísticas do equipamento:")
    print(f"   Total de limpezas: {stats['total_cleanings']}")
    print(f"   Taxa de conformidade: {stats['compliance_rate']}%")
    print(f"   Duração média: {stats['avg_duration_minutes']} minutos")
    print(f"   Última limpeza: {stats['last_cleaning']}")
    print(f"\n📋 Histórico recente:")

    for log in data["results"][:5]:  # Mostrar últimas 5
        print(f"   • {log['cleaned_at']} - {log['cleaned_by']['name']}")
        print(f"     Nota: {log['notes']}")
else:
    print(f"❌ Erro: {response.status_code}")
```

---

### **5. REPORTS (Relatórios)**

#### **GET /facilities/{id}/compliance-stats/**
Retorna métricas de conformidade em formato JSON (para dashboards e integrações).

**Request:**
```http
GET /facilities/456/compliance-stats/?start_date=2025-01-01&end_date=2025-01-31
Authorization: Bearer {token}
```

**Query Parameters:**
```
start_date=2025-01-01    # Data início (ISO 8601) - Obrigatório
end_date=2025-01-31      # Data fim (ISO 8601) - Obrigatório
equipment_id=1           # Equipamento específico (opcional)
category=life_support    # Filtrar por categoria (opcional)
include_details=true     # Incluir breakdown por equipamento (default: false)
include_technicians=true # Incluir estatísticas por técnico (default: false)
```

**Response (200 OK):**
```json
{
  "facility": {
    "id": 456,
    "name": "Hospital Memorial",
    "city": "São Paulo",
    "state": "SP"
  },
  "period": {
    "start_date": "2025-01-01",
    "end_date": "2025-01-31",
    "total_days": 31
  },
  "summary": {
    "total_equipment": 45,
    "active_equipment": 43,
    "inactive_equipment": 2,
    "total_cleanings": 1234,
    "compliant_cleanings": 1187,
    "non_compliant_cleanings": 47,
    "compliance_rate": 96.2,
    "overdue_equipment": 3,
    "overdue_rate": 6.7,
    "active_technicians": 15,
    "avg_cleanings_per_day": 39.8,
    "avg_cleanings_per_equipment": 27.4,
    "avg_duration_minutes": 11.5
  },
  "compliance_by_category": [
    {
      "category": "life_support",
      "category_display": "Suporte à Vida",
      "total_equipment": 12,
      "total_cleanings": 456,
      "compliance_rate": 98.5,
      "overdue_count": 0
    },
    {
      "category": "diagnostic",
      "category_display": "Diagnóstico",
      "total_equipment": 18,
      "total_cleanings": 512,
      "compliance_rate": 95.1,
      "overdue_count": 2
    },
    {
      "category": "monitoring",
      "category_display": "Monitoramento",
      "total_equipment": 15,
      "total_cleanings": 266,
      "compliance_rate": 94.8,
      "overdue_count": 1
    }
  ],
  "trends": {
    "compliance_rate_change": 2.3,
    "cleanings_count_change": 15.7,
    "comparison_period": "previous_month"
  },
  "equipment_breakdown": [
    {
      "id": 1,
      "name": "Desfibrilador XYZ",
      "serial_number": "DEF-001-2025",
      "category": "life_support",
      "location": "UTI - Sala 3",
      "total_cleanings": 31,
      "compliant_cleanings": 30,
      "non_compliant_cleanings": 1,
      "compliance_rate": 96.8,
      "is_overdue": false,
      "last_cleaning": "2025-01-31T14:30:00Z",
      "next_cleaning_due": "2025-02-01T14:30:00Z",
      "avg_duration_minutes": 12
    },
    {
      "id": 2,
      "name": "Ventilador ABC",
      "serial_number": "VEN-023-2025",
      "category": "life_support",
      "location": "CTI - Leito 5",
      "total_cleanings": 89,
      "compliant_cleanings": 89,
      "non_compliant_cleanings": 0,
      "compliance_rate": 100.0,
      "is_overdue": false,
      "last_cleaning": "2025-01-31T18:00:00Z",
      "next_cleaning_due": "2025-02-01T02:00:00Z",
      "avg_duration_minutes": 8
    }
  ],
  "technician_stats": [
    {
      "id": 234,
      "name": "Maria Santos",
      "email": "maria@hospital.com",
      "total_cleanings": 456,
      "compliant_cleanings": 445,
      "compliance_rate": 97.6,
      "avg_duration_minutes": 12,
      "equipment_coverage": 28,
      "most_cleaned_category": "life_support"
    },
    {
      "id": 235,
      "name": "João Oliveira",
      "email": "joao@hospital.com",
      "total_cleanings": 389,
      "compliant_cleanings": 378,
      "compliance_rate": 97.2,
      "avg_duration_minutes": 11,
      "equipment_coverage": 25,
      "most_cleaned_category": "diagnostic"
    }
  ],
  "daily_stats": [
    {
      "date": "2025-01-01",
      "total_cleanings": 42,
      "compliant": 40,
      "compliance_rate": 95.2
    },
    {
      "date": "2025-01-02",
      "total_cleanings": 38,
      "compliant": 37,
      "compliance_rate": 97.4
    }
  ],
  "generated_at": "2025-01-22T18:00:00Z",
  "generated_by": {
    "id": 123,
    "name": "Admin User",
    "email": "admin@hospital.com"
  }
}
```

---

#### **GET /facilities/{id}/compliance-report/**
Gera relatório de conformidade em PDF (para auditorias e impressão).

**Request:**
```http
GET /facilities/456/compliance-report/?start_date=2025-01-01&end_date=2025-01-31&format=pdf
Authorization: Bearer {token}
```

**Query Parameters:**
```
start_date=2025-01-01    # Data início (ISO 8601) - Obrigatório
end_date=2025-01-31      # Data fim (ISO 8601) - Obrigatório
format=pdf               # Formato (pdf, excel, csv) - Default: pdf
include_photos=false     # Incluir fotos das limpezas (default: false)
include_signatures=true  # Incluir assinaturas digitais (default: true)
language=pt-BR           # Idioma (pt-BR, en-US, es-ES) - Default: pt-BR
template=standard        # Template (standard, detailed, executive) - Default: standard
```

**Response (200 OK) - PDF:**
```http
Content-Type: application/pdf
Content-Disposition: attachment; filename="compliance_report_456_2025-01.pdf"
Content-Length: 524288

[Binary PDF data]
```

**Response Headers:**
```http
X-Report-ID: rpt_abc123xyz789
X-Generated-At: 2025-01-22T18:00:00Z
X-Report-Period: 2025-01-01 to 2025-01-31
X-Facility-ID: 456
X-Total-Pages: 8
X-File-Size: 524288
```

---

#### **Conteúdo do PDF gerado:**

```
┌─────────────────────────────────────────────────────────────┐
│ 🏥 RELATÓRIO DE CONFORMIDADE DE LIMPEZA                     │
│ CleanTrack - Medical Equipment Compliance                   │
└─────────────────────────────────────────────────────────────┘

INSTALAÇÃO: Hospital Memorial
ENDEREÇO:   Rua das Flores, 123 - São Paulo, SP
PERÍODO:    01/01/2025 a 31/01/2025 (31 dias)
GERADO EM:  22/01/2025 às 18:00

═══════════════════════════════════════════════════════════════

RESUMO EXECUTIVO

├─ Total de Equipamentos:        45 ativos
├─ Total de Limpezas:            1.234 registros
├─ Limpezas Conformes:           1.187 (96.2%)
├─ Limpezas Não Conformes:       47 (3.8%)
├─ Equipamentos Atrasados:       3 (6.7%)
├─ Técnicos Ativos:              15
└─ Duração Média de Limpeza:     11.5 minutos

TAXA DE CONFORMIDADE: 96.2% ✅ (Meta: 95%)

═══════════════════════════════════════════════════════════════

CONFORMIDADE POR CATEGORIA

┌──────────────────────┬─────────┬──────────┬─────────────┐
│ Categoria            │ Equip.  │ Limpezas │ Conformidade│
├──────────────────────┼─────────┼──────────┼─────────────┤
│ Suporte à Vida       │   12    │   456    │   98.5%  ✅ │
│ Diagnóstico          │   18    │   512    │   95.1%  ✅ │
│ Monitoramento        │   15    │   266    │   94.8%  ⚠️ │
│ Cirúrgico            │    0    │     0    │    N/A      │
└──────────────────────┴─────────┴──────────┴─────────────┘

═══════════════════════════════════════════════════════════════

EQUIPAMENTOS DETALHADOS (Top 10 por limpezas)

1. Ventilador ABC (VEN-023-2025)
   └─ Categoria: Suporte à Vida | Local: CTI - Leito 5
   └─ Limpezas: 89 | Conformidade: 100% ✅
   └─ Última: 31/01/2025 18:00 | Próxima: 01/02/2025 02:00

2. Desfibrilador XYZ (DEF-001-2025)
   └─ Categoria: Suporte à Vida | Local: UTI - Sala 3
   └─ Limpezas: 31 | Conformidade: 96.8% ✅
   └─ Última: 31/01/2025 14:30 | Próxima: 01/02/2025 14:30

[... continua para todos equipamentos ...]

═══════════════════════════════════════════════════════════════

EQUIPAMENTOS ATRASADOS (Ação Imediata Requerida!)

⚠️ 1. Monitor Cardíaco DEF (MON-045-2024)
   └─ Última limpeza: 20/01/2025 10:00
   └─ Deveria ter sido limpo: 21/01/2025 10:00
   └─ Atraso: 11 dias | Status: CRÍTICO 🔴

⚠️ 2. Bomba de Infusão GHI (BOM-012-2024)
   └─ Última limpeza: 28/01/2025 14:00
   └─ Deveria ter sido limpo: 28/01/2025 18:00
   └─ Atraso: 4 horas | Status: ATRASADO 🟡

═══════════════════════════════════════════════════════════════

DESEMPENHO POR TÉCNICO

┌──────────────────────┬──────────┬─────────────┬────────────┐
│ Técnico              │ Limpezas │ Conformidade│ Duração Avg│
├──────────────────────┼──────────┼─────────────┼────────────┤
│ Maria Santos         │   456    │   97.6%  ✅ │  12 min    │
│ João Oliveira        │   389    │   97.2%  ✅ │  11 min    │
│ Ana Costa            │   312    │   96.5%  ✅ │  10 min    │
└──────────────────────┴──────────┴─────────────┴────────────┘

═══════════════════════════════════════════════════════════════

GRÁFICOS E TENDÊNCIAS

[Gráfico de barras: Conformidade por categoria]
[Gráfico de linha: Limpezas por dia ao longo do mês]
[Gráfico de pizza: Distribuição de limpezas por técnico]

═══════════════════════════════════════════════════════════════

ASSINATURAS E CERTIFICAÇÃO

Este relatório foi gerado automaticamente pelo sistema CleanTrack
em conformidade com as normas ANVISA RDC 15/2012.

Responsável Técnico: _________________________________
                      João Silva - CRM 12345/SP

Data: ___/___/______

Assinatura Digital:
SHA256: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
Timestamp: 2025-01-22T18:00:00Z
Verificar em: https://app.cleantrack.com/verify/rpt_abc123xyz789

═══════════════════════════════════════════════════════════════

Página 1 de 8                    CleanTrack © 2025
```

---

#### **GET /reports/compliance/**
Relatório de conformidade multi-facility (para administradores).

**Request:**
```http
GET /reports/compliance/?facility_id=456&start_date=2025-01-01&end_date=2025-01-31
Authorization: Bearer {token}
```

**Query Parameters:**
```
facility_id=456          # Facility (obrigatório para managers, opcional para admins)
start_date=2025-01-01    # Data início
end_date=2025-01-31      # Data fim
equipment_id=1           # Equipamento específico (opcional)
```

**Response (200 OK):**
```json
{
  "facility": {
    "id": 456,
    "name": "Hospital Memorial"
  },
  "period": {
    "start_date": "2025-01-01",
    "end_date": "2025-01-31"
  },
  "summary": {
    "total_equipment": 45,
    "total_cleanings": 1234,
    "compliant_cleanings": 1187,
    "non_compliant_cleanings": 47,
    "compliance_rate": 96.2,
    "overdue_equipment": 3,
    "active_technicians": 15
  },
  "equipment_breakdown": [
    {
      "id": 1,
      "name": "Desfibrilador XYZ",
      "category": "life_support",
      "total_cleanings": 31,
      "compliant": 30,
      "non_compliant": 1,
      "compliance_rate": 96.8,
      "is_overdue": false
    }
  ],
  "technician_stats": [
    {
      "id": 234,
      "name": "Maria Santos",
      "total_cleanings": 456,
      "avg_duration_minutes": 12
    }
  ],
  "generated_at": "2025-01-22T18:00:00Z"
}
```

#### **Exemplo: Obter estatísticas JSON para dashboard**

```python
import requests
from datetime import datetime, timedelta

# Autenticar
token = "your_access_token"
headers = {"Authorization": f"Bearer {token}"}

# Definir período (último mês)
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# Buscar estatísticas completas
response = requests.get(
    "https://api.cleantrack.com/v1/facilities/456/compliance-stats/",
    headers=headers,
    params={
        "start_date": start_date.date().isoformat(),
        "end_date": end_date.date().isoformat(),
        "include_details": True,
        "include_technicians": True
    }
)

if response.status_code == 200:
    stats = response.json()

    # Exibir resumo
    summary = stats["summary"]
    print(f"📊 RESUMO DE CONFORMIDADE")
    print(f"{'='*50}")
    print(f"Total de equipamentos: {summary['total_equipment']}")
    print(f"Total de limpezas: {summary['total_cleanings']}")
    print(f"Taxa de conformidade: {summary['compliance_rate']}%")
    print(f"Equipamentos atrasados: {summary['overdue_equipment']}")
    print(f"Média de limpezas/dia: {summary['avg_cleanings_per_day']:.1f}")

    # Exibir conformidade por categoria
    print(f"\n📋 CONFORMIDADE POR CATEGORIA")
    print(f"{'='*50}")
    for cat in stats["compliance_by_category"]:
        status = "✅" if cat["compliance_rate"] >= 95 else "⚠️"
        print(f"{status} {cat['category_display']}: {cat['compliance_rate']}%")

    # Top 3 técnicos
    print(f"\n🏆 TOP 3 TÉCNICOS")
    print(f"{'='*50}")
    for i, tech in enumerate(stats["technician_stats"][:3], 1):
        print(f"{i}. {tech['name']}")
        print(f"   Limpezas: {tech['total_cleanings']} | Conformidade: {tech['compliance_rate']}%")
else:
    print(f"❌ Erro: {response.status_code}")
    print(response.json())
```

---

#### **Exemplo: Baixar relatório PDF**

```python
import requests
from datetime import datetime, timedelta

# Autenticar
token = "your_access_token"
headers = {"Authorization": f"Bearer {token}"}

# Definir período
start_date = "2025-01-01"
end_date = "2025-01-31"

# Requisitar PDF
response = requests.get(
    "https://api.cleantrack.com/v1/facilities/456/compliance-report/",
    headers=headers,
    params={
        "start_date": start_date,
        "end_date": end_date,
        "format": "pdf",
        "include_signatures": True,
        "template": "detailed",
        "language": "pt-BR"
    },
    stream=True  # Importante para arquivos grandes
)

if response.status_code == 200:
    # Extrair nome do arquivo do header
    content_disposition = response.headers.get('Content-Disposition')
    filename = content_disposition.split('filename=')[1].strip('"')

    # Salvar PDF
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Exibir informações do relatório
    print(f"✅ Relatório PDF baixado com sucesso!")
    print(f"   Arquivo: {filename}")
    print(f"   Tamanho: {response.headers.get('Content-Length')} bytes")
    print(f"   Report ID: {response.headers.get('X-Report-ID')}")
    print(f"   Total de páginas: {response.headers.get('X-Total-Pages')}")
    print(f"   Período: {response.headers.get('X-Report-Period')}")
else:
    print(f"❌ Erro ao gerar relatório: {response.status_code}")
    print(response.json())
```

---

#### **Exemplo: Gerar relatório Excel via JavaScript**

```javascript
async function downloadComplianceExcel(facilityId, startDate, endDate) {
  const token = localStorage.getItem('access_token');

  const params = new URLSearchParams({
    start_date: startDate,
    end_date: endDate,
    format: 'excel'
  });

  try {
    const response = await fetch(
      `https://api.cleantrack.com/v1/facilities/${facilityId}/compliance-report/?${params}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );

    if (response.ok) {
      // Converter para blob
      const blob = await response.blob();

      // Extrair nome do arquivo
      const contentDisposition = response.headers.get('Content-Disposition');
      const filename = contentDisposition
        .split('filename=')[1]
        .replace(/"/g, '');

      // Criar link de download
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);

      console.log('✅ Relatório Excel baixado:', filename);

      // Exibir metadados
      console.log('Report ID:', response.headers.get('X-Report-ID'));
      console.log('Período:', response.headers.get('X-Report-Period'));
    } else {
      const error = await response.json();
      console.error('❌ Erro:', error);
      alert(`Erro ao gerar relatório: ${error.message}`);
    }
  } catch (err) {
    console.error('❌ Erro de rede:', err);
    alert('Não foi possível conectar ao servidor');
  }
}

// Uso
downloadComplianceExcel(456, '2025-01-01', '2025-01-31');
```

---

#### **Exemplo: Dashboard em tempo real com React**

```javascript
import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

function ComplianceDashboard({ facilityId }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats();
  }, [facilityId]);

  async function fetchStats() {
    try {
      const token = localStorage.getItem('access_token');
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - 30);

      const response = await fetch(
        `https://api.cleantrack.com/v1/facilities/${facilityId}/compliance-stats/?` +
        `start_date=${startDate.toISOString().split('T')[0]}&` +
        `end_date=${endDate.toISOString().split('T')[0]}&` +
        `include_details=true&include_technicians=true`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      if (response.ok) {
        const data = await response.json();
        setStats(data);
      } else {
        throw new Error('Erro ao carregar estatísticas');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  if (loading) return <div>Carregando...</div>;
  if (error) return <div>Erro: {error}</div>;
  if (!stats) return null;

  const { summary, compliance_by_category, daily_stats, technician_stats } = stats;

  return (
    <div className="dashboard">
      {/* KPIs principais */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <h3>Taxa de Conformidade</h3>
          <div className="kpi-value">{summary.compliance_rate}%</div>
          <div className={summary.compliance_rate >= 95 ? 'positive' : 'negative'}>
            {summary.compliance_rate >= 95 ? '✅ Meta atingida' : '⚠️ Abaixo da meta'}
          </div>
        </div>

        <div className="kpi-card">
          <h3>Total de Limpezas</h3>
          <div className="kpi-value">{summary.total_cleanings}</div>
          <div>Média: {summary.avg_cleanings_per_day.toFixed(1)}/dia</div>
        </div>

        <div className="kpi-card">
          <h3>Equipamentos Atrasados</h3>
          <div className="kpi-value">{summary.overdue_equipment}</div>
          <div className={summary.overdue_equipment === 0 ? 'positive' : 'warning'}>
            {summary.overdue_equipment === 0 ? '✅ Nenhum' : `⚠️ ${summary.overdue_rate}%`}
          </div>
        </div>

        <div className="kpi-card">
          <h3>Técnicos Ativos</h3>
          <div className="kpi-value">{summary.active_technicians}</div>
          <div>Duração média: {summary.avg_duration_minutes} min</div>
        </div>
      </div>

      {/* Gráfico de conformidade por categoria */}
      <div className="chart-container">
        <h3>Conformidade por Categoria</h3>
        <BarChart width={600} height={300} data={compliance_by_category}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="category_display" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="compliance_rate" fill="#27ae60" name="Conformidade %" />
        </BarChart>
      </div>

      {/* Gráfico de limpezas por dia */}
      <div className="chart-container">
        <h3>Limpezas por Dia</h3>
        <LineChart width={800} height={300} data={daily_stats}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="total_cleanings" stroke="#3498db" name="Limpezas" />
          <Line type="monotone" dataKey="compliance_rate" stroke="#27ae60" name="Conformidade %" />
        </LineChart>
      </div>

      {/* Ranking de técnicos */}
      <div className="technician-ranking">
        <h3>Top Técnicos</h3>
        <table>
          <thead>
            <tr>
              <th>Posição</th>
              <th>Nome</th>
              <th>Limpezas</th>
              <th>Conformidade</th>
              <th>Duração Média</th>
            </tr>
          </thead>
          <tbody>
            {technician_stats.map((tech, idx) => (
              <tr key={tech.id}>
                <td>{idx + 1}</td>
                <td>{tech.name}</td>
                <td>{tech.total_cleanings}</td>
                <td>
                  <span className={tech.compliance_rate >= 95 ? 'positive' : 'warning'}>
                    {tech.compliance_rate}%
                  </span>
                </td>
                <td>{tech.avg_duration_minutes} min</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ComplianceDashboard;
```

---

#### **POST /reports/compliance/pdf/**
Gera PDF de relatório de conformidade (método alternativo - via POST para configurações avançadas).

**Request:**
```http
POST /reports/compliance/pdf/
Authorization: Bearer {token}
Content-Type: application/json

{
  "facility_id": 456,
  "start_date": "2025-01-01",
  "end_date": "2025-01-31",
  "include_photos": false,
  "language": "pt-BR"
}
```

**Response (200 OK):**
```json
{
  "pdf_url": "https://reports.cleantrack.com/compliance_456_202501.pdf",
  "expires_at": "2025-01-23T18:00:00Z",
  "file_size_bytes": 524288,
  "generated_at": "2025-01-22T18:00:00Z"
}
```

---

#### **POST /reports/compliance/excel/**
Gera Excel de relatório de conformidade.

**Request:**
```http
POST /reports/compliance/excel/
Authorization: Bearer {token}
Content-Type: application/json

{
  "facility_id": 456,
  "start_date": "2025-01-01",
  "end_date": "2025-01-31"
}
```

**Response (200 OK):**
```json
{
  "excel_url": "https://reports.cleantrack.com/compliance_456_202501.xlsx",
  "expires_at": "2025-01-23T18:00:00Z",
  "file_size_bytes": 102400,
  "generated_at": "2025-01-22T18:00:00Z"
}
```

---

### **6. WEBHOOKS**

#### **POST /webhooks/**
Cria um webhook para receber eventos.

**Request:**
```http
POST /webhooks/
Authorization: Bearer {token}
Content-Type: application/json

{
  "url": "https://meuapp.com/webhooks/cleantrack",
  "events": [
    "cleaning_log.created",
    "equipment.overdue",
    "facility.updated"
  ],
  "is_active": true
}
```

**Response (201 Created):**
```json
{
  "id": 10,
  "url": "https://meuapp.com/webhooks/cleantrack",
  "events": [
    "cleaning_log.created",
    "equipment.overdue",
    "facility.updated"
  ],
  "secret": "whsec_abc123xyz789",
  "is_active": true,
  "created_at": "2025-01-22T19:00:00Z"
}
```

---

#### **Webhook Events (Eventos Disponíveis)**

```
cleaning_log.created         # Novo registro de limpeza criado
cleaning_log.updated         # Registro de limpeza atualizado
cleaning_log.deleted         # Registro de limpeza excluído

equipment.created            # Novo equipamento criado
equipment.updated            # Equipamento atualizado
equipment.deleted            # Equipamento excluído (soft delete)
equipment.overdue            # Equipamento está atrasado para limpeza

facility.created             # Nova facility criada
facility.updated             # Facility atualizada
facility.deleted             # Facility desativada

compliance.report_ready      # Relatório de conformidade gerado e pronto
compliance.threshold_breached # Taxa de conformidade abaixo do limite

user.created                 # Novo usuário criado
user.updated                 # Usuário atualizado
user.deleted                 # Usuário desativado
```

---

#### **Webhook Payload Examples**

**Event: `cleaning_log.created`**
```json
{
  "id": "evt_abc123",
  "type": "cleaning_log.created",
  "created_at": "2025-01-22T19:05:00Z",
  "data": {
    "cleaning_log": {
      "id": 568,
      "equipment": {
        "id": 1,
        "name": "Desfibrilador XYZ",
        "serial_number": "DEF-001-2025"
      },
      "facility": {
        "id": 456,
        "name": "Hospital Memorial"
      },
      "cleaned_by": {
        "id": 234,
        "name": "Maria Santos",
        "email": "maria@hospital.com"
      },
      "cleaned_at": "2025-01-22T09:00:00Z",
      "photo": "https://media.cleantrack.com/cleaning/568.jpg",
      "is_compliant": true,
      "duration_minutes": 12
    }
  }
}
```

---

**Event: `equipment.overdue`**
```json
{
  "id": "evt_def456",
  "type": "equipment.overdue",
  "created_at": "2025-01-22T20:00:00Z",
  "data": {
    "equipment": {
      "id": 5,
      "name": "Monitor Cardíaco ABC",
      "serial_number": "MON-045-2024",
      "category": "monitoring",
      "location": "UTI - Leito 2"
    },
    "facility": {
      "id": 456,
      "name": "Hospital Memorial"
    },
    "last_cleaning": {
      "id": 450,
      "cleaned_at": "2025-01-20T10:00:00Z",
      "cleaned_by": {
        "id": 234,
        "name": "Maria Santos"
      }
    },
    "should_have_been_cleaned_at": "2025-01-21T10:00:00Z",
    "overdue_hours": 33,
    "status": "critical"
  }
}
```

---

**Event: `compliance.report_ready`**
```json
{
  "id": "evt_ghi789",
  "type": "compliance.report_ready",
  "created_at": "2025-01-22T21:00:00Z",
  "data": {
    "report": {
      "id": "rpt_abc123xyz789",
      "facility": {
        "id": 456,
        "name": "Hospital Memorial"
      },
      "period": {
        "start_date": "2025-01-01",
        "end_date": "2025-01-31"
      },
      "format": "pdf",
      "url": "https://reports.cleantrack.com/compliance_456_202501.pdf",
      "expires_at": "2025-01-23T21:00:00Z",
      "file_size_bytes": 524288,
      "total_pages": 8,
      "summary": {
        "compliance_rate": 96.2,
        "total_cleanings": 1234,
        "overdue_equipment": 3
      }
    },
    "requested_by": {
      "id": 123,
      "name": "João Silva",
      "email": "joao@hospital.com"
    }
  }
}
```

---

**Event: `compliance.threshold_breached`**
```json
{
  "id": "evt_jkl012",
  "type": "compliance.threshold_breached",
  "created_at": "2025-01-22T22:00:00Z",
  "data": {
    "facility": {
      "id": 456,
      "name": "Hospital Memorial"
    },
    "threshold": {
      "metric": "compliance_rate",
      "limit": 95.0,
      "current_value": 92.8,
      "severity": "warning"
    },
    "period": {
      "start_date": "2025-01-01",
      "end_date": "2025-01-22"
    },
    "statistics": {
      "total_equipment": 45,
      "overdue_equipment": 5,
      "overdue_rate": 11.1
    }
  }
}
```

---

#### **Webhook Signature Verification**

**Header enviado:**
```
X-CleanTrack-Signature: t=1737570300,v1=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

**Formato:**
```
t={timestamp},v1={hmac_sha256_hex}
```

**Verificação em Python:**
```python
import hmac
import hashlib
import time

def verify_webhook(payload, signature_header, secret):
    """
    Verifica a assinatura do webhook CleanTrack

    Args:
        payload: Raw body da requisição (string)
        signature_header: Valor do header X-CleanTrack-Signature
        secret: Webhook secret (obtido ao criar webhook)

    Returns:
        bool: True se assinatura válida, False caso contrário
    """
    # Extrair timestamp e assinatura
    parts = signature_header.split(',')
    timestamp = int(parts[0].split('=')[1])
    signature = parts[1].split('=')[1]

    # Verificar timestamp (máximo 5 minutos de diferença)
    current_time = int(time.time())
    if abs(current_time - timestamp) > 300:  # 5 minutos
        return False

    # Calcular assinatura esperada
    signed_payload = f"{timestamp}.{payload}"
    expected_signature = hmac.new(
        secret.encode(),
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()

    # Comparar com timing-safe
    return hmac.compare_digest(expected_signature, signature)


# Exemplo de uso com Flask
from flask import Flask, request

app = Flask(__name__)
WEBHOOK_SECRET = "whsec_abc123xyz789"

@app.route('/webhooks/cleantrack', methods=['POST'])
def webhook():
    # Obter payload e assinatura
    payload = request.data.decode()
    signature = request.headers.get('X-CleanTrack-Signature')

    # Verificar assinatura
    if not verify_webhook(payload, signature, WEBHOOK_SECRET):
        return 'Invalid signature', 401

    # Processar evento
    event = request.json
    handle_webhook_event(event)

    return '', 200


def handle_webhook_event(event):
    event_type = event['type']

    if event_type == 'cleaning_log.created':
        log = event['data']['cleaning_log']
        print(f"✅ Nova limpeza: {log['equipment']['name']}")
        # Enviar notificação, atualizar dashboard, etc.

    elif event_type == 'equipment.overdue':
        equipment = event['data']['equipment']
        overdue_hours = event['data']['overdue_hours']
        print(f"⚠️ Equipamento atrasado: {equipment['name']} ({overdue_hours}h)")
        # Enviar alerta urgente

    elif event_type == 'compliance.report_ready':
        report = event['data']['report']
        print(f"📄 Relatório pronto: {report['url']}")
        # Enviar email com link do relatório

    elif event_type == 'compliance.threshold_breached':
        threshold = event['data']['threshold']
        print(f"🚨 Conformidade baixa: {threshold['current_value']}%")
        # Escalar para gerência
```

---

**Verificação em Node.js:**
```javascript
const crypto = require('crypto');

function verifyWebhook(payload, signatureHeader, secret) {
  // Extrair timestamp e assinatura
  const parts = signatureHeader.split(',');
  const timestamp = parseInt(parts[0].split('=')[1]);
  const signature = parts[1].split('=')[1];

  // Verificar timestamp (máximo 5 minutos)
  const currentTime = Math.floor(Date.now() / 1000);
  if (Math.abs(currentTime - timestamp) > 300) {
    return false;
  }

  // Calcular assinatura esperada
  const signedPayload = `${timestamp}.${payload}`;
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(signedPayload)
    .digest('hex');

  // Comparar com timing-safe
  return crypto.timingSafeEqual(
    Buffer.from(expectedSignature),
    Buffer.from(signature)
  );
}

// Exemplo com Express
const express = require('express');
const app = express();

const WEBHOOK_SECRET = 'whsec_abc123xyz789';

app.post('/webhooks/cleantrack', express.raw({ type: 'application/json' }), (req, res) => {
  const payload = req.body.toString();
  const signature = req.headers['x-cleantrack-signature'];

  // Verificar assinatura
  if (!verifyWebhook(payload, signature, WEBHOOK_SECRET)) {
    return res.status(401).send('Invalid signature');
  }

  // Processar evento
  const event = JSON.parse(payload);
  handleWebhookEvent(event);

  res.status(200).send('');
});

function handleWebhookEvent(event) {
  switch (event.type) {
    case 'cleaning_log.created':
      const log = event.data.cleaning_log;
      console.log(`✅ Nova limpeza: ${log.equipment.name}`);
      break;

    case 'equipment.overdue':
      const equipment = event.data.equipment;
      console.log(`⚠️ Equipamento atrasado: ${equipment.name}`);
      break;

    case 'compliance.report_ready':
      const report = event.data.report;
      console.log(`📄 Relatório pronto: ${report.url}`);
      break;
  }
}
```

---

## ⚠️ **RATE LIMITING**

### **Limites**
```
Padrão:      1.000 requisições/hora
Enterprise:  10.000 requisições/hora
Burst:       50 requisições/minuto
```

### **Headers de Response**
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1737574800
```

### **Response (429 Too Many Requests):**
```json
{
  "error": "rate_limit_exceeded",
  "message": "Você excedeu o limite de 1.000 requisições/hora",
  "retry_after": 3600
}
```

---

## 🚨 **CÓDIGOS DE ERRO**

### **Formato de Erro Padrão**
```json
{
  "error": "invalid_request",
  "message": "O campo 'name' é obrigatório",
  "details": {
    "name": ["Este campo é obrigatório."]
  },
  "request_id": "req_abc123"
}
```

---

### **Códigos HTTP**

```
200 OK                  - Sucesso
201 Created             - Recurso criado
204 No Content          - Sucesso sem conteúdo
400 Bad Request         - Requisição inválida
401 Unauthorized        - Token inválido ou ausente
403 Forbidden           - Sem permissão para recurso
404 Not Found           - Recurso não encontrado
409 Conflict            - Conflito (ex: serial duplicado)
422 Unprocessable Entity - Validação falhou
429 Too Many Requests   - Rate limit excedido
500 Internal Server Error - Erro no servidor
503 Service Unavailable - Serviço temporariamente indisponível
```

---

### **Códigos de Erro Customizados**

```json
{
  "invalid_request": "Requisição inválida",
  "invalid_token": "Token JWT inválido ou expirado",
  "invalid_credentials": "Email ou senha incorretos",
  "permission_denied": "Sem permissão para este recurso",
  "resource_not_found": "Recurso não encontrado",
  "duplicate_resource": "Recurso já existe (ex: serial duplicado)",
  "validation_error": "Erro de validação de dados",
  "rate_limit_exceeded": "Limite de requisições excedido",
  "internal_error": "Erro interno do servidor"
}
```

---

## 📚 **SDKs E BIBLIOTECAS**

### **Python SDK**
```python
# Instalação
pip install cleantrack-sdk

# Uso
from cleantrack import CleanTrack

client = CleanTrack(api_key="your_api_key")

# Listar equipamentos
equipment_list = client.equipment.list(facility_id=456)

# Criar equipamento
new_equipment = client.equipment.create(
    facility_id=456,
    name="Ventilador ABC",
    serial_number="VEN-023-2025",
    category="life_support"
)

# Gerar QR code
qr_svg = client.equipment.qr_code(equipment_id=1, format="svg")

# Criar limpeza
cleaning = client.cleaning_logs.create(
    equipment_id=1,
    photo=open("photo.jpg", "rb"),
    notes="Limpeza de rotina"
)
```

---

### **JavaScript SDK**
```javascript
// Instalação
npm install @cleantrack/sdk

// Uso
import CleanTrack from '@cleantrack/sdk';

const client = new CleanTrack({ apiKey: 'your_api_key' });

// Listar equipamentos
const equipment = await client.equipment.list({ facilityId: 456 });

// Criar equipamento
const newEquipment = await client.equipment.create({
  facilityId: 456,
  name: 'Ventilador ABC',
  serialNumber: 'VEN-023-2025',
  category: 'life_support'
});

// Gerar QR code
const qrSvg = await client.equipment.qrCode(1, { format: 'svg' });

// Criar limpeza
const cleaning = await client.cleaningLogs.create({
  equipmentId: 1,
  photo: fileInput.files[0],
  notes: 'Limpeza de rotina'
});
```

---

## 🔐 **SEGURANÇA**

### **HTTPS Obrigatório**
```
✅ TLS 1.2+ (obrigatório)
❌ HTTP não suportado (redirect para HTTPS)
```

### **Autenticação**
```
✅ JWT (JSON Web Tokens)
✅ Bearer Token em header Authorization
✅ Refresh token para renovação
✅ Revoke token em logout
```

### **Permissões (RBAC)**
```
Admin:      Acesso total (todas facilities)
Manager:    Apenas facilities gerenciadas
Technician: Read-only + criar cleaning logs
Auditor:    Read-only (sem criar/editar)
```

### **CORS**
```
Origens permitidas:
├─ app.cleantrack.com
├─ *.cleantrack.com (subdomínios)
└─ Origens customizadas (whitelist por cliente)

Headers:
Access-Control-Allow-Origin: https://app.cleantrack.com
Access-Control-Allow-Methods: GET, POST, PATCH, DELETE
Access-Control-Allow-Headers: Authorization, Content-Type
```

---

## 📝 **VERSIONAMENTO**

### **Estratégia**
```
Base URL: https://api.cleantrack.com/v1

Versões:
├─ v1 (atual) - Estável até 2027
├─ v2 (futura) - Planejada para 2026
└─ Legacy: Suportado por 12 meses após deprecation
```

### **Header de Versão (Alternativo)**
```http
GET /equipment/
Authorization: Bearer {token}
Accept: application/vnd.cleantrack.v1+json
```

---

## 🧪 **AMBIENTE DE TESTE (SANDBOX)**

### **Base URL Sandbox**
```
https://sandbox-api.cleantrack.com/v1
```

### **Credenciais de Teste**
```
Email:    test@cleantrack.com
Password: test123

API Key:  test_sk_abc123xyz789
```

### **Dados de Teste**
```
Facility ID: 999
Equipment ID: 9999
Cleaning Log ID: 99999
```

### **Reset de Dados**
```http
POST /sandbox/reset/
Authorization: Bearer {test_token}
```

---

## 📖 **EXEMPLOS DE USO**

### **Exemplo 1: Listar Equipamentos Atrasados**
```python
import requests

# Autenticação
response = requests.post(
    "https://api.cleantrack.com/v1/auth/token/",
    json={
        "email": "admin@hospital.com",
        "password": "senha_segura"
    }
)
token = response.json()["access_token"]

# Listar equipamentos atrasados
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "https://api.cleantrack.com/v1/facilities/456/equipment/",
    headers=headers,
    params={"is_overdue": True}
)

overdue_equipment = response.json()["results"]
print(f"Equipamentos atrasados: {len(overdue_equipment)}")
```

---

### **Exemplo 2: Criar Equipamento + Gerar QR Code**
```javascript
// Autenticação
const authResponse = await fetch('https://api.cleantrack.com/v1/auth/token/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'admin@hospital.com',
    password: 'senha_segura'
  })
});
const { access_token } = await authResponse.json();

// Criar equipamento
const createResponse = await fetch('https://api.cleantrack.com/v1/equipment/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    facility_id: 456,
    name: 'Bomba de Infusão',
    serial_number: 'BOM-045-2025',
    category: 'monitoring',
    location: 'Emergência',
    cleaning_frequency_hours: 4
  })
});
const equipment = await createResponse.json();

// Gerar QR code
const qrResponse = await fetch(
  `https://api.cleantrack.com/v1/equipment/${equipment.id}/qr/?format=svg`,
  { headers: { 'Authorization': `Bearer ${access_token}` } }
);
const qrSvg = await qrResponse.text();

console.log('Equipamento criado:', equipment);
console.log('QR Code gerado:', qrSvg);
```

---

### **Exemplo 3: Integração com Sensores IoT**

**Cenário:** Sensor automático detecta limpeza e registra no CleanTrack via API

```python
"""
IoT Integration Example - Sensor de Limpeza Automático

Hardware:
- Raspberry Pi 4 + Camera Module
- Sensor de movimento PIR
- LED de status

Fluxo:
1. Sensor PIR detecta movimento próximo ao equipamento
2. Câmera captura foto da limpeza
3. Sistema envia dados para CleanTrack API
4. LED acende verde (sucesso) ou vermelho (erro)
"""

import requests
import base64
import time
from datetime import datetime
from picamera import PiCamera
import RPi.GPIO as GPIO

# Configuração
CLEANTRACK_API = "https://api.cleantrack.com/v1"
API_TOKEN = "your_api_token_here"
EQUIPMENT_ID = 1  # ID do equipamento monitorado

# GPIO
PIR_SENSOR_PIN = 17  # Sensor de movimento
LED_GREEN_PIN = 22   # LED verde (sucesso)
LED_RED_PIN = 27     # LED vermelho (erro)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_SENSOR_PIN, GPIO.IN)
GPIO.setup(LED_GREEN_PIN, GPIO.OUT)
GPIO.setup(LED_RED_PIN, GPIO.OUT)

# Camera
camera = PiCamera()
camera.resolution = (1920, 1080)


def capture_photo():
    """Captura foto e retorna em Base64"""
    photo_path = f"/tmp/cleaning_{int(time.time())}.jpg"

    # Capturar foto
    camera.capture(photo_path)

    # Converter para Base64
    with open(photo_path, "rb") as f:
        photo_bytes = f.read()
        photo_base64 = base64.b64encode(photo_bytes).decode()

    return f"data:image/jpeg;base64,{photo_base64}"


def register_cleaning(equipment_id, photo_base64):
    """Registra limpeza no CleanTrack"""
    url = f"{CLEANTRACK_API}/cleaning-logs/"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "equipment_id": equipment_id,
        "cleaned_at": datetime.now().isoformat(),
        "photo_base64": photo_base64,
        "notes": "Limpeza detectada automaticamente via sensor IoT",
        "duration_minutes": None  # Sensor não mede duração
    }

    response = requests.post(url, headers=headers, json=data)
    return response


def indicate_success():
    """LED verde por 3 segundos"""
    GPIO.output(LED_GREEN_PIN, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(LED_GREEN_PIN, GPIO.LOW)


def indicate_error():
    """LED vermelho piscando"""
    for _ in range(6):
        GPIO.output(LED_RED_PIN, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(LED_RED_PIN, GPIO.LOW)
        time.sleep(0.25)


def main():
    """Loop principal do sensor"""
    print("🔌 Sensor IoT CleanTrack iniciado")
    print(f"📍 Monitorando equipamento ID: {EQUIPMENT_ID}")
    print("⏳ Aguardando detecção de limpeza...\n")

    cooldown = 0  # Evitar múltiplas detecções

    try:
        while True:
            # Detectar movimento
            if GPIO.input(PIR_SENSOR_PIN) and cooldown == 0:
                print(f"🚨 [{datetime.now()}] Movimento detectado!")

                # Aguardar 2 segundos (técnico posicionar)
                print("📸 Aguardando 2s para captura...")
                time.sleep(2)

                # Capturar foto
                print("📸 Capturando foto...")
                photo_base64 = capture_photo()
                print(f"✅ Foto capturada ({len(photo_base64)} bytes)")

                # Registrar no CleanTrack
                print("☁️  Enviando para CleanTrack API...")
                response = register_cleaning(EQUIPMENT_ID, photo_base64)

                if response.status_code == 201:
                    cleaning = response.json()
                    print(f"✅ Limpeza registrada com sucesso!")
                    print(f"   ID: {cleaning['id']}")
                    print(f"   Equipamento: {cleaning['equipment']['name']}")
                    print(f"   Foto: {cleaning['photo']}")
                    indicate_success()
                else:
                    print(f"❌ Erro ao registrar limpeza:")
                    print(f"   Status: {response.status_code}")
                    print(f"   Erro: {response.json()}")
                    indicate_error()

                # Cooldown de 5 minutos (evitar duplicatas)
                print("⏳ Cooldown de 5 minutos ativado\n")
                cooldown = 300  # 5 minutos em segundos

            # Decrementar cooldown
            if cooldown > 0:
                cooldown -= 1
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Encerrando sensor...")
        GPIO.cleanup()
        camera.close()


if __name__ == "__main__":
    main()
```

---

### **Exemplo 4: Integração com Sistema Hospitalar (HL7/FHIR)**

**Cenário:** Sistema hospitalar envia dados de limpeza de equipamentos médicos

```python
"""
HL7/FHIR Integration - Hospital Information System (HIS)

Integração bidirecional:
- HIS → CleanTrack: Registra limpezas
- CleanTrack → HIS: Alerta sobre equipamentos atrasados
"""

import requests
from datetime import datetime
from fhir.resources.device import Device
from fhir.resources.procedure import Procedure


class CleanTrackHISIntegration:
    """Integração entre CleanTrack e Sistema Hospitalar"""

    def __init__(self, api_url, api_token):
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    def sync_equipment_from_fhir(self, fhir_device: Device):
        """
        Sincroniza equipamento do FHIR para CleanTrack

        FHIR Device → CleanTrack Equipment
        """
        # Extrair dados do Device FHIR
        equipment_data = {
            "name": fhir_device.deviceName[0].name,
            "serial_number": fhir_device.serialNumber,
            "manufacturer": fhir_device.manufacturer,
            "model": fhir_device.modelNumber,
            "location": fhir_device.location.display if fhir_device.location else None,
            "facility_id": self._get_facility_id_from_fhir(fhir_device)
        }

        # Criar equipamento no CleanTrack
        response = requests.post(
            f"{self.api_url}/equipment/",
            headers=self.headers,
            json=equipment_data
        )

        if response.status_code == 201:
            equipment = response.json()
            print(f"✅ Equipamento sincronizado: {equipment['name']} (ID: {equipment['id']})")
            return equipment
        else:
            print(f"❌ Erro ao sincronizar: {response.json()}")
            return None

    def register_cleaning_from_procedure(self, fhir_procedure: Procedure, photo_path: str):
        """
        Registra limpeza a partir de um Procedure FHIR

        FHIR Procedure (limpeza) → CleanTrack Cleaning Log
        """
        # Ler e converter foto
        import base64
        with open(photo_path, "rb") as f:
            photo_base64 = base64.b64encode(f.read()).decode()
            photo_data_uri = f"data:image/jpeg;base64,{photo_base64}"

        # Extrair dados do Procedure
        cleaning_data = {
            "equipment_serial": fhir_procedure.subject.identifier.value,
            "cleaned_at": fhir_procedure.performedDateTime.isoformat(),
            "photo_base64": photo_data_uri,
            "notes": fhir_procedure.note[0].text if fhir_procedure.note else None
        }

        # Registrar no CleanTrack
        response = requests.post(
            f"{self.api_url}/cleaning-logs/",
            headers=self.headers,
            json=cleaning_data
        )

        return response.json() if response.status_code == 201 else None

    def get_overdue_equipment_for_his(self, facility_id: int):
        """
        Consulta equipamentos atrasados e retorna em formato HIS
        """
        response = requests.get(
            f"{self.api_url}/facilities/{facility_id}/equipment/",
            headers=self.headers,
            params={"is_overdue": True}
        )

        if response.status_code == 200:
            equipment_list = response.json()["results"]

            # Gerar alertas para HIS
            alerts = []
            for eq in equipment_list:
                alerts.append({
                    "equipment_id": eq["id"],
                    "equipment_name": eq["name"],
                    "serial_number": eq["serial_number"],
                    "location": eq["location"],
                    "last_cleaning": eq["last_cleaning"]["cleaned_at"],
                    "overdue_status": "CRITICAL" if eq["is_overdue"] else "OK",
                    "priority": "HIGH"
                })

            return alerts
        else:
            return []

    def _get_facility_id_from_fhir(self, fhir_device):
        """Helper para mapear FHIR Organization → CleanTrack Facility"""
        # Implementação depende do mapeamento específico
        return 456  # Placeholder


# Uso
if __name__ == "__main__":
    integration = CleanTrackHISIntegration(
        api_url="https://api.cleantrack.com/v1",
        api_token="your_api_token"
    )

    # Exemplo: Consultar equipamentos atrasados
    overdue = integration.get_overdue_equipment_for_his(facility_id=456)
    print(f"📋 {len(overdue)} equipamentos atrasados:")
    for alert in overdue:
        print(f"   ⚠️ {alert['equipment_name']} - {alert['location']} ({alert['overdue_status']})")
```

---

### **Exemplo 5: Automação via Webhook (Slack + PagerDuty)**

**Cenário:** Equipamento atrasado dispara alertas no Slack e PagerDuty

```python
"""
Webhook Automation - Multi-Channel Alerts

CleanTrack Webhook → Slack + PagerDuty
"""

from flask import Flask, request
import requests
import hmac
import hashlib

app = Flask(__name__)

# Configuração
WEBHOOK_SECRET = "whsec_abc123xyz789"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
PAGERDUTY_API_KEY = "your_pagerduty_api_key"
PAGERDUTY_SERVICE_ID = "your_service_id"


def verify_webhook(payload, signature_header, secret):
    """Verificar assinatura do webhook CleanTrack"""
    parts = signature_header.split(',')
    timestamp = int(parts[0].split('=')[1])
    signature = parts[1].split('=')[1]

    signed_payload = f"{timestamp}.{payload}"
    expected = hmac.new(
        secret.encode(),
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)


def send_slack_alert(equipment_name, overdue_hours, location):
    """Enviar alerta para Slack"""
    message = {
        "text": f"🚨 *Equipamento Atrasado para Limpeza* 🚨",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "⚠️ Alerta de Conformidade"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Equipamento:*\n{equipment_name}"},
                    {"type": "mrkdwn", "text": f"*Localização:*\n{location}"},
                    {"type": "mrkdwn", "text": f"*Atraso:*\n{overdue_hours} horas"},
                    {"type": "mrkdwn", "text": f"*Status:*\n🔴 CRÍTICO"}
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Ver Detalhes"},
                        "url": "https://app.cleantrack.com/equipment/5"
                    }
                ]
            }
        ]
    }

    requests.post(SLACK_WEBHOOK_URL, json=message)


def create_pagerduty_incident(equipment_name, overdue_hours):
    """Criar incidente no PagerDuty"""
    headers = {
        "Authorization": f"Token token={PAGERDUTY_API_KEY}",
        "Content-Type": "application/json"
    }

    incident = {
        "incident": {
            "type": "incident",
            "title": f"Equipamento atrasado: {equipment_name}",
            "service": {
                "id": PAGERDUTY_SERVICE_ID,
                "type": "service_reference"
            },
            "urgency": "high",
            "body": {
                "type": "incident_body",
                "details": f"{equipment_name} está {overdue_hours}h atrasado para limpeza."
            }
        }
    }

    requests.post(
        "https://api.pagerduty.com/incidents",
        headers=headers,
        json=incident
    )


@app.route('/webhooks/cleantrack', methods=['POST'])
def webhook():
    # Verificar assinatura
    payload = request.data.decode()
    signature = request.headers.get('X-CleanTrack-Signature')

    if not verify_webhook(payload, signature, WEBHOOK_SECRET):
        return 'Invalid signature', 401

    # Processar evento
    event = request.json

    if event['type'] == 'equipment.overdue':
        equipment = event['data']['equipment']
        overdue_hours = event['data']['overdue_hours']

        print(f"⚠️ Equipamento atrasado: {equipment['name']} ({overdue_hours}h)")

        # Enviar alertas
        send_slack_alert(
            equipment_name=equipment['name'],
            overdue_hours=overdue_hours,
            location=equipment['location']
        )

        # Se crítico (>24h), criar incidente PagerDuty
        if overdue_hours > 24:
            create_pagerduty_incident(equipment['name'], overdue_hours)
            print(f"🚨 Incidente PagerDuty criado (overdue > 24h)")

    elif event['type'] == 'compliance.threshold_breached':
        threshold = event['data']['threshold']
        facility = event['data']['facility']

        # Enviar alerta para Slack
        message = {
            "text": f"🚨 *Taxa de Conformidade Baixa*\n"
                    f"Facility: {facility['name']}\n"
                    f"Taxa atual: {threshold['current_value']}% (meta: {threshold['limit']}%)"
        }
        requests.post(SLACK_WEBHOOK_URL, json=message)

    return '', 200


if __name__ == '__main__':
    app.run(port=5000)
```

---

## 📊 **CHANGELOG**

### **v1.0.0 (Q1/2026) - Initial Release**
```
✅ Autenticação JWT
✅ Endpoints de facilities, equipment, cleaning logs
✅ QR code generation (SVG/PNG)
✅ Reports (JSON/PDF/Excel)
✅ Webhooks
✅ Rate limiting
✅ RBAC (Role-Based Access Control)
✅ SDKs (Python, JavaScript)
```

### **v1.1.0 (Q2/2026) - Planned**
```
🔜 Batch operations (criar múltiplos equipamentos)
🔜 GraphQL API (alternativa REST)
🔜 Real-time subscriptions (WebSockets)
🔜 Analytics API (métricas avançadas)
🔜 Mobile SDKs (iOS, Android native)
```

---

## 🆘 **SUPORTE**

### **Documentação**
```
📖 Docs: https://docs.cleantrack.com/api
📺 Video tutorials: https://cleantrack.com/api-tutorials
💬 Community forum: https://community.cleantrack.com
```

### **Contato**
```
📧 Email: api-support@cleantrack.com
💬 Slack: cleantrack-developers.slack.com
🐛 Issues: github.com/cleantrack/api-issues
```

### **Status da API**
```
📊 Status page: https://status.cleantrack.com
🔔 Incident alerts: Via email/Slack
```

---

**API REST DOCUMENTAÇÃO COMPLETA - PRONTA PARA FASE 2!** 🚀🔌

**Próximo passo:** Implementar endpoints em Django REST Framework (Q1/2026)
