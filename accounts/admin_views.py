from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.utils import timezone
from .models import User
from .serializers import UserSerializer
from applications.models import Application
from applications.serializers import ApplicationSerializer
from documents.models import Document
from documents.serializers import DocumentSerializer
from payments.models import Payment
from shares.models import ShareTransaction

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
    def list(self, request):
        users = User.objects.all()
        data = [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'date_joined': user.date_joined
        } for user in users]
        return Response(data)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return Response({'status': 'active toggled'})
    
    @action(detail=True, methods=['post'])
    def toggle_admin(self, request, pk=None):
        user = self.get_object()
        # Prevent removing admin rights from self or other admins
        if user.is_staff and (user == request.user or user.is_superuser):
            return Response({'error': 'Cannot remove admin rights from yourself or superuser'}, 
                          status=status.HTTP_403_FORBIDDEN)
        user.is_staff = not user.is_staff
        user.save()
        return Response({'status': 'admin toggled'})
    
    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        user = self.get_object()
        user.set_password('newpassword123')
        user.save()
        return Response({'status': 'password reset'})
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        # Prevent modifying admin users
        if user.is_staff and user != request.user:
            return Response({'error': 'Cannot modify other admin users'}, 
                          status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        # Prevent deleting admin users or self
        if user.is_staff or user == request.user:
            return Response({'error': 'Cannot delete admin users or yourself'}, 
                          status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def activate_user(self, request, pk=None):
        from django.core.mail import send_mail
        from django.conf import settings
        
        user = self.get_object()
        user.is_activated = True
        user.is_active = True
        user.activation_date = timezone.now()
        user.activated_by = request.user
        user.save()
        
        # Send activation email to user
        send_mail(
            subject='Account Activated - Pamoja Kenya MN',
            message=f'''
            Dear {user.get_full_name()},
            
            Your account has been successfully activated!
            
            You now have full access to all features including:
            - Membership applications
            - Share purchases
            - Benefit claims
            - Meeting registrations
            
            Welcome to Pamoja Kenya MN!
            
            Best regards,
            Pamoja Kenya MN Team
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        
        # Send notification to admin
        send_mail(
            subject=f'User Activated - {user.username}',
            message=f'''
            User account activated:
            
            User: {user.get_full_name()}
            Email: {user.email}
            Username: {user.username}
            Activated by: {request.user.username}
            Date: {timezone.now()}
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['pamojakeny@gmail.com'],
            fail_silently=True,
        )
        
        return Response({'message': 'User activated successfully'})
    
    @action(detail=False, methods=['get'])
    def financial_report(self, request):
        # Generate financial report
        payments = Payment.objects.all()
        total_revenue = sum(p.amount for p in payments if p.status == 'approved')
        pending_payments = payments.filter(status='pending').count()
        approved_payments = payments.filter(status='approved').count()
        
        report_data = {
            'total_revenue': total_revenue,
            'pending_payments': pending_payments,
            'approved_payments': approved_payments,
            'payment_breakdown': {
                'activation_fees': sum(p.amount for p in payments if p.type == 'activation_fee' and p.status == 'approved'),
                'share_purchases': sum(p.amount for p in payments if p.type == 'share_purchase' and p.status == 'approved'),
                'membership_fees': sum(p.amount for p in payments if p.type == 'membership_fee' and p.status == 'approved')
            }
        }
        return Response(report_data)
    
    @action(detail=False, methods=['get'])
    def shares_report(self, request):
        # Generate shares report
        share_transactions = ShareTransaction.objects.all()
        total_shares_sold = sum(t.shares_purchased for t in share_transactions if t.status == 'completed')
        total_share_revenue = sum(t.amount for t in share_transactions if t.status == 'completed')
        pending_transactions = share_transactions.filter(status='pending').count()
        
        report_data = {
            'total_shares_sold': total_shares_sold,
            'total_share_revenue': total_share_revenue,
            'pending_transactions': pending_transactions,
            'completed_transactions': share_transactions.filter(status='completed').count(),
            'average_share_price': total_share_revenue / total_shares_sold if total_shares_sold > 0 else 0
        }
        return Response(report_data)
    
    @action(detail=True, methods=['get'])
    def application_details(self, request, pk=None):
        try:
            application = Application.objects.get(pk=pk)
            documents = Document.objects.filter(user=application.user)
            
            return Response({
                'application': ApplicationSerializer(application).data,
                'documents': DocumentSerializer(documents, many=True).data,
                'user_details': UserSerializer(application.user).data
            })
        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=404)

class AdminPaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-created_at')
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'])
    def approve_payment(self, request, pk=None):
        payment = self.get_object()
        payment.status = 'completed'
        payment.processed_by = request.user
        payment.processed_at = timezone.now()
        payment.admin_notes = request.data.get('notes', '')
        payment.save()
        
        # Send email notification to user
        try:
            from notifications.utils import send_payment_approval_notification
            send_payment_approval_notification(payment.user, payment)
        except Exception as e:
            print(f"Failed to send approval notification: {e}")
        
        return Response({'message': 'Payment approved successfully'})

    @action(detail=True, methods=['post'])
    def reject_payment(self, request, pk=None):
        payment = self.get_object()
        payment.status = 'failed'
        payment.processed_by = request.user
        payment.processed_at = timezone.now()
        payment.admin_notes = request.data.get('reason', '')
        payment.save()
        
        return Response({'message': 'Payment rejected'})

    @action(detail=False, methods=['get'])
    def payment_financial_report(self, request):
        from django.db.models import Sum, Count
        
        payments = Payment.objects.filter(status='completed')
        
        report = {
            'total_revenue': payments.aggregate(Sum('amount'))['amount__sum'] or 0,
            'total_payments': payments.count(),
            'by_type': {},
            'recent_payments': PaymentSerializer(
                payments.order_by('-processed_at')[:10], many=True
            ).data
        }
        
        for payment_type, display_name in PAYMENT_TYPES:
            type_payments = payments.filter(payment_type=payment_type)
            report['by_type'][payment_type] = {
                'name': display_name,
                'count': type_payments.count(),
                'total': type_payments.aggregate(Sum('amount'))['amount__sum'] or 0
            }
        
        return Response(report)

    @action(detail=False, methods=['get'])
    def payment_shares_report(self, request):
        share_payments = Payment.objects.filter(
            payment_type='shares', 
            status='completed'
        )
        
        report = {
            'total_share_revenue': share_payments.aggregate(Sum('amount'))['amount__sum'] or 0,
            'total_share_purchases': share_payments.count(),
            'recent_purchases': PaymentSerializer(
                share_payments.order_by('-processed_at')[:20], many=True
            ).data
        }
        
        return Response(report)