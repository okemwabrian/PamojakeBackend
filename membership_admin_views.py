from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count, Q
from django.utils import timezone

from applications.models import Application
from claims.models import Claim
from payments.models import Payment
from shares.models import ShareTransaction
from contact.models import ContactMessage
from documents.models import Document

from applications.serializers import ApplicationSerializer
from claims.serializers import ClaimSerializer
from payments.serializers import PaymentSerializer
from shares.serializers import ShareTransactionSerializer
from contact.serializers import ContactMessageSerializer
from documents.serializers import DocumentSerializer
from accounts.serializers import UserSerializer

User = get_user_model()

class ComprehensiveMembershipAdminViewSet(viewsets.ViewSet):
    """
    Comprehensive admin viewset for complete membership system management
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    # APPLICATIONS MANAGEMENT
    @action(detail=False, methods=['get'])
    def applications(self, request):
        """Get all membership applications"""
        applications = Application.objects.all().order_by('-created_at')
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def approve_application(self, request, pk=None):
        """Approve membership application"""
        try:
            application = Application.objects.get(pk=pk)
            application.status = 'approved'
            application.reviewed_by = request.user
            application.admin_notes = request.data.get('notes', '')
            
            # Update user membership
            user = application.user
            user.membership_type = application.type
            user.is_member = True
            user.is_active = True
            user.is_activated = True
            user.is_active_member = True
            user.membership_date = timezone.now()
            user.activation_date = timezone.now()
            user.activated_by = request.user
            user.deactivation_reason = ''
            user.save()
            
            application.save()
            
            return Response({'status': 'Application approved', 'message': 'User activated successfully'})
        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=404)
    
    @action(detail=True, methods=['post'])
    def reject_application(self, request, pk=None):
        """Reject membership application"""
        try:
            application = Application.objects.get(pk=pk)
            application.status = 'rejected'
            application.reviewed_by = request.user
            application.admin_notes = request.data.get('notes', '')
            application.save()
            return Response({'status': 'Application rejected'})
        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=404)
    
    @action(detail=True, methods=['delete'])
    def delete_application(self, request, pk=None):
        """Delete membership application"""
        try:
            application = Application.objects.get(pk=pk)
            application.delete()
            return Response({'status': 'Application deleted'})
        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=404)
    
    # CLAIMS MANAGEMENT
    @action(detail=False, methods=['get'])
    def claims(self, request):
        """Get all claims"""
        claims = Claim.objects.all().order_by('-created_at')
        serializer = ClaimSerializer(claims, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def approve_claim(self, request, pk=None):
        """Approve claim"""
        try:
            claim = Claim.objects.get(pk=pk)
            claim.status = 'approved'
            claim.admin_notes = request.data.get('notes', '')
            claim.save()
            return Response({'status': 'Claim approved'})
        except Claim.DoesNotExist:
            return Response({'error': 'Claim not found'}, status=404)
    
    @action(detail=True, methods=['post'])
    def reject_claim(self, request, pk=None):
        """Reject claim"""
        try:
            claim = Claim.objects.get(pk=pk)
            claim.status = 'rejected'
            claim.admin_notes = request.data.get('notes', '')
            claim.save()
            return Response({'status': 'Claim rejected'})
        except Claim.DoesNotExist:
            return Response({'error': 'Claim not found'}, status=404)
    
    @action(detail=True, methods=['delete'])
    def delete_claim(self, request, pk=None):
        """Delete claim"""
        try:
            claim = Claim.objects.get(pk=pk)
            claim.delete()
            return Response({'status': 'Claim deleted'})
        except Claim.DoesNotExist:
            return Response({'error': 'Claim not found'}, status=404)
    
    # PAYMENTS MANAGEMENT
    @action(detail=False, methods=['get'])
    def payments(self, request):
        """Get all payments"""
        payments = Payment.objects.all().order_by('-created_at')
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def approve_payment(self, request, pk=None):
        """Approve payment"""
        try:
            payment = Payment.objects.get(pk=pk)
            payment.status = 'approved'
            payment.admin_notes = request.data.get('notes', '')
            payment.processed_by = request.user
            payment.processed_at = timezone.now()
            payment.save()  # This will trigger share addition if payment_type is 'shares'
            return Response({'status': 'Payment approved'})
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=404)
    
    @action(detail=True, methods=['post'])
    def reject_payment(self, request, pk=None):
        """Reject payment"""
        try:
            payment = Payment.objects.get(pk=pk)
            payment.status = 'rejected'
            payment.admin_notes = request.data.get('notes', '')
            payment.save()
            return Response({'status': 'Payment rejected'})
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=404)
    
    # SHARES MANAGEMENT
    @action(detail=False, methods=['get'])
    def shares(self, request):
        """Get all share transactions"""
        shares = ShareTransaction.objects.all().order_by('-created_at')
        serializer = ShareTransactionSerializer(shares, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def approve_share_transaction(self, request, pk=None):
        """Approve share transaction"""
        try:
            transaction = ShareTransaction.objects.get(pk=pk)
            transaction.status = 'approved'
            transaction.admin_notes = request.data.get('notes', '')
            transaction.save()  # This will trigger share addition
            return Response({'status': 'Share transaction approved'})
        except ShareTransaction.DoesNotExist:
            return Response({'error': 'Share transaction not found'}, status=404)
    
    # USER MANAGEMENT
    @action(detail=False, methods=['get'])
    def users(self, request):
        """Get all users"""
        users = User.objects.all().order_by('-date_joined')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate_user(self, request, pk=None):
        """Activate user"""
        try:
            user = User.objects.get(pk=pk)
            user.is_active = True
            user.is_activated = True
            user.is_active_member = True
            user.activation_date = timezone.now()
            user.activated_by = request.user
            user.deactivation_reason = ''
            user.save()
            return Response({'status': 'User activated'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
    
    @action(detail=True, methods=['post'])
    def deactivate_user(self, request, pk=None):
        """Deactivate user"""
        try:
            user = User.objects.get(pk=pk)
            reason = request.data.get('reason', '')
            user.is_active = False
            user.is_active_member = False
            user.deactivation_reason = reason
            user.save()
            return Response({'status': 'User deactivated', 'reason': reason})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
    
    @action(detail=True, methods=['post'])
    def update_user_shares(self, request, pk=None):
        """Update user shares"""
        try:
            user = User.objects.get(pk=pk)
            shares = int(request.data.get('shares', 0))
            user.shares_owned = shares
            user.shares = shares
            user.save()  # This will trigger auto-activation if shares >= 20
            return Response({
                'status': 'Shares updated',
                'shares': user.shares,
                'is_active_member': user.is_active_member
            })
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
    
    # REPORTS AND ANALYTICS
    @action(detail=False, methods=['get'])
    def membership_stats(self, request):
        """Get comprehensive membership statistics"""
        total_users = User.objects.count()
        active_members = User.objects.filter(is_active_member=True).count()
        inactive_members = total_users - active_members
        
        total_applications = Application.objects.count()
        pending_applications = Application.objects.filter(status='pending').count()
        approved_applications = Application.objects.filter(status='approved').count()
        
        total_claims = Claim.objects.count()
        pending_claims = Claim.objects.filter(status='pending').count()
        approved_claims = Claim.objects.filter(status='approved').count()
        
        total_payments = Payment.objects.filter(status='approved').aggregate(
            total=Sum('amount'))['total'] or 0
        pending_payments = Payment.objects.filter(status='pending').count()
        
        total_shares = User.objects.aggregate(total=Sum('shares'))['total'] or 0
        
        return Response({
            'users': {
                'total': total_users,
                'active_members': active_members,
                'inactive_members': inactive_members
            },
            'applications': {
                'total': total_applications,
                'pending': pending_applications,
                'approved': approved_applications
            },
            'claims': {
                'total': total_claims,
                'pending': pending_claims,
                'approved': approved_claims
            },
            'payments': {
                'total_amount': float(total_payments),
                'pending_count': pending_payments
            },
            'shares': {
                'total_shares': total_shares,
                'average_per_member': round(total_shares / max(active_members, 1), 2)
            }
        })
    
    @action(detail=False, methods=['get'])
    def financial_report(self, request):
        """Get financial report"""
        # Total revenue from approved payments
        total_payments = Payment.objects.filter(status='approved').aggregate(
            total=Sum('amount'))['total'] or 0
        
        # Revenue by payment type
        payment_types = Payment.objects.filter(status='approved').values('payment_type').annotate(
            total=Sum('amount'), count=Count('id'))
        
        # Share transactions
        share_revenue = ShareTransaction.objects.filter(status='approved').aggregate(
            total=Sum('total_amount'))['total'] or 0
        
        return Response({
            'total_revenue': float(total_payments + share_revenue),
            'payment_revenue': float(total_payments),
            'share_revenue': float(share_revenue),
            'payment_breakdown': list(payment_types),
            'pending_payments': Payment.objects.filter(status='pending').count()
        })
    
    # BULK OPERATIONS
    @action(detail=False, methods=['post'])
    def bulk_approve_applications(self, request):
        """Bulk approve applications"""
        application_ids = request.data.get('application_ids', [])
        approved_count = 0
        
        for app_id in application_ids:
            try:
                application = Application.objects.get(pk=app_id)
                application.status = 'approved'
                application.reviewed_by = request.user
                
                # Activate user
                user = application.user
                user.membership_type = application.type
                user.is_member = True
                user.is_active = True
                user.is_activated = True
                user.is_active_member = True
                user.membership_date = timezone.now()
                user.activation_date = timezone.now()
                user.activated_by = request.user
                user.save()
                
                application.save()
                approved_count += 1
            except Application.DoesNotExist:
                continue
        
        return Response({
            'status': f'Approved {approved_count} applications',
            'approved_count': approved_count
        })
    
    @action(detail=False, methods=['post'])
    def deduct_shares_all_members(self, request):
        """Deduct shares from all active members"""
        amount = int(request.data.get('amount', 0))
        reason = request.data.get('reason', 'Community support')
        
        if amount <= 0:
            return Response({'error': 'Amount must be greater than 0'}, status=400)
        
        active_users = User.objects.filter(is_active_member=True, shares__gte=amount)
        deactivated_count = 0
        
        for user in active_users:
            user.shares -= amount
            user.shares_owned -= amount
            
            # Auto-deactivate if shares fall below 20
            if user.shares < 20:
                user.is_active_member = False
                user.deactivation_reason = f'Insufficient shares after deduction (below 20)'
                deactivated_count += 1
            
            user.save()
        
        return Response({
            'status': 'Shares deducted successfully',
            'users_affected': active_users.count(),
            'users_deactivated': deactivated_count,
            'amount_deducted': amount,
            'reason': reason
        })