from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.utils import timezone
from .new_application_models import SingleApplication, DoubleApplication, NewSharePurchase, ActivationFeePayment
from .new_application_serializers import (
    SingleApplicationSerializer, DoubleApplicationSerializer, 
    NewSharePurchaseSerializer, ActivationFeePaymentSerializer
)

class SingleApplicationViewSet(viewsets.ModelViewSet):
    queryset = SingleApplication.objects.all()
    serializer_class = SingleApplicationSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class DoubleApplicationViewSet(viewsets.ModelViewSet):
    queryset = DoubleApplication.objects.all()
    serializer_class = DoubleApplicationSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class NewSharePurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = NewSharePurchaseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return NewSharePurchase.objects.all()
        return NewSharePurchase.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        share_purchase = self.get_object()
        shares_assigned = request.data.get('shares_assigned', share_purchase.shares_requested)
        admin_notes = request.data.get('admin_notes', '')
        
        share_purchase.status = 'approved'
        share_purchase.shares_assigned = shares_assigned
        share_purchase.admin_notes = admin_notes
        share_purchase.reviewed_by = request.user
        share_purchase.reviewed_at = timezone.now()
        share_purchase.save()
        
        return Response({'message': 'Share purchase approved successfully'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        share_purchase = self.get_object()
        admin_notes = request.data.get('admin_notes', '')
        
        share_purchase.status = 'rejected'
        share_purchase.admin_notes = admin_notes
        share_purchase.reviewed_by = request.user
        share_purchase.reviewed_at = timezone.now()
        share_purchase.save()
        
        return Response({'message': 'Share purchase rejected'})

class ActivationFeePaymentViewSet(viewsets.ModelViewSet):
    serializer_class = ActivationFeePaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return ActivationFeePayment.objects.all()
        return ActivationFeePayment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        activation_payment = self.get_object()
        admin_notes = request.data.get('admin_notes', '')
        
        activation_payment.status = 'approved'
        activation_payment.admin_notes = admin_notes
        activation_payment.reviewed_by = request.user
        activation_payment.reviewed_at = timezone.now()
        activation_payment.save()
        
        return Response({'message': 'Activation fee approved and membership activated'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        activation_payment = self.get_object()
        admin_notes = request.data.get('admin_notes', '')
        
        activation_payment.status = 'rejected'
        activation_payment.admin_notes = admin_notes
        activation_payment.reviewed_by = request.user
        activation_payment.reviewed_at = timezone.now()
        activation_payment.save()
        
        return Response({'message': 'Activation fee payment rejected'})

# API Views for specific endpoints
@api_view(['POST'])
@permission_classes([AllowAny])
def submit_single_application(request):
    serializer = SingleApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Single family application submitted successfully!',
            'application_id': serializer.data['id']
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_double_application(request):
    serializer = DoubleApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Double family application submitted successfully!',
            'application_id': serializer.data['id']
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_activation_fee(request):
    serializer = ActivationFeePaymentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({
            'message': 'Activation fee payment submitted successfully!',
            'payment_id': serializer.data['id']
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_shares(request):
    serializer = NewSharePurchaseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({
            'message': 'Share purchase request submitted successfully!',
            'purchase_id': serializer.data['id']
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)