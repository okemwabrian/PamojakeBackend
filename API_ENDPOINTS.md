# Pamoja Kenya MN - Complete API Endpoints

## Base URL: `http://localhost:8000/api`

## Authentication Endpoints
- `POST /auth/login/` - Login user
- `POST /auth/register/` - Register new user
- `POST /auth/logout/` - Logout user
- `GET /auth/user/` - Get current user profile
- `PUT /auth/user/` - Update user profile

## Applications Endpoints
- `GET /applications/` - List user applications (admin: all applications)
- `POST /applications/` - Create new application
- `GET /applications/{id}/` - Get application details
- `PUT /applications/{id}/` - Update application
- `DELETE /applications/{id}/` - Delete application
- `POST /applications/{id}/approve/` - Approve application (admin only)
- `POST /applications/{id}/reject/` - Reject application (admin only)

## Payments Endpoints
- `GET /payments/` - List user payments (admin: all payments)
- `POST /payments/` - Create new payment
- `GET /payments/{id}/` - Get payment details
- `PUT /payments/{id}/` - Update payment

## Shares Endpoints
- `GET /shares/` - List user shares (admin: all shares)
- `POST /shares/` - Buy shares
- `GET /shares/{id}/` - Get share details

## Claims Endpoints
- `GET /claims/` - List user claims (admin: all claims)
- `POST /claims/` - Submit new claim
- `GET /claims/{id}/` - Get claim details
- `PUT /claims/{id}/` - Update claim
- `POST /claims/{id}/approve/` - Approve claim (admin only)
- `POST /claims/{id}/reject/` - Reject claim (admin only)

## Documents Endpoints
- `GET /documents/` - List user documents (admin: all documents)
- `POST /documents/` - Upload document
- `GET /documents/{id}/` - Get document details
- `DELETE /documents/{id}/` - Delete document
- `POST /documents/{id}/approve/` - Approve document (admin only)
- `POST /documents/{id}/reject/` - Reject document (admin only)

## Announcements Endpoints
- `GET /announcements/` - List active announcements
- `POST /announcements/` - Create announcement (admin only)
- `GET /announcements/{id}/` - Get announcement details
- `PUT /announcements/{id}/` - Update announcement (admin only)
- `DELETE /announcements/{id}/` - Delete announcement (admin only)

## Meetings Endpoints
- `GET /meetings/` - List active meetings
- `POST /meetings/` - Create meeting (admin only)
- `GET /meetings/{id}/` - Get meeting details
- `PUT /meetings/{id}/` - Update meeting (admin only)
- `DELETE /meetings/{id}/` - Delete meeting (admin only)

## Contact Endpoints
- `GET /contact/` - List messages (admin only)
- `POST /contact/` - Send contact message
- `GET /contact/{id}/` - Get message details (admin only)
- `POST /contact/{id}/mark_read/` - Mark message as read (admin only)
- `POST /contact/{id}/reply/` - Reply to message (admin only)

## Admin Panel Endpoints

### User Management
- `GET /admin/users/` - List all users
- `GET /admin/users/stats/` - Get user statistics
- `POST /admin/users/{id}/toggle_membership/` - Toggle user membership
- `POST /admin/users/{id}/reset_password/` - Reset user password
- `POST /admin/users/{id}/activate_user/` - Activate user account
- `POST /admin/users/{id}/deactivate_user/` - Deactivate user account
- `POST /admin/users/{id}/update_shares/` - Update user shares

### Application Management
- `GET /admin/applications/` - List all applications
- `POST /admin/applications/{id}/approve/` - Approve application
- `POST /admin/applications/{id}/reject/` - Reject application

### Claim Management
- `GET /admin/claims/` - List all claims
- `POST /admin/claims/{id}/approve/` - Approve claim
- `POST /admin/claims/{id}/reject/` - Reject claim

### Payment Management
- `GET /admin/payments/` - List all payments
- `POST /admin/payments/{id}/mark_completed/` - Mark payment as completed

### Contact Management
- `GET /admin/contact/` - List all contact messages
- `POST /admin/contact/{id}/mark_read/` - Mark message as read
- `POST /admin/contact/{id}/reply/` - Reply to contact message

## Authentication
All endpoints except `/auth/login/`, `/auth/register/`, and `POST /contact/` require authentication.

Use Token authentication:
```
Authorization: Token <your-token-here>
```

## Response Format
All responses are in JSON format:

### Success Response
```json
{
  "data": {...},
  "status": "success"
}
```

### Error Response
```json
{
  "error": "Error message",
  "status": "error"
}
```

## File Upload
For document uploads, use `multipart/form-data` content type.

## Pagination
List endpoints support pagination with `page` parameter:
- `GET /applications/?page=2`

Default page size: 20 items per page.