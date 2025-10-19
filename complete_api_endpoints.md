# Complete Django Backend API Endpoints

## ✅ IMPLEMENTED ENDPOINTS

### Authentication
- POST /api/auth/register/
- POST /api/auth/login/
- POST /api/auth/logout/
- GET /api/auth/user/
- PUT /api/auth/user/
- POST /api/auth/change-password/

### Applications
- GET /api/applications/
- POST /api/applications/single/
- POST /api/applications/double/
- GET /api/applications/{id}/
- PUT /api/applications/{id}/
- DELETE /api/applications/{id}/
- POST /api/applications/{id}/approve/
- POST /api/applications/{id}/reject/

### Admin Applications
- GET /api/admin/applications/

### Shares
- GET /api/shares/
- POST /api/shares/
- GET /api/shares/{id}/
- PUT /api/shares/{id}/
- DELETE /api/shares/{id}/
- POST /api/shares/{id}/approve/
- POST /api/shares/{id}/reject/

### Documents
- GET /api/documents/
- POST /api/documents/
- GET /api/documents/{id}/
- PUT /api/documents/{id}/
- DELETE /api/documents/{id}/
- POST /api/documents/{id}/approve/
- POST /api/documents/{id}/reject/

### Meetings
- GET /api/meetings/
- POST /api/meetings/
- GET /api/meetings/{id}/
- PUT /api/meetings/{id}/
- DELETE /api/meetings/{id}/
- POST /api/meetings/{id}/attend/

### Payments
- GET /api/payments/
- POST /api/payments/
- GET /api/payments/{id}/
- PUT /api/payments/{id}/
- POST /api/payments/{id}/approve/
- POST /api/payments/{id}/reject/

### Claims
- GET /api/claims/
- POST /api/claims/
- GET /api/claims/{id}/
- PUT /api/claims/{id}/
- DELETE /api/claims/{id}/
- POST /api/claims/{id}/approve/
- POST /api/claims/{id}/reject/

### Announcements
- GET /api/announcements/
- POST /api/announcements/
- GET /api/announcements/{id}/
- PUT /api/announcements/{id}/
- DELETE /api/announcements/{id}/

### Contact
- GET /api/contact/
- POST /api/contact/
- GET /api/contact/{id}/

### Beneficiaries
- GET /api/beneficiaries/
- POST /api/beneficiaries/
- GET /api/beneficiaries/{id}/
- PUT /api/beneficiaries/{id}/
- DELETE /api/beneficiaries/{id}/

### Admin Users
- GET /api/auth/users/
- GET /api/auth/users/{id}/
- PUT /api/auth/users/{id}/
- DELETE /api/auth/users/{id}/
- POST /api/auth/users/{id}/toggle_active/
- POST /api/auth/users/{id}/toggle_admin/
- POST /api/auth/users/{id}/reset_password/

### Admin Panel
- GET /api/admin/applications/
- GET /api/admin/shares/
- GET /api/admin/documents/
- GET /api/admin/payments/
- GET /api/admin/claims/

## 🔐 PERMISSIONS
- **Public**: announcements (read), meetings (read)
- **Authenticated**: All user endpoints
- **Admin**: All admin endpoints, approve/reject actions
- **File Upload**: documents, applications (multipart/form-data)

## 📊 STATUS
All major CRUD operations implemented with proper permissions and validation!