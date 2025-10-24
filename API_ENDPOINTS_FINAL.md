# Pamoja Backend API Endpoints

## Base URLs
- **Local Development**: `http://localhost:8000`
- **Production**: `https://okemwabrianny.pythonanywhere.com`
- **Frontend**: `https://pamojake.netlify.app`

## Authentication Endpoints

### POST `/api/auth/register/`
Register a new user
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string"
}
```

### POST `/api/auth/login/`
User login
```json
{
  "username": "string",
  "password": "string"
}
```

### GET `/api/auth/test/`
Test API connectivity (no auth required)

## Application Endpoints

### POST `/api/applications/single/submit/`
Submit single family application (no auth required)
```json
{
  "firstName": "string",
  "lastName": "string",
  "email": "string",
  "phoneMain": "string",
  "address1": "string",
  "city": "string",
  "stateProvince": "string",
  "zip": "string",
  "id_document": "file",
  "declarationAccepted": true
}
```

### POST `/api/applications/double/submit/`
Submit double family application (no auth required)
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "confirm_email": "string",
  "phone": "string",
  "address_1": "string",
  "city": "string",
  "state_province": "string",
  "zip_postal": "string",
  "id_document": "file",
  "constitution_agreed": true
}
```

## Payment Endpoints

### POST `/api/payments/activation/submit/`
Submit activation fee payment (requires auth)
```json
{
  "amount": "50.00",
  "payment_method": "paypal|venmo|zelle|mpesa|bank|other",
  "transaction_id": "string",
  "description": "string",
  "payment_proof": "file"
}
```

### GET `/api/payments/`
List user's payments (requires auth)

## Share Purchase Endpoints

### POST `/api/shares/buy/`
Purchase shares (requires auth)
```json
{
  "quantity": 10,
  "amount": "100.00",
  "payment_method": "paypal|venmo|zelle|mpesa|bank|other",
  "transaction_id": "string",
  "notes": "string"
}
```

### GET `/api/shares/`
List user's share purchases (requires auth)

## User Endpoints

### GET `/api/auth/user/`
Get current user profile (requires auth)

### PUT `/api/auth/user/`
Update user profile (requires auth)

### GET `/api/auth/dashboard-stats/`
Get user dashboard statistics (requires auth)

## Admin Endpoints (Staff Only)

### GET `/api/applications/`
List all applications

### GET `/api/payments/`
List all payments

### GET `/api/shares/`
List all share purchases

### POST `/api/shares/{id}/approve/`
Approve share purchase

### POST `/api/shares/{id}/reject/`
Reject share purchase

### POST `/api/payments/{id}/approve/`
Approve payment

### POST `/api/payments/{id}/reject/`
Reject payment

## File Upload Notes

- All file uploads should use `multipart/form-data`
- Supported file types: PDF, JPG, PNG, DOC, DOCX
- Maximum file size: 10MB
- Files are stored in `/media/` directory

## Error Responses

All endpoints return standard HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

Error response format:
```json
{
  "error": "Error message",
  "details": {
    "field": ["Field-specific error"]
  }
}
```

## CORS Configuration

The backend is configured to accept requests from:
- `https://pamojake.netlify.app` (production frontend)
- `http://localhost:3000` (development frontend)

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:
1. Login to get a token
2. Include token in Authorization header: `Bearer <token>`
3. Tokens expire after 24 hours