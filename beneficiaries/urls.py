from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BeneficiaryViewSet, change_request

router = DefaultRouter()
router.register(r'', BeneficiaryViewSet, basename='beneficiary')

urlpatterns = [
    path('change-request/', change_request, name='beneficiary-change-request'),
    path('', include(router.urls)),
]