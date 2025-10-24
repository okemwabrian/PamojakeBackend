from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import views
from .serializers import PaymentCreateSerializer, PaymentSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_activation_fee(request):
    data = request.data.copy()
    data['payment_type'] = 'activation_fee'
    data['description'] = 'Account Activation Fee'
    
    serializer = PaymentCreateSerializer(data=data)
    if serializer.is_valid():
        payment = serializer.save(user=request.user)
        return Response({
            'message': 'Activation fee payment submitted successfully!',
            'payment_id': payment.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

router = DefaultRouter()
router.register(r'', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('activation/submit/', submit_activation_fee, name='submit-activation-fee'),
    path('', include(router.urls)),
]