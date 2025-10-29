from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer
import logging

logger = logging.getLogger(__name__)

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all().order_by('-created_at')
        return Payment.objects.filter(user=self.request.user).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        """Override list to return consistent format with custom endpoint"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'payments': serializer.data})
    
    def create(self, request, *args, **kwargs):
        # Debug logging
        logger.info(f"Request data keys: {list(request.data.keys())}")
        logger.info(f"Request files: {list(request.FILES.keys())}")
        
        try:
            # Validate required fields
            required_fields = ['payment_type', 'amount', 'payment_method']
            missing_fields = [field for field in required_fields if not request.data.get(field)]
            
            if missing_fields:
                return Response(
                    {"error": f"Missing required fields: {', '.join(missing_fields)}"}, 
                    status=400
                )
            
            # Check for required file
            if 'payment_proof' not in request.FILES:
                return Response(
                    {"payment_proof": ["Payment proof file is required"]}, 
                    status=400
                )
            
            serializer = PaymentCreateSerializer(data=request.data)
            if serializer.is_valid():
                payment = serializer.save(user=request.user)
                return Response(PaymentSerializer(payment).data, status=201)
            else:
                logger.error(f"Payment validation errors: {serializer.errors}")
                return Response(serializer.errors, status=400)
        except Exception as e:
            logger.error(f"Payment creation error: {str(e)}")
            return Response({'error': str(e)}, status=400)

    @action(detail=False, methods=['post'])
    def activation_fee(self, request):
        amount = request.data.get('amount')
        payment_proof = request.FILES.get('payment_proof')
        
        if not amount or not payment_proof:
            return Response({'message': 'Amount and payment proof required'}, status=400)
        
        try:
            payment = Payment.objects.create(
                user=request.user,
                payment_type='activation_fee',
                amount=float(amount),
                description='Account Activation Fee',
                payment_proof=payment_proof,
                status='pending'
            )
            return Response(PaymentSerializer(payment).data, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        payment = self.get_object()
        payment.status = 'approved'
        payment.admin_notes = request.data.get('notes', '')
        
        # Update shares if share purchase
        if payment.payment_type == 'share_purchase':
            shares_to_add = int(payment.amount // 25)
            payment.user.shares += shares_to_add
            if payment.user.shares >= 20:
                payment.user.is_active_member = True
            payment.user.save()
        
        payment.save()
        return Response({'status': 'approved'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        payment = self.get_object()
        payment.status = 'rejected'
        payment.admin_notes = request.data.get('notes', '')
        payment.save()
        return Response({'status': 'rejected'})
    
    @action(detail=False, methods=['get'])
    def admin_list(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        payments = Payment.objects.all().order_by('-created_at')
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)