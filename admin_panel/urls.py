from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminUserViewSet,
    AdminApplicationViewSet,
    AdminClaimViewSet,
    AdminPaymentViewSet,
    AdminContactViewSet
)
from .crud_views import (
    admin_applications, admin_application_detail,
    admin_payments, admin_payment_detail,
    admin_claims, admin_claim_detail,
    admin_shares, admin_share_detail,
    admin_user_activities, admin_user_activity_detail,
    admin_dashboard_stats
)
from .members_views import get_registered_members, get_member_details

from shares.views import ShareTransactionViewSet
from documents.views import DocumentViewSet
from meetings.views import MeetingViewSet

router = DefaultRouter()
router.register(r'users', AdminUserViewSet, basename='admin-users')
router.register(r'applications', AdminApplicationViewSet, basename='admin-applications')
router.register(r'claims', AdminClaimViewSet, basename='admin-claims')
router.register(r'payments', AdminPaymentViewSet, basename='admin-payments')
router.register(r'contact', AdminContactViewSet, basename='admin-contact')
router.register(r'shares', ShareTransactionViewSet, basename='admin-shares')
router.register(r'documents', DocumentViewSet, basename='admin-documents')
router.register(r'meetings', MeetingViewSet, basename='admin-meetings')

urlpatterns = [
    path('', include(router.urls)),
    
    # CRUD Endpoints
    path('crud/applications/', admin_applications, name='admin_crud_applications'),
    path('crud/applications/<int:app_id>/', admin_application_detail, name='admin_crud_application_detail'),
    
    path('crud/payments/', admin_payments, name='admin_crud_payments'),
    path('crud/payments/<int:payment_id>/', admin_payment_detail, name='admin_crud_payment_detail'),
    
    path('crud/claims/', admin_claims, name='admin_crud_claims'),
    path('crud/claims/<int:claim_id>/', admin_claim_detail, name='admin_crud_claim_detail'),
    
    path('crud/shares/', admin_shares, name='admin_crud_shares'),
    path('crud/shares/<int:share_id>/', admin_share_detail, name='admin_crud_share_detail'),
    
    # Activity Tracking
    path('activities/', admin_user_activities, name='admin_user_activities'),
    path('users/<int:user_id>/activities/', admin_user_activity_detail, name='admin_user_activity_detail'),
    
    # Dashboard Stats
    path('dashboard/stats/', admin_dashboard_stats, name='admin_dashboard_stats'),
    
    # Registered Members
    path('members/', get_registered_members, name='get_registered_members'),
    path('members/<int:user_id>/', get_member_details, name='get_member_details'),
]