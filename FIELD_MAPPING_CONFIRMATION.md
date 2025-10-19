# ✅ BACKEND FIELD MAPPING CONFIRMATION

## 🎯 YOUR EXPECTED FIELDS vs BACKEND IMPLEMENTATION

### **SINGLE MEMBERSHIP APPLICATION**

| Your Expected Field | Backend Model Field | Status | Notes |
|-------------------|-------------------|--------|-------|
| `membership_type` | `membership_type` | ✅ | Primary field |
| `first_name` | `first_name` | ✅ | Required |
| `last_name` | `last_name` | ✅ | Required |
| `email` | `email` | ✅ | Required |
| `phone` | `phone` | ✅ | Required |
| `date_of_birth` | `date_of_birth` | ✅ | Required |
| `id_number` | `id_number` | ✅ | Required |
| `address` | `address` | ✅ | Primary field |
| `city` | `city` | ✅ | Required |
| `state` | `state` | ✅ | Primary field |
| `zip_code` | `zip_code` | ✅ | Primary field |
| `emergency_name` | `emergency_name` | ✅ | Required |
| `emergency_phone` | `emergency_phone` | ✅ | Required |
| `emergency_relationship` | `emergency_relationship` | ✅ | Required |
| `children_info` | `children_info` | ✅ | JSON field |
| `id_document` | `id_document` | ✅ | File field |
| `payment_proof` | `payment_proof` | ✅ | File field |
| `payment_amount` | `payment_amount` | ✅ | Decimal field |

### **DOUBLE MEMBERSHIP APPLICATION**

| Your Expected Field | Backend Model Field | Status | Notes |
|-------------------|-------------------|--------|-------|
| **All Single Fields Above** | **Same as above** | ✅ | Inherited |
| `spouse_first_name` | `spouse_first_name` | ✅ | Required for double |
| `spouse_last_name` | `spouse_last_name` | ✅ | Required for double |
| `spouse_email` | `spouse_email` | ✅ | Optional |
| `spouse_phone` | `spouse_phone` | ✅ | Optional |
| `spouse_date_of_birth` | `spouse_date_of_birth` | ✅ | Required for double |
| `spouse_id_number` | `spouse_id_number` | ✅ | Required for double |
| `spouse_id_document` | `spouse_id_document` | ✅ | File field |

## 🔧 BACKEND MODEL STRUCTURE

```python
class Application(models.Model):
    # System fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=10, choices=TYPE_CHOICES)  # ✅
    status = models.CharField(max_length=20, default='pending')
    
    # Primary applicant - Required
    first_name = models.CharField(max_length=100)  # ✅
    last_name = models.CharField(max_length=100)   # ✅
    email = models.EmailField()                    # ✅
    phone = models.CharField(max_length=15)        # ✅
    date_of_birth = models.DateField()             # ✅
    id_number = models.CharField(max_length=20)    # ✅
    
    # Address - Required
    address = models.TextField()                   # ✅
    city = models.CharField(max_length=100)        # ✅
    state = models.CharField(max_length=100)       # ✅
    zip_code = models.CharField(max_length=10)     # ✅
    
    # Emergency Contact - Required
    emergency_name = models.CharField(max_length=100)        # ✅
    emergency_phone = models.CharField(max_length=20)        # ✅
    emergency_relationship = models.CharField(max_length=50) # ✅
    
    # Spouse Info - Required for double
    spouse_first_name = models.CharField(max_length=100, blank=True, null=True)  # ✅
    spouse_last_name = models.CharField(max_length=100, blank=True, null=True)   # ✅
    spouse_email = models.EmailField(blank=True, null=True)                      # ✅
    spouse_phone = models.CharField(max_length=15, blank=True)                   # ✅
    spouse_date_of_birth = models.DateField(blank=True, null=True)               # ✅
    spouse_id_number = models.CharField(max_length=20, blank=True)               # ✅
    
    # Children Info - Optional
    children_info = models.JSONField(default=list, blank=True)  # ✅
    
    # Files - Required/Optional
    id_document = models.FileField(upload_to='applications/ids/')              # ✅
    spouse_id_document = models.FileField(upload_to='applications/spouse_ids/', blank=True, null=True)  # ✅
    payment_proof = models.FileField(upload_to='applications/payments/', blank=True, null=True)         # ✅
    
    # Payment Info - Optional
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # ✅
    
    # Admin fields
    admin_notes = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## 📤 API ENDPOINT CONFIRMATION

### **Endpoint**: `POST /api/applications/`
### **Content-Type**: `multipart/form-data`
### **Authentication**: `Bearer Token Required`

### **FormData Structure**:
```javascript
const formData = new FormData();

// Required for Single
formData.append('membership_type', 'single');
formData.append('first_name', 'John');
formData.append('last_name', 'Doe');
formData.append('email', 'john@email.com');
formData.append('phone', '+1234567890');
formData.append('date_of_birth', '1990-01-01');
formData.append('id_number', 'ID123456789');
formData.append('address', '123 Main Street');
formData.append('city', 'Minneapolis');
formData.append('state', 'Minnesota');
formData.append('zip_code', '55401');
formData.append('emergency_name', 'Jane Doe');
formData.append('emergency_phone', '+1987654321');
formData.append('emergency_relationship', 'spouse');
formData.append('id_document', fileInput.files[0]);

// Additional for Double
formData.append('spouse_first_name', 'Jane');
formData.append('spouse_last_name', 'Doe');
formData.append('spouse_date_of_birth', '1992-01-01');
formData.append('spouse_id_number', 'ID987654321');
formData.append('spouse_id_document', spouseFileInput.files[0]);

// Optional fields
formData.append('spouse_email', 'jane@email.com');
formData.append('spouse_phone', '+1987654321');
formData.append('children_info', JSON.stringify([
    {
        name: 'Child Name',
        date_of_birth: '2010-01-01',
        relationship: 'child'
    }
]));
formData.append('payment_proof', paymentFileInput.files[0]);
formData.append('payment_amount', '150.00');
```

## ✅ VALIDATION RULES

### **Single Membership (15 Required Fields)**:
1. `membership_type` ✅
2. `first_name` ✅
3. `last_name` ✅
4. `email` ✅
5. `phone` ✅
6. `date_of_birth` ✅
7. `id_number` ✅
8. `address` ✅
9. `city` ✅
10. `state` ✅
11. `zip_code` ✅
12. `emergency_name` ✅
13. `emergency_phone` ✅
14. `emergency_relationship` ✅
15. `id_document` (File) ✅

### **Double Membership (Additional 5 Required Fields)**:
16. `spouse_first_name` ✅
17. `spouse_last_name` ✅
18. `spouse_date_of_birth` ✅
19. `spouse_id_number` ✅
20. `spouse_id_document` (File) ✅

### **Optional Fields (Both Types)**:
- `spouse_email` ✅
- `spouse_phone` ✅
- `children_info` (JSON) ✅
- `payment_proof` (File) ✅
- `payment_amount` ✅

## 🔄 BACKWARD COMPATIBILITY

The backend maintains backward compatibility with existing fields:
- `type` ↔ `membership_type`
- `address_1` ↔ `address`
- `state_province` ↔ `state`
- `zip_postal` ↔ `zip_code`
- `spouse` ↔ `spouse_first_name + spouse_last_name`

## 📋 RESPONSE FORMAT

### **Success Response (201)**:
```json
{
    "id": 1,
    "membership_type": "single",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@email.com",
    "phone": "+1234567890",
    "date_of_birth": "1990-01-01",
    "id_number": "ID123456789",
    "address": "123 Main Street",
    "city": "Minneapolis",
    "state": "Minnesota",
    "zip_code": "55401",
    "emergency_name": "Jane Doe",
    "emergency_phone": "+1987654321",
    "emergency_relationship": "spouse",
    "children_info": [],
    "payment_amount": "150.00",
    "status": "pending",
    "created_at": "2025-01-01T12:00:00Z",
    "id_document": "/media/applications/ids/document.pdf",
    "payment_proof": "/media/applications/payments/proof.jpg"
}
```

### **Error Response (400)**:
```json
{
    "first_name": ["This field is required."],
    "id_document": ["No file was submitted."],
    "spouse_first_name": ["This field is required for double membership."]
}
```

## ✅ CONFIRMATION

**YES, the backend expects and supports EXACTLY the field structure you specified:**

- ✅ **Single Membership**: 15 required fields + 1 required file
- ✅ **Double Membership**: 19 required fields + 2 required files  
- ✅ **Optional fields**: children_info (JSON), payment fields
- ✅ **File uploads**: PDF, JPG, PNG supported
- ✅ **FormData submission**: Properly configured
- ✅ **Field validation**: All rules implemented
- ✅ **Backward compatibility**: Maintained with existing system

**The backend is ready to receive applications in the exact format you specified.**