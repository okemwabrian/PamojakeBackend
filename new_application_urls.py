from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import new_application_views as views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'single-applications', views.SingleApplicationViewSet)
router.register(r'double-applications', views.DoubleApplicationViewSet)
router.register(r'new-shares', views.NewSharePurchaseViewSet, basename='new-shares')
router.register(r'activation-payments', views.ActivationFeePaymentViewSet, basename='activation-payments')

urlpatterns = [
    # API Router URLs
    path('api/v2/', include(router.urls)),
    
    # Custom API endpoints
    path('api/v2/applications/single/submit/', views.submit_single_application, name='submit-single-application'),
    path('api/v2/applications/double/submit/', views.submit_double_application, name='submit-double-application'),
    path('api/v2/payments/activation/submit/', views.submit_activation_fee, name='submit-activation-fee'),
    path('api/v2/shares/buy/', views.buy_shares, name='buy-shares'),
]