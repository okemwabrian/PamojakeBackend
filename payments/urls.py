from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import views
from .models import Payment
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

@csrf_exempt
def get_user_payments(request):
    """Get user payments in simple format for frontend"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    payments_data = [{
        'id': payment.id,
        'payment_type': payment.payment_type,
        'amount': str(payment.amount),
        'payment_method': payment.payment_method,
        'status': payment.status,
        'description': payment.description,
        'admin_notes': payment.admin_notes,
        'created_at': payment.created_at.isoformat(),
        'updated_at': payment.updated_at.isoformat(),
    } for payment in payments]
    
    return JsonResponse({'payments': payments_data})

@csrf_exempt
def print_payment_receipt(request, payment_id):
    """Generate payment receipt"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        payment = Payment.objects.get(id=payment_id, user=request.user)
        
        if payment.status != 'approved':
            return JsonResponse({'error': 'Receipt only available for approved payments'}, status=400)
        
        # Simple receipt data (frontend can format as needed)
        receipt_data = {
            'receipt_id': payment.id,
            'date': payment.created_at.strftime('%B %d, %Y'),
            'member_name': request.user.get_full_name() or request.user.username,
            'payment_type': payment.payment_type,
            'amount': str(payment.amount),
            'payment_method': payment.payment_method,
            'status': payment.status.upper(),
            'description': payment.description,
        }
        
        return JsonResponse({
            'success': True,
            'receipt': receipt_data
        })
        
    except Payment.DoesNotExist:
        return JsonResponse({'error': 'Payment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

router = DefaultRouter()
router.register(r'', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('activation/submit/', submit_activation_fee, name='submit-activation-fee'),
    path('list/', get_user_payments, name='get-user-payments'),  # Simple GET endpoint
    path('<int:payment_id>/receipt/', print_payment_receipt, name='payment-receipt'),
    path('', include(router.urls)),
]