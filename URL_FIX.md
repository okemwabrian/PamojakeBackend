# URL Fix for Activation Fee

## ❌ Issue
Frontend was calling: `POST /api/payments/activation-fee/` (with hyphen)
Backend expects: `POST /api/payments/activation_fee/` (with underscore)

## ✅ Solution
Updated React API service to use correct URL with underscore.

## 🔧 Frontend Update Required
In your React project, update the API call to use:
```javascript
// Correct URL (with underscore)
paymentsAPI.submitActivationFee(data)
// This calls: POST /api/payments/activation_fee/

// Or use the general payments endpoint:
paymentsAPI.createPayment({
  type: 'activation_fee',
  amount: 100,
  ...otherData
})
```

## 📋 Available Payment Endpoints
- `GET /api/payments/` - List payments
- `POST /api/payments/` - Create payment
- `POST /api/payments/activation_fee/` - Submit activation fee (specific)
- `POST /api/payments/{id}/approve/` - Approve payment
- `POST /api/payments/{id}/reject/` - Reject payment

The activation fee endpoint should now work correctly!