from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .views import ShareTransactionViewSet, ShareViewSet, buy_shares
from .serializers import SharePurchaseSerializer



router = DefaultRouter()
router.register(r'transactions', ShareTransactionViewSet, basename='share-transaction')
router.register(r'', ShareViewSet, basename='share')

urlpatterns = [
    path('buy/', buy_shares, name='buy-shares'),
    path('', include(router.urls)),
]