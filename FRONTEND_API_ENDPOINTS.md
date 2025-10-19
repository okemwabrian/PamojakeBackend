# COMPLETE FRONTEND API ENDPOINTS LIST

## 🔐 AUTHENTICATION ENDPOINTS

### User Registration & Login
```
POST /api/auth/register/
Body: {username, email, password, first_name, last_name}

POST /api/auth/login/
Body: {username, password}
Response: {token, user: {id, username, email, is_activated, ...}}

GET /api/auth/user/
Headers: Authorization: Bearer <token>
Response: {id, username, email, is_activated}

GET /api/auth/user-status/
Headers: Authorization: Bearer <token>
Response: {id, username, email, is_activated}

PUT /api/auth/user/
Headers: Authorization: Bearer <token>
Body: {first_name, last_name, phone, address, city, state}

POST /api/auth/change-password/
Headers: Authorization: Bearer <token>
Body: {old_password, new_password}
```

## 💰 PAYMENT ENDPOINTS

### Activation Fee & Payments
```
POST /api/payments/activation_fee/
Headers: Authorization: Bearer <token>
Content-Type: multipart/form-data
Body: {amount, payment_proof (file)}
Response: {message: "Payment submitted successfully"}

GET /api/payments/
Headers: Authorization: Bearer <token>
Response: [list of user payments]

POST /api/payments/
Headers: Authorization: Bearer <token>
Content-Type: multipart/form-data
Body: {payment_type, amount, description, payment_proof (file), payment_method}
```

## 📋 APPLICATION ENDPOINTS

### Membership Applications
```
GET /api/applications/
Headers: Authorization: Bearer <token>
Response: [list of user applications]

POST /api/applications/
Headers: Authorization: Bearer <token>
Content-Type: multipart/form-data
Body: {
  type: "single" or "double",
  first_name, last_name, email, phone_main,
  address_1, city, state_province, zip_postal,
  spouse, spouse_phone, authorized_rep,
  child_1, child_2, child_3, child_4, child_5,
  parent_1, parent_2, spouse_parent_1, spouse_parent_2,
  sibling_1, sibling_2, sibling_3,
  declaration_accepted: true,
  constitution_agreed: true,
  id_document (file)
}

GET /api/applications/{id}/
Headers: Authorization: Bearer <token>
Response: {application details}
```

## 📈 SHARES ENDPOINTS

### Share Purchases
```
GET /api/shares/
Headers: Authorization: Bearer <token>
Response: [list of user share purchases]

POST /api/shares/
Headers: Authorization: Bearer <token>
Content-Type: multipart/form-data
Body: {
  quantity: number,
  payment_method: "paypal|mpesa|bank",
  payment_proof (file)
}
Response: {id, quantity, total_amount, status, created_at}
```

## 🏥 CLAIMS ENDPOINTS

### Benefit Claims
```
GET /api/claims/
Headers: Authorization: Bearer <token>
Response: [list of user claims]

POST /api/claims/
Headers: Authorization: Bearer <token>
Content-Type: multipart/form-data
Body: {
  claim_type: "medical|death|disability|other",
  amount: number,
  description: "text",
  supporting_documents (file)
}
Response: {id, claim_type, amount, status, created_at}
```

## 📄 DOCUMENT ENDPOINTS

### Document Management
```
GET /api/documents/
Headers: Authorization: Bearer <token>
Response: [list of user documents]

POST /api/documents/
Headers: Authorization: Bearer <token>
Content-Type: multipart/form-data
Body: {
  name: "document name",
  document_type: "id|passport|certificate|other",
  file (file upload)
}
Response: {id, name, document_type, status, created_at}
```

## 🤝 MEETING ENDPOINTS

### Meeting Registration
```
GET /api/meetings/
Response: [list of all meetings - public access]

POST /api/meetings/{id}/register/
Headers: Authorization: Bearer <token>
Response: {message: "Successfully registered for meeting"}

GET /api/meetings/{id}/
Response: {meeting details, is_expired, registration_count}
```

## 📢 ANNOUNCEMENT ENDPOINTS

### Public Announcements
```
GET /api/announcements/
Response: [list of announcements - public access]

GET /api/announcements/{id}/
Response: {announcement details}
```

## 👥 BENEFICIARY ENDPOINTS

### Beneficiary Management
```
GET /api/beneficiaries/
Headers: Authorization: Bearer <token>
Response: [list of user beneficiaries]

POST /api/beneficiaries/
Headers: Authorization: Bearer <token>
Body: {
  name: "beneficiary name",
  relationship: "spouse|child|parent|sibling|other",
  phone: "phone number",
  email: "email address"
}

PUT /api/beneficiaries/{id}/
Headers: Authorization: Bearer <token>
Body: {name, relationship, phone, email}

DELETE /api/beneficiaries/{id}/
Headers: Authorization: Bearer <token>
```

## 📞 CONTACT ENDPOINTS

### Contact Messages
```
POST /api/contact/
Body: {
  name: "sender name",
  email: "sender email", 
  phone: "phone number",
  subject: "message subject",
  message: "message content"
}
Response: {message: "Message sent successfully"}
```

## 📊 DASHBOARD ENDPOINTS

### User Statistics
```
GET /api/auth/dashboard/dashboard_stats/
Headers: Authorization: Bearer <token>
Response: {
  total_applications: number,
  total_payments: number,
  total_shares: number,
  total_claims: number,
  total_documents: number,
  pending_claims: number,
  pending_shares: number,
  pending_payments: number,
  activation_status: boolean,
  membership_status: boolean
}
```

## 🔧 REQUIRED HEADERS

### For All Authenticated Requests:
```
Authorization: Bearer <jwt_token>
```

### For File Uploads:
```
Content-Type: multipart/form-data
Authorization: Bearer <jwt_token>
```

### For JSON Requests:
```
Content-Type: application/json
Authorization: Bearer <jwt_token>
```

## 📱 FRONTEND USAGE EXAMPLES

### Login Flow
```javascript
// 1. Login
const loginResponse = await fetch('/api/auth/login/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({username, password})
});
const {token, user} = await loginResponse.json();

// 2. Check activation status
const userResponse = await fetch('/api/auth/user/', {
  headers: {'Authorization': `Bearer ${token}`}
});
const userData = await userResponse.json();

// 3. If not activated, show activation fee form
if (!userData.is_activated) {
  // Show activation fee payment form
}
```

### File Upload Example
```javascript
const formData = new FormData();
formData.append('amount', '50');
formData.append('payment_proof', fileInput.files[0]);

const response = await fetch('/api/payments/activation_fee/', {
  method: 'POST',
  headers: {'Authorization': `Bearer ${token}`},
  body: formData
});
```

## 🎯 KEY ENDPOINTS FOR YOUR FRONTEND

1. **POST /api/auth/login/** - User login
2. **GET /api/auth/user/** - Check user activation status  
3. **POST /api/payments/activation_fee/** - Submit activation fee
4. **POST /api/applications/** - Submit membership application
5. **POST /api/shares/** - Purchase shares
6. **POST /api/claims/** - Submit benefit claims
7. **POST /api/documents/** - Upload documents
8. **GET /api/auth/dashboard/dashboard_stats/** - Dashboard statistics

All endpoints support proper error handling and return appropriate HTTP status codes (200, 201, 400, 401, 403, 404, 500).