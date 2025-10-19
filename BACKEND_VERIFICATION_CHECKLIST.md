# BACKEND VERIFICATION CHECKLIST

## ✅ AUTHENTICATION ENDPOINTS - VERIFIED

### ✅ POST /api/auth/login/
- **Status:** WORKING ✅
- **Location:** `accounts/views.py` - `login` function
- **Response:** Returns token + user data with `is_activated` field
- **Frontend Ready:** YES

### ✅ POST /api/auth/register/
- **Status:** WORKING ✅
- **Location:** `accounts/views.py` - `register` function
- **Response:** Returns user data and success message
- **Frontend Ready:** YES

### ✅ GET /api/auth/user/
- **Status:** WORKING ✅
- **Location:** `pamojabackend/urls.py` - `user_status` view
- **Response:** Returns user data with activation status
- **Frontend Ready:** YES

### ✅ PUT /api/auth/user/
- **Status:** WORKING ✅
- **Location:** `accounts/views.py` - `user_profile` function
- **Response:** Updates and returns user profile
- **Frontend Ready:** YES

### ✅ POST /api/auth/change-password/
- **Status:** WORKING ✅
- **Location:** `accounts/views.py` - `change_password` function
- **Response:** Password change confirmation
- **Frontend Ready:** YES

## ✅ PAYMENT ENDPOINTS - VERIFIED

### ✅ POST /api/payments/activation_fee/
- **Status:** WORKING ✅
- **Location:** `payments/views.py` - `activation_fee` action
- **File Upload:** YES - MultiPartParser enabled
- **Validation:** Checks amount and payment_proof
- **Response:** Success message
- **Frontend Ready:** YES

### ✅ GET /api/payments/
- **Status:** WORKING ✅
- **Location:** `payments/views.py` - PaymentViewSet list method
- **Response:** User's payment history
- **Frontend Ready:** YES

### ⚠️ POST /api/payments/ - NEEDS VERIFICATION
- **Status:** NEEDS CHECK
- **Expected:** General payment submission endpoint
- **Action Required:** Verify if create method handles all payment types

## ✅ DASHBOARD ENDPOINTS - VERIFIED

### ✅ GET /api/auth/dashboard-stats/
- **Status:** WORKING ✅
- **Location:** `accounts/views.py` - `dashboard_stats` function
- **Response:** Complete user statistics
- **Frontend Ready:** YES

## ⚠️ SHARES ENDPOINTS - NEEDS VERIFICATION

### ⚠️ GET /api/shares/
- **Status:** NEEDS CHECK
- **Expected Location:** `shares/views.py`
- **Action Required:** Verify ShareViewSet exists and works

### ⚠️ POST /api/shares/
- **Status:** NEEDS CHECK
- **Expected:** Share purchase with file upload
- **Action Required:** Verify create method with quantity calculation

## ⚠️ CLAIMS ENDPOINTS - NEEDS VERIFICATION

### ⚠️ GET /api/claims/
- **Status:** NEEDS CHECK
- **Expected Location:** `claims/views.py`
- **Action Required:** Verify ClaimViewSet exists

### ⚠️ POST /api/claims/
- **Status:** NEEDS CHECK
- **Expected:** Claim submission with file upload
- **Action Required:** Verify create method works

## ⚠️ DOCUMENTS ENDPOINTS - NEEDS VERIFICATION

### ⚠️ GET /api/documents/
- **Status:** NEEDS CHECK
- **Expected Location:** `documents/views.py`
- **Action Required:** Verify DocumentViewSet exists

### ⚠️ POST /api/documents/
- **Status:** NEEDS CHECK
- **Expected:** Document upload
- **Action Required:** Verify create method works

## ⚠️ APPLICATIONS ENDPOINTS - NEEDS VERIFICATION

### ⚠️ GET /api/applications/
- **Status:** NEEDS CHECK
- **Expected Location:** `applications/views.py`
- **Action Required:** Verify ApplicationViewSet exists

### ⚠️ POST /api/applications/
- **Status:** NEEDS CHECK
- **Expected:** Membership application with file upload
- **Action Required:** Verify create method works

## ⚠️ MEETINGS ENDPOINTS - NEEDS VERIFICATION

### ⚠️ GET /api/meetings/
- **Status:** NEEDS CHECK
- **Expected Location:** `meetings/views.py`
- **Action Required:** Verify MeetingViewSet exists

### ⚠️ POST /api/meetings/{id}/register/
- **Status:** NEEDS CHECK
- **Expected:** Meeting registration
- **Action Required:** Verify register action exists

## ⚠️ OTHER ENDPOINTS - NEEDS VERIFICATION

### ⚠️ GET /api/announcements/
- **Status:** NEEDS CHECK
- **Expected Location:** `announcements/views.py`

### ⚠️ GET /api/beneficiaries/
- **Status:** NEEDS CHECK
- **Expected Location:** `beneficiaries/views.py`

### ⚠️ POST /api/contact/
- **Status:** NEEDS CHECK
- **Expected Location:** `contact/views.py`

## 🔧 CRITICAL MISSING ITEMS TO CHECK

### 1. User Model Fields
```python
# Required fields in User model:
class User(AbstractUser):
    is_activated = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    shares_owned = models.IntegerField(default=0)
    available_shares = models.IntegerField(default=0)
    is_member = models.BooleanField(default=False)
```

### 2. Payment Model Fields
```python
# Required fields in Payment model:
class Payment(models.Model):
    payment_type = models.CharField(max_length=50)
    payment_proof = models.FileField(upload_to='payment_proofs/')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
```

### 3. CORS Settings
```python
# Required in settings.py:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True
```

### 4. File Upload Settings
```python
# Required in settings.py:
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## 🎯 IMMEDIATE ACTION REQUIRED

### HIGH PRIORITY (Frontend Blockers):
1. ✅ **Login/Auth** - WORKING
2. ✅ **Activation Fee** - WORKING
3. ⚠️ **Shares Purchase** - NEEDS VERIFICATION
4. ⚠️ **Claims Submission** - NEEDS VERIFICATION
5. ⚠️ **Applications** - NEEDS VERIFICATION

### MEDIUM PRIORITY:
6. ⚠️ **Documents Upload** - NEEDS VERIFICATION
7. ⚠️ **Meetings** - NEEDS VERIFICATION
8. ⚠️ **Beneficiaries** - NEEDS VERIFICATION

### LOW PRIORITY:
9. ⚠️ **Announcements** - NEEDS VERIFICATION
10. ⚠️ **Contact** - NEEDS VERIFICATION

## 🚨 NEXT STEPS

1. **Verify Shares ViewSet** - Check if shares/views.py has proper endpoints
2. **Verify Claims ViewSet** - Check if claims/views.py has proper endpoints
3. **Verify Applications ViewSet** - Check if applications/views.py has proper endpoints
4. **Test File Uploads** - Ensure MultiPartParser works on all endpoints
5. **Check Model Fields** - Verify all required fields exist in models
6. **Test API Responses** - Ensure responses match frontend expectations

## ✅ CONFIRMED WORKING ENDPOINTS

1. `POST /api/auth/login/` ✅
2. `POST /api/auth/register/` ✅
3. `GET /api/auth/user/` ✅
4. `PUT /api/auth/user/` ✅
5. `POST /api/auth/change-password/` ✅
6. `POST /api/payments/activation_fee/` ✅
7. `GET /api/payments/` ✅
8. `GET /api/auth/dashboard-stats/` ✅

**Status: 8/20+ endpoints verified and working**