from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .views import ShareTransactionViewSet, ShareViewSet
from .serializers import SharePurchaseSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_shares(request):
    serializer = SharePurchaseSerializer(data=request.data)
    if serializer.is_valid():
        share = serializer.save(user=request.user)
        return Response({
            'message': 'Share purchase request submitted successfully!',
            'purchase_id': share.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

router = DefaultRouter()
router.register(r'transactions', ShareTransactionViewSet, basename='share-transaction')
router.register(r'', ShareViewSet, basename='share')

urlpatterns = [
    path('buy/', buy_shares, name='buy-shares'),
    path('', include(router.urls)),
]