from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShareTransactionViewSet, ShareViewSet

router = DefaultRouter()
router.register(r'transactions', ShareTransactionViewSet, basename='share-transaction')
router.register(r'', ShareViewSet, basename='share')

urlpatterns = [
    path('', include(router.urls)),
]