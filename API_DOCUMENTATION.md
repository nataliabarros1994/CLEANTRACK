# 🔌 CleanTrack API Documentation

Complete REST API documentation for CleanTrack healthcare compliance platform.

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Base URL](#base-url)
4. [Rate Limiting](#rate-limiting)
5. [Endpoints](#endpoints)
6. [Error Handling](#error-handling)
7. [Examples](#examples)
8. [Webhooks](#webhooks)

---

## Overview

CleanTrack provides a RESTful API for programmatic access to:
- Equipment management
- Cleaning log creation and retrieval
- Facility management
- Compliance metrics
- User management

### API Features
- ✅ JSON request/response format
- ✅ Token-based authentication
- ✅ Rate limiting
- ✅ Pagination support
- ✅ Filtering and search
- ✅ CORS enabled

---

## Authentication

### Session Authentication (Web)
Used for browser-based requests when logged into Django admin.

**Example:**
```javascript
fetch('/api/equipment/', {
  credentials: 'include',  // Send session cookie
  headers: {
    'X-CSRFToken': getCookie('csrftoken')
  }
})
```

### Token Authentication (API)
For external integrations and mobile apps.

**Get Token:**
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your_password"
}
```

**Response:**
```json
{
  "token": "abc123def456ghi789",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**Use Token:**
```http
GET /api/equipment/
Authorization: Token abc123def456ghi789
```

---

## Base URL

### Development
```
http://localhost:8000/api/
```

### Production
```
https://cleantrack-api.onrender.com/api/
```

---

## Rate Limiting

| User Type | Rate Limit |
|-----------|------------|
| Anonymous | 100 requests/hour |
| Authenticated | 1000 requests/hour |
| Admin | Unlimited |

**Rate Limit Headers:**
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1640000000
```

---

## Endpoints

### Equipment Management

#### List Equipment
```http
GET /api/equipment/
```

**Query Parameters:**
- `facility` (int): Filter by facility ID
- `category` (string): Filter by equipment category
- `search` (string): Search by name or serial number
- `page` (int): Page number (default: 1)
- `page_size` (int): Items per page (default: 20, max: 100)

**Response:**
```json
{
  "count": 42,
  "next": "http://localhost:8000/api/equipment/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "X-Ray Machine",
      "serial_number": "XR-12345",
      "category": "Radiology",
      "facility": {
        "id": 1,
        "name": "Main Hospital"
      },
      "qr_code": "http://localhost:8000/media/qr_codes/XR-12345.png",
      "public_token": "abc123def456",
      "token_expires_at": "2025-01-24T15:30:00Z",
      "last_cleaned_at": "2025-01-24T10:00:00Z",
      "cleaning_frequency_days": 1,
      "is_overdue": false,
      "created_at": "2025-01-01T00:00:00Z"
    }
  ]
}
```

#### Get Equipment Details
```http
GET /api/equipment/{id}/
```

**Response:**
```json
{
  "id": 1,
  "name": "X-Ray Machine",
  "serial_number": "XR-12345",
  "category": "Radiology",
  "description": "Digital X-ray system for diagnostic imaging",
  "manufacturer": "GE Healthcare",
  "model": "Revolution EVO",
  "location": "Radiology Department - Room 3",
  "facility": {
    "id": 1,
    "name": "Main Hospital",
    "address": "123 Medical Plaza"
  },
  "qr_code": "http://localhost:8000/media/qr_codes/XR-12345.png",
  "public_token": "abc123def456",
  "token_expires_at": "2025-01-24T15:30:00Z",
  "token_valid_minutes": 5,
  "cleaning_frequency_days": 1,
  "last_cleaned_at": "2025-01-24T10:00:00Z",
  "next_cleaning_due": "2025-01-25T10:00:00Z",
  "is_overdue": false,
  "total_cleanings": 127,
  "compliance_rate": 95.5,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-24T10:05:00Z"
}
```

#### Create Equipment
```http
POST /api/equipment/
Content-Type: application/json
Authorization: Token xxx

{
  "name": "MRI Scanner",
  "serial_number": "MRI-67890",
  "category": "Radiology",
  "description": "3T MRI for advanced imaging",
  "manufacturer": "Siemens",
  "model": "MAGNETOM Skyra",
  "location": "Radiology Department - Room 5",
  "facility": 1,
  "cleaning_frequency_days": 1,
  "token_valid_minutes": 5
}
```

**Response:** `201 Created`
```json
{
  "id": 2,
  "name": "MRI Scanner",
  "serial_number": "MRI-67890",
  "qr_code": "http://localhost:8000/media/qr_codes/MRI-67890.png",
  "public_token": "xyz789abc123",
  "created_at": "2025-01-24T12:00:00Z"
}
```

#### Update Equipment
```http
PUT /api/equipment/{id}/
Content-Type: application/json
Authorization: Token xxx

{
  "name": "MRI Scanner - Updated",
  "location": "Radiology Department - Room 6",
  "cleaning_frequency_days": 2
}
```

#### Delete Equipment
```http
DELETE /api/equipment/{id}/
Authorization: Token xxx
```

**Response:** `204 No Content`

#### Generate New QR Code
```http
POST /api/equipment/{id}/generate-qr/
Authorization: Token xxx
```

**Response:**
```json
{
  "qr_code": "http://localhost:8000/media/qr_codes/XR-12345.png",
  "public_token": "new_token_here",
  "token_expires_at": "2025-01-24T16:00:00Z"
}
```

#### Download Equipment Label (PDF)
```http
GET /api/equipment/{id}/label/
Authorization: Token xxx
```

**Response:** PDF file (2.4" x 1.2" thermal label)

---

### Cleaning Logs

#### List Cleaning Logs
```http
GET /api/cleaning-logs/
```

**Query Parameters:**
- `equipment` (int): Filter by equipment ID
- `facility` (int): Filter by facility ID
- `cleaned_by` (string): Filter by technician name
- `date_from` (date): Filter logs after this date (YYYY-MM-DD)
- `date_to` (date): Filter logs before this date
- `page` (int): Page number

**Response:**
```json
{
  "count": 156,
  "next": "http://localhost:8000/api/cleaning-logs/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "equipment": {
        "id": 1,
        "name": "X-Ray Machine",
        "serial_number": "XR-12345"
      },
      "cleaned_by": "John Doe",
      "cleaned_at": "2025-01-24T10:00:00Z",
      "notes": "Thorough cleaning completed",
      "photo": "http://localhost:8000/media/cleaning_photos/photo_123.jpg",
      "token_used": "abc123def456",
      "created_at": "2025-01-24T10:01:00Z"
    }
  ]
}
```

#### Get Cleaning Log Details
```http
GET /api/cleaning-logs/{id}/
```

#### Create Cleaning Log (Authenticated)
```http
POST /api/cleaning-logs/
Content-Type: multipart/form-data
Authorization: Token xxx

equipment: 1
cleaned_by: Jane Smith
notes: Deep cleaning with disinfectant
photo: [binary file]
```

**Response:** `201 Created`
```json
{
  "id": 2,
  "equipment": 1,
  "cleaned_by": "Jane Smith",
  "cleaned_at": "2025-01-24T12:30:00Z",
  "notes": "Deep cleaning with disinfectant",
  "photo": "http://localhost:8000/media/cleaning_photos/photo_124.jpg",
  "created_at": "2025-01-24T12:30:15Z"
}
```

#### Register Cleaning (Public - No Auth Required)
```http
POST /api/register-cleaning/{token}/
Content-Type: multipart/form-data

cleaned_by: Mike Johnson
notes: Quick maintenance clean
photo: [binary file]
```

**Response:** `201 Created`
```json
{
  "success": true,
  "message": "Cleaning recorded successfully",
  "cleaning_log_id": 3,
  "equipment": {
    "id": 1,
    "name": "X-Ray Machine",
    "serial_number": "XR-12345"
  },
  "cleaned_at": "2025-01-24T14:00:00Z"
}
```

**Error Response (Token Expired):**
```json
{
  "success": false,
  "error": "Token expired",
  "message": "This QR code has expired. Please request a new one.",
  "expired_at": "2025-01-24T13:55:00Z"
}
```

---

### Facilities

#### List Facilities
```http
GET /api/facilities/
Authorization: Token xxx
```

**Response:**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "name": "Main Hospital",
      "address": "123 Medical Plaza, San Francisco, CA",
      "phone": "+1-555-0100",
      "email": "contact@mainhospital.com",
      "is_active": true,
      "equipment_count": 42,
      "compliance_rate": 94.5,
      "created_at": "2025-01-01T00:00:00Z"
    }
  ]
}
```

#### Get Facility Details
```http
GET /api/facilities/{id}/
Authorization: Token xxx
```

#### Get Facility Compliance Metrics
```http
GET /api/facilities/{id}/compliance/
Authorization: Token xxx
```

**Response:**
```json
{
  "facility_id": 1,
  "facility_name": "Main Hospital",
  "total_equipment": 42,
  "cleaned_today": 38,
  "overdue": 2,
  "upcoming_due": 5,
  "compliance_rate": 94.5,
  "average_cleaning_time": "00:03:45",
  "total_cleanings_this_month": 1247,
  "breakdown_by_category": {
    "Radiology": {
      "total": 10,
      "compliant": 9,
      "overdue": 1,
      "rate": 90.0
    },
    "Laboratory": {
      "total": 15,
      "compliant": 15,
      "overdue": 0,
      "rate": 100.0
    }
  },
  "last_updated": "2025-01-24T15:00:00Z"
}
```

---

### Users

#### List Users
```http
GET /api/users/
Authorization: Token xxx
```

**Query Parameters:**
- `role` (string): Filter by role (admin, manager, technician)
- `facility` (int): Filter by facility ID

#### Get User Profile
```http
GET /api/users/me/
Authorization: Token xxx
```

**Response:**
```json
{
  "id": 5,
  "email": "john.doe@hospital.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "technician",
  "facilities": [
    {
      "id": 1,
      "name": "Main Hospital"
    }
  ],
  "total_cleanings": 523,
  "joined_at": "2024-06-15T00:00:00Z"
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Resource deleted successfully |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

### Error Response Format

```json
{
  "error": "ValidationError",
  "message": "Invalid input data",
  "details": {
    "serial_number": [
      "This field is required."
    ],
    "facility": [
      "Invalid facility ID."
    ]
  },
  "timestamp": "2025-01-24T15:30:00Z"
}
```

---

## Examples

### Python (requests)

```python
import requests

# Configuration
BASE_URL = "http://localhost:8000/api"
TOKEN = "your_auth_token_here"

headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

# List equipment
response = requests.get(f"{BASE_URL}/equipment/", headers=headers)
equipment = response.json()
print(f"Total equipment: {equipment['count']}")

# Create equipment
new_equipment = {
    "name": "CT Scanner",
    "serial_number": "CT-99999",
    "category": "Radiology",
    "facility": 1,
    "cleaning_frequency_days": 1
}
response = requests.post(
    f"{BASE_URL}/equipment/",
    json=new_equipment,
    headers=headers
)
created = response.json()
print(f"Created equipment ID: {created['id']}")

# Register cleaning (no auth required)
token = "abc123def456"
files = {"photo": open("cleaning_photo.jpg", "rb")}
data = {
    "cleaned_by": "John Doe",
    "notes": "Routine cleaning"
}
response = requests.post(
    f"{BASE_URL}/register-cleaning/{token}/",
    files=files,
    data=data
)
result = response.json()
print(f"Cleaning recorded: {result['success']}")
```

### JavaScript (fetch)

```javascript
const BASE_URL = "http://localhost:8000/api";
const TOKEN = "your_auth_token_here";

// List equipment
async function listEquipment() {
  const response = await fetch(`${BASE_URL}/equipment/`, {
    headers: {
      "Authorization": `Token ${TOKEN}`
    }
  });
  const data = await response.json();
  console.log(`Total equipment: ${data.count}`);
  return data.results;
}

// Create equipment
async function createEquipment(equipment) {
  const response = await fetch(`${BASE_URL}/equipment/`, {
    method: "POST",
    headers: {
      "Authorization": `Token ${TOKEN}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(equipment)
  });
  const created = await response.json();
  console.log(`Created equipment ID: ${created.id}`);
  return created;
}

// Register cleaning via QR code
async function registerCleaning(token, formData) {
  const response = await fetch(`${BASE_URL}/register-cleaning/${token}/`, {
    method: "POST",
    body: formData  // FormData with photo + fields
  });
  const result = await response.json();
  console.log(`Cleaning recorded: ${result.success}`);
  return result;
}

// Example usage
const equipment = {
  name: "Ultrasound Machine",
  serial_number: "US-88888",
  category: "Radiology",
  facility: 1,
  cleaning_frequency_days: 1
};

createEquipment(equipment).then(data => {
  console.log("Equipment created:", data);
});
```

### cURL

```bash
# List equipment
curl -X GET "http://localhost:8000/api/equipment/" \
  -H "Authorization: Token your_token_here"

# Create equipment
curl -X POST "http://localhost:8000/api/equipment/" \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MRI Scanner",
    "serial_number": "MRI-77777",
    "category": "Radiology",
    "facility": 1,
    "cleaning_frequency_days": 1
  }'

# Register cleaning (public endpoint)
curl -X POST "http://localhost:8000/api/register-cleaning/abc123def456/" \
  -F "cleaned_by=John Doe" \
  -F "notes=Routine cleaning" \
  -F "photo=@cleaning_photo.jpg"

# Get compliance metrics
curl -X GET "http://localhost:8000/api/facilities/1/compliance/" \
  -H "Authorization: Token your_token_here"
```

---

## Webhooks

### Stripe Webhooks

CleanTrack listens for Stripe webhook events for subscription management.

**Endpoint:**
```
POST /webhooks/stripe/
```

**Supported Events:**
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `invoice.payment_succeeded`
- `invoice.payment_failed`

**Configuration:**
1. Go to Stripe Dashboard → Developers → Webhooks
2. Add endpoint: `https://your-domain.com/webhooks/stripe/`
3. Select events to listen for
4. Copy webhook secret to `.env` as `STRIPE_WEBHOOK_SECRET`

**Example Event:**
```json
{
  "id": "evt_123",
  "type": "customer.subscription.created",
  "data": {
    "object": {
      "id": "sub_123",
      "customer": "cus_123",
      "status": "active",
      "items": {
        "data": [
          {
            "price": {
              "id": "price_123",
              "product": "prod_123"
            }
          }
        ]
      }
    }
  }
}
```

---

## Pagination

All list endpoints support pagination.

**Default:** 20 items per page
**Maximum:** 100 items per page

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)

**Response Format:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/equipment/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## Filtering & Search

### Filtering
```http
GET /api/equipment/?facility=1&category=Radiology
```

### Search
```http
GET /api/equipment/?search=X-Ray
```

Searches across: name, serial_number, description

### Ordering
```http
GET /api/equipment/?ordering=-created_at
```

Prefix with `-` for descending order.

---

## CORS Configuration

CORS is enabled for all origins in development.

**Production:** Configure `CORS_ALLOWED_ORIGINS` in `.env`

```bash
CORS_ALLOWED_ORIGINS=https://app.cleantrack.com,https://mobile.cleantrack.com
```

---

## API Versioning

Currently using **v1** (no explicit version in URL).

Future versions will use: `/api/v2/`

---

## Support

**Questions or issues?**
- Email: natyssis23@gmail.com
- Documentation: https://cleantrack.com/docs
- GitHub Issues: https://github.com/yourusername/cleantrack/issues

---

*Last Updated: January 2025 | CleanTrack API v1.0.0*
