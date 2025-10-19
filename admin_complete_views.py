from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from applications.models import Application
from applications.serializers import ApplicationSerializer
from payments.models import Payment
from payments.serializers import PaymentSerializer
from claims.models import Claim
from claims.serializers import ClaimSerializer
from shares.models import SharePurchase
from shares.serializers import SharePurchaseSerializer
from accounts.serializers import UserSerializer

User = get_user_model()

# Admin List Views
class AdminApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        return Application.objects.all().order_by('-created_at')

class AdminPaymentsView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        return Payment.objects.all().order_by('-created_at')

class AdminClaimsView(generics.ListAPIView):
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        return Claim.objects.all().order_by('-created_at')

class AdminSharesView(generics.ListAPIView):
    serializer_class = SharePurchaseSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        return SharePurchase.objects.all().order_by('-created_at')

class AdminUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')

# Admin Dashboard Stats
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_dashboard_stats(request):
    stats = {
        'total_users': User.objects.count(),
        'active_members': User.objects.filter(is_active_member=True).count(),
        'pending_applications': Application.objects.filter(status='pending').count(),
        'pending_payments': Payment.objects.filter(status='pending').count(),
        'pending_claims': Claim.objects.filter(status='pending').count(),
        'pending_shares': SharePurchase.objects.filter(status='pending').count(),
        'total_applications': Application.objects.count(),
        'total_payments': Payment.objects.count(),
        'total_claims': Claim.objects.count(),
        'total_shares': SharePurchase.objects.count(),
    }
    return Response(stats)

# Bulk Actions
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def bulk_approve_applications(request):
    application_ids = request.data.get('application_ids', [])
    notes = request.data.get('notes', '')
    
    applications = Application.objects.filter(id__in=application_ids)
    for app in applications:
        app.status = 'approved'
        app.admin_notes = notes
        app.user.is_member = True
        app.user.is_active = True
        app.user.save()
        app.save()
    
    return Response({'message': f'Approved {len(applications)} applications'})

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def bulk_approve_payments(request):
    payment_ids = request.data.get('payment_ids', [])
    notes = request.data.get('notes', '')
    
    payments = Payment.objects.filter(id__in=payment_ids)
    for payment in payments:
        payment.status = 'approved'
        payment.admin_notes = notes
        
        # Update shares if share purchase
        if payment.payment_type == 'share_purchase':
            shares_to_add = int(payment.amount // 25)
            payment.user.shares += shares_to_add
            if payment.user.shares >= 20:
                payment.user.is_active_member = True
            payment.user.save()
        
        payment.save()
    
    return Response({'message': f'Approved {len(payments)} payments'})