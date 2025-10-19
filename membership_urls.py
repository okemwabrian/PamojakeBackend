from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import the new comprehensive viewsets
from membership_admin_views import ComprehensiveMembershipAdminViewSet
from membership_user_views import (
    MembershipApplicationViewSet,
    MemberClaimViewSet, 
    MemberPaymentViewSet,
    MemberShareViewSet,
    MemberDocumentViewSet,
    MemberDashboardViewSet
)

# Create routers
admin_router = DefaultRouter()
user_router = DefaultRouter()

# Register admin viewsets
admin_router.register(r'membership', ComprehensiveMembershipAdminViewSet, basename='admin-membership')

# Register user viewsets
user_router.register(r'applications', MembershipApplicationViewSet, basename='member-applications')
user_router.register(r'claims', MemberClaimViewSet, basename='member-claims')
user_router.register(r'payments', MemberPaymentViewSet, basename='member-payments')
user_router.register(r'shares', MemberShareViewSet, basename='member-shares')
user_router.register(r'documents', MemberDocumentViewSet, basename='member-documents')
user_router.register(r'dashboard', MemberDashboardViewSet, basename='member-dashboard')

# URL patterns
urlpatterns = [
    # Admin endpoints
    path('api/admin/', include(admin_router.urls)),
    
    # User endpoints
    path('api/member/', include(user_router.urls)),
]

# ENDPOINT DOCUMENTATION
"""
ADMIN ENDPOINTS:
================

Applications:
- GET /api/admin/membership/applications/ - Get all applications
- POST /api/admin/membership/{id}/approve_application/ - Approve application
- POST /api/admin/membership/{id}/reject_application/ - Reject application
- DELETE /api/admin/membership/{id}/delete_application/ - Delete application

Claims:
- GET /api/admin/membership/claims/ - Get all claims
- POST /api/admin/membership/{id}/approve_claim/ - Approve claim
- POST /api/admin/membership/{id}/reject_claim/ - Reject claim
- DELETE /api/admin/membership/{id}/delete_claim/ - Delete claim

Payments:
- GET /api/admin/membership/payments/ - Get all payments
- POST /api/admin/membership/{id}/approve_payment/ - Approve payment
- POST /api/admin/membership/{id}/reject_payment/ - Reject payment

Shares:
- GET /api/admin/membership/shares/ - Get all share transactions
- POST /api/admin/membership/{id}/approve_share_transaction/ - Approve share transaction

Users:
- GET /api/admin/membership/users/ - Get all users
- POST /api/admin/membership/{id}/activate_user/ - Activate user
- POST /api/admin/membership/{id}/deactivate_user/ - Deactivate user
- POST /api/admin/membership/{id}/update_user_shares/ - Update user shares

Reports:
- GET /api/admin/membership/membership_stats/ - Get membership statistics
- GET /api/admin/membership/financial_report/ - Get financial report

Bulk Operations:
- POST /api/admin/membership/bulk_approve_applications/ - Bulk approve applications
- POST /api/admin/membership/deduct_shares_all_members/ - Deduct shares from all members

USER ENDPOINTS:
===============

Applications:
- GET /api/member/applications/ - Get user's applications
- POST /api/member/applications/ - Submit new application
- GET /api/member/applications/{id}/ - Get specific application
- PUT /api/member/applications/{id}/ - Update application
- DELETE /api/member/applications/{id}/ - Delete application

Claims:
- GET /api/member/claims/ - Get user's claims
- POST /api/member/claims/ - Submit new claim
- GET /api/member/claims/{id}/ - Get specific claim
- PUT /api/member/claims/{id}/ - Update claim
- DELETE /api/member/claims/{id}/ - Delete claim

Payments:
- GET /api/member/payments/ - Get user's payments
- POST /api/member/payments/ - Submit new payment
- POST /api/member/payments/activation_fee/ - Submit activation fee
- GET /api/member/payments/{id}/ - Get specific payment

Shares:
- GET /api/member/shares/ - Get user's share transactions
- POST /api/member/shares/ - Purchase shares
- GET /api/member/shares/my_shares/ - Get current share information
- GET /api/member/shares/{id}/ - Get specific transaction

Documents:
- GET /api/member/documents/ - Get user's documents
- POST /api/member/documents/ - Upload new document
- GET /api/member/documents/{id}/ - Get specific document
- DELETE /api/member/documents/{id}/ - Delete document

Dashboard:
- GET /api/member/dashboard/overview/ - Get dashboard overview
- GET /api/member/dashboard/membership_status/ - Get membership status

USAGE EXAMPLES:
===============

# Submit membership application
POST /api/member/applications/
{
    "membership_type": "single",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "123-456-7890",
    "date_of_birth": "1990-01-01",
    "id_number": "12345678",
    "address": "123 Main St",
    "city": "Minneapolis",
    "state": "MN",
    "zip_code": "55401",
    "emergency_name": "Jane Doe",
    "emergency_phone": "123-456-7891",
    "emergency_relationship": "spouse"
}
+ Files: id_document, payment_proof

# Submit claim
POST /api/member/claims/
{
    "claim_type": "medical",
    "member_name": "John Doe",
    "relationship": "self",
    "incident_date": "2025-01-01",
    "amount_requested": 500.00,
    "description": "Medical emergency"
}
+ Files: supporting_documents

# Purchase shares
POST /api/member/shares/
{
    "quantity": 10,
    "payment_method": "paypal",
    "total_amount": 250.00
}
+ Files: payment_proof

# Admin approve application
POST /api/admin/membership/1/approve_application/
{
    "notes": "Application approved - all documents verified"
}

# Admin financial report
GET /api/admin/membership/financial_report/
Response: {
    "total_revenue": 15000.00,
    "payment_revenue": 10000.00,
    "share_revenue": 5000.00,
    "payment_breakdown": [...],
    "pending_payments": 5
}
"""