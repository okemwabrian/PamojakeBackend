from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminUserViewSet,
    AdminApplicationViewSet,
    AdminClaimViewSet,
    AdminPaymentViewSet,
    AdminContactViewSet
)

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
]