from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import ShareTransaction, SharePurchase
from .serializers import ShareTransactionSerializer, SharePurchaseSerializer
from accounts.email_templates import send_payment_notification_to_admin
from notifications.utils import send_payment_approval_notification

class ShareViewSet(viewsets.ModelViewSet):
    serializer_class = SharePurchaseSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return SharePurchase.objects.all().order_by('-created_at')
        return SharePurchase.objects.filter(user=self.request.user).order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            quantity = int(data.get('quantity', 0))
            
            if quantity <= 0:
                return Response({'message': 'Quantity must be greater than 0'}, status=400)
            
            # Calculate amounts (assuming $10 per share)
            amount_per_share = 10
            total_amount = quantity * amount_per_share
            
            data['amount_per_share'] = amount_per_share
            data['total_amount'] = total_amount
            
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                share = serializer.save(
                    user=request.user, 
                    buyer_name=request.user.get_full_name()
                )
                
                # Send notification to admin
                send_mail(
                    subject=f'New Share Purchase - {request.user.username}',
                    message=f'''
                    New share purchase submitted:
                    
                    User: {request.user.get_full_name()}
                    Email: {request.user.email}
                    Quantity: {share.quantity} shares
                    Total Amount: ${share.total_amount}
                    Date: {share.created_at}
                    
                    Please review in admin panel.
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['pamojakeny@gmail.com'],
                    fail_silently=True,
                )
                
                return Response(SharePurchaseSerializer(share).data, status=201)
            return Response({'message': 'Invalid share purchase data'}, status=400)
        except Exception as e:
            return Response({'message': str(e)}, status=400)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        share = self.get_object()
        share.status = 'approved'
        share.admin_notes = request.data.get('notes', '')
        
        # Update user's shares
        user = share.user
        user.shares += share.quantity
        if user.shares >= 20:
            user.is_active_member = True
        user.save()
        
        share.save()
        return Response({'status': 'approved'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        share = self.get_object()
        share.status = 'rejected'
        share.admin_notes = request.data.get('notes', '')
        share.save()
        return Response({'status': 'rejected'})
    
    @action(detail=False, methods=['get'])
    def admin_list(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        shares = SharePurchase.objects.all().order_by('-created_at')
        serializer = self.get_serializer(shares, many=True)
        return Response(serializer.data)

class ShareTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = ShareTransactionSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        if getattr(self.request.user, 'is_staff', False):
            return ShareTransaction.objects.all()
        return ShareTransaction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        share_transaction = serializer.save(user=self.request.user)
        
        # Notify admin about the payment
        send_payment_notification_to_admin(
            user=self.request.user,
            payment_type='Shares Purchase',
            amount=share_transaction.amount
        )
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a share transaction"""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
            
        share = self.get_object()
        share.status = 'approved'
        share.admin_notes = request.data.get('admin_notes', '')
        share.save()
        
        # Update user's shares
        user = share.user
        user.shares_owned += share.shares_purchased
        user.available_shares += share.shares_purchased
        user.save()
        
        # Send approval notification
        try:
            send_payment_approval_notification(user, share)
        except Exception as e:
            print(f"Failed to send approval notification: {e}")
        
        return Response({'message': 'Share approved successfully'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a share transaction"""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
            
        try:
            share = self.get_object()
            share.status = 'rejected'
            notes = request.data.get('notes', '')
            share.admin_notes = notes
            share.save()
            return Response({'message': 'Share rejected successfully'})
        except ShareTransaction.DoesNotExist:
            return Response({'error': 'Share not found'}, status=404)

@csrf_exempt
@require_http_methods(["POST"])
def buy_shares(request):
    try:
        data = json.loads(request.body)
        amount = data.get('amount')
        payment_method = data.get('payment_method')
        shares_purchased = data.get('shares_purchased')
        
        # Create share purchase record
        share_purchase = SharePurchase.objects.create(
            user=request.user if request.user.is_authenticated else None,
            quantity=shares_purchased,
            total_amount=amount,
            payment_method=payment_method,
            status='pending'
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Share purchase submitted successfully',
            'purchase_id': share_purchase.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)