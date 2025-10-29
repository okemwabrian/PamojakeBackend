from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from django.db import models
from applications.models import Application
from claims.models import Claim
from payments.models import Payment
from contact.models import ContactMessage
from shares.models import ShareTransaction
from applications.serializers import ApplicationSerializer
from claims.serializers import ClaimSerializer
from payments.serializers import PaymentSerializer
from contact.serializers import ContactMessageSerializer
from accounts.serializers import UserSerializer
from .models import UserActivity
from accounts.email_templates import (
    send_activation_email, send_deactivation_email, send_password_reset_email,
    send_low_shares_warning, send_membership_status_email, send_claim_status_email,
    send_shares_deduction_notification, send_auto_deactivation_email
)

User = get_user_model()

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # Disable pagination for admin
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_membership(self, request, pk=None):
        user = self.get_object()
        user.is_member = not user.is_member
        user.save()
        return Response({'status': 'membership toggled'})
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get admin overview statistics"""
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        inactive_users = User.objects.filter(is_active=False).count()
        total_shares = User.objects.aggregate(total=models.Sum('shares_owned'))['total'] or 0
        
        return Response({
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': inactive_users,
            'total_shares': total_shares
        })
    
    @action(detail=False, methods=['get'])
    def registered_users(self, request):
        """Get list of registered users for admin view"""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
            
        users = User.objects.all().values(
            'id', 'username', 'first_name', 'last_name', 'email', 'full_name',
            'phone_number', 'address', 'date_of_birth', 'is_active', 'is_activated',
            'date_joined', 'registration_date', 'last_login', 'shares_owned', 'available_shares'
        )
        return Response(list(users))
    
    @action(detail=False, methods=['get'])
    def get_all_users(self, request):
        """Get all users for admin management"""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
            
        users = User.objects.all().values(
            'id', 'username', 'email', 'first_name', 'last_name', 
            'full_name', 'phone_number', 'address', 'date_of_birth',
            'is_activated', 'registration_date', 'last_login'
        )
        return Response(list(users))
    
    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        user = self.get_object()
        success, new_password = send_password_reset_email(user)
        
        if success:
            return Response({'status': 'password reset', 'message': 'New password sent to user email'})
        else:
            return Response({'error': 'Failed to send password reset email'}, status=500)
    
    @action(detail=True, methods=['post'])
    def activate_user(self, request, pk=None):
        from django.utils import timezone
        user = self.get_object()
        user.is_active = True
        user.is_activated = True
        user.is_active_member = True
        user.activation_date = timezone.now()
        user.activated_by = request.user
        user.deactivation_reason = ''  # Clear reason on reactivation
        user.save()
        
        # Send activation email
        send_activation_email(user)
        
        return Response({'status': 'user activated', 'message': 'User activated successfully'})
    
    @action(detail=True, methods=['post'])
    def deactivate_user(self, request, pk=None):
        user = self.get_object()
        reason = request.data.get('reason', '')
        user.is_active = False
        user.is_active_member = False
        user.deactivation_reason = reason
        user.save()
        
        # Send deactivation email with reason
        if reason:
            send_deactivation_email(user, reason)
        
        return Response({'status': 'user deactivated', 'reason': reason})
    
    @action(detail=True, methods=['post'])
    def update_shares(self, request, pk=None):
        user = self.get_object()
        shares_owned = request.data.get('shares_owned')
        available_shares = request.data.get('available_shares')
        
        if shares_owned is not None:
            user.shares_owned = int(shares_owned)
            # Send low shares warning if below 25
            if user.shares_owned < 25:
                send_low_shares_warning(user)
                
        if available_shares is not None:
            user.available_shares = int(available_shares)
            
        user.save()
        # Auto-deactivate if shares below 20
        if user.shares_owned < 20 and user.is_active:
            user.is_active = False
            user.deactivation_reason = 'Insufficient shares balance (below 20)'
            user.save()
            send_auto_deactivation_email(user)
            
        user.save()
        return Response({
            'status': 'shares updated', 
            'shares_owned': user.shares_owned,
            'available_shares': user.available_shares,
            'auto_deactivated': user.shares_owned < 20
        })

class AdminApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """Get detailed application information"""
        try:
            app = self.get_object()
            data = {
                'id': app.id,
                'user': {
                    'username': app.user.username,
                    'email': app.user.email,
                    'full_name': getattr(app.user, 'full_name', ''),
                    'phone': getattr(app.user, 'phone_number', ''),
                },
                'membership_type': app.membership_type or app.type,
                'status': app.status,
                'created_at': app.created_at.isoformat(),
                'updated_at': app.updated_at.isoformat(),
                
                # Complete Personal Details
                'personal_details': {
                    'first_name': app.first_name,
                    'middle_name': app.middle_name,
                    'last_name': app.last_name,
                    'email': app.email,
                    'confirm_email': app.confirm_email,
                    'phone': app.phone,
                    'phone_main': app.phone_main,
                    'date_of_birth': app.date_of_birth.isoformat() if app.date_of_birth else None,
                    'id_number': app.id_number,
                },
                
                # Complete Address Details
                'address_details': {
                    'address': app.address,
                    'address_1': app.address_1,
                    'address_2': app.address_2,
                    'city': app.city,
                    'state': app.state,
                    'state_province': app.state_province,
                    'zip_code': app.zip_code,
                    'zip_postal': app.zip_postal,
                },
                
                # Emergency Contact
                'emergency_contact': {
                    'name': app.emergency_name,
                    'phone': app.emergency_phone,
                    'relationship': app.emergency_relationship,
                },
                
                # Spouse Details (for double membership)
                'spouse_details': {
                    'first_name': app.spouse_first_name,
                    'last_name': app.spouse_last_name,
                    'email': app.spouse_email,
                    'phone': app.spouse_phone,
                    'date_of_birth': app.spouse_date_of_birth.isoformat() if app.spouse_date_of_birth else None,
                    'id_number': app.spouse_id_number,
                    'spouse': app.spouse,
                    'authorized_rep': app.authorized_rep,
                },
                
                # Family Information
                'family_info': {
                    'children_info': app.children_info if app.children_info else [],
                    'child_1': app.child_1,
                    'child_2': app.child_2,
                    'child_3': app.child_3,
                    'child_4': app.child_4,
                    'child_5': app.child_5,
                    'parent_1': app.parent_1,
                    'parent_2': app.parent_2,
                    'spouse_parent_1': app.spouse_parent_1,
                    'spouse_parent_2': app.spouse_parent_2,
                    'sibling_1': app.sibling_1,
                    'sibling_2': app.sibling_2,
                    'sibling_3': app.sibling_3,
                },
                
                # Documents
                'documents': {
                    'id_document': app.id_document.url if app.id_document else None,
                    'spouse_id_document': app.spouse_id_document.url if app.spouse_id_document else None,
                    'payment_proof': app.payment_proof.url if app.payment_proof else None,
                },
                
                # Payment Information
                'payment_info': {
                    'payment_amount': str(app.payment_amount),
                    'payment_reference': app.payment_reference,
                    'activation_fee_paid': app.activation_fee_paid,
                    'activation_fee_amount': str(app.activation_fee_amount),
                    'payment_verified': app.payment_verified,
                },
                
                # Agreements
                'agreements': {
                    'declaration_accepted': app.declaration_accepted,
                    'constitution_agreed': app.constitution_agreed,
                },
                
                'admin_notes': app.admin_notes,
            }
            return Response(data)
        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=404)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        application = self.get_object()
        application.status = 'approved'
        application.save()
        
        # Send approval email
        send_membership_status_email(application.user, 'approved', application.type)
        
        return Response({'status': 'approved'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        application = self.get_object()
        application.status = 'rejected'
        notes = request.data.get('notes', '')
        if notes:
            application.admin_notes = notes
        application.save()
        
        # Send rejection email
        send_membership_status_email(application.user, 'rejected', application.type)
        
        return Response({'status': 'rejected', 'message': 'Application rejected successfully'})

class AdminClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        claim = self.get_object()
        claim.status = 'rejected'
        claim.save()
        
        # Send rejection email
        send_claim_status_email(claim.user, claim, 'rejected')
        
        return Response({'status': 'rejected'})
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        claim = self.get_object()
        claim.status = 'approved'
        amount = request.data.get('amount_approved')
        if amount:
            claim.amount_approved = amount
        claim.save()
        
        # Send approval email
        send_claim_status_email(claim.user, claim, 'approved')
        
        return Response({'status': 'approved'})

class AdminPaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def approve_payment(self, request, pk=None):
        from django.utils import timezone
        payment = self.get_object()
        payment.status = 'completed'
        payment.processed_by = request.user
        payment.processed_at = timezone.now()
        payment.admin_notes = request.data.get('notes', '')
        payment.save()
        return Response({'status': 'approved', 'message': 'Payment approved successfully'})
    
    @action(detail=True, methods=['post'])
    def reject_payment(self, request, pk=None):
        payment = self.get_object()
        payment.status = 'failed'
        payment.admin_notes = request.data.get('notes', 'Payment rejected by admin')
        payment.save()
        return Response({'status': 'rejected', 'message': 'Payment rejected'})
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        payment = self.get_object()
        payment.status = 'completed'
        payment.save()
        return Response({'status': 'completed'})



class AdminContactViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        message = self.get_object()
        message.status = 'read'
        message.save()
        return Response({'status': 'read'})
    
    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        from django.utils import timezone
        message = self.get_object()
        reply_text = request.data.get('reply')
        
        if not reply_text:
            return Response({'error': 'Reply text is required'}, status=400)
        
        message.admin_reply = reply_text
        message.status = 'replied'
        message.replied_by = request.user
        message.replied_at = timezone.now()
        message.save()
        
        return Response({'status': 'replied', 'reply': reply_text})
    
    @action(detail=True, methods=['post'])
    def mark_replied(self, request, pk=None):
        message = self.get_object()
        message.status = 'replied'
        message.save()
        return Response({'status': 'replied'})
    
    @action(detail=False, methods=['post'])
    def deduct_shares_all(self, request):
        """Deduct shares from all active members"""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
            
        amount = int(request.data.get('amount', 0))
        reason = request.data.get('reason', 'Community support')
        
        if amount <= 0:
            return Response({'error': 'Amount must be greater than 0'}, status=400)
            
        # Get all active users with sufficient shares
        users = User.objects.filter(is_active=True, shares_owned__gte=amount)
        deactivated_users = []
        
        for user in users:
            user.shares_owned -= amount
            
            # Auto-deactivate if shares fall below 20
            if user.shares_owned < 20:
                user.is_active = False
                user.deactivation_reason = f'Insufficient shares after deduction (below 20)'
                deactivated_users.append(user)
                send_auto_deactivation_email(user)
                
            user.save()
        
        # Send individual email notifications
        from accounts.email_templates import send_share_deduction_email
        for user in users:
            send_share_deduction_email(user, amount, user.shares_owned, reason)
        
        return Response({
            'status': 'shares deducted',
            'users_affected': users.count(),
            'users_deactivated': len(deactivated_users),
            'amount_deducted': amount,
            'reason': reason
        })
    
    @action(detail=False, methods=['get'])
    def financial_report(self, request):
        from django.db.models import Sum
        total_payments = Payment.objects.filter(status='completed').aggregate(
            total=Sum('amount'))['total'] or 0
        total_shares_sold = ShareTransaction.objects.filter(status='approved').aggregate(
            total=Sum('total_amount'))['total'] or 0
        pending_payments = Payment.objects.filter(status='pending').count()
        
        return Response({
            'total_payments': float(total_payments),
            'total_shares_sold': float(total_shares_sold),
            'pending_payments': pending_payments,
            'total_revenue': float(total_payments + total_shares_sold)
        })
    
    @action(detail=False, methods=['get'])
    def shares_report(self, request):
        from django.db.models import Sum, Avg
        total_shares = User.objects.aggregate(total=Sum('shares_owned'))['total'] or 0
        active_members = User.objects.filter(is_active_member=True).count()
        inactive_members = User.objects.filter(is_active_member=False).count()
        avg_shares = User.objects.aggregate(avg=Avg('shares_owned'))['avg'] or 0
        
        return Response({
            'total_shares': total_shares,
            'active_members': active_members,
            'inactive_members': inactive_members,
            'average_shares': round(float(avg_shares), 2)
        })