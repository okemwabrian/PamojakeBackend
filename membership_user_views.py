from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth import get_user_model

from applications.models import Application
from claims.models import Claim
from payments.models import Payment
from shares.models import ShareTransaction
from documents.models import Document

from applications.serializers import ApplicationSerializer
from claims.serializers import ClaimSerializer
from payments.serializers import PaymentSerializer, PaymentCreateSerializer
from shares.serializers import ShareTransactionSerializer
from documents.serializers import DocumentSerializer

User = get_user_model()

class MembershipApplicationViewSet(viewsets.ModelViewSet):
    """User-facing membership application management"""
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Create membership application with file uploads"""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                application = serializer.save(user=request.user)
                return Response(ApplicationSerializer(application).data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class MemberClaimViewSet(viewsets.ModelViewSet):
    """User-facing claims management"""
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        return Claim.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Create claim with file uploads"""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                claim = serializer.save(user=request.user)
                return Response(ClaimSerializer(claim).data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class MemberPaymentViewSet(viewsets.ModelViewSet):
    """User-facing payment management"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Create payment with file uploads"""
        try:
            serializer = PaymentCreateSerializer(data=request.data)
            if serializer.is_valid():
                payment = serializer.save(user=request.user)
                return Response(PaymentSerializer(payment).data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    
    @action(detail=False, methods=['post'])
    def activation_fee(self, request):
        """Submit activation fee payment"""
        amount = request.data.get('amount', 50.00)
        payment_proof = request.FILES.get('payment_proof')
        
        if not payment_proof:
            return Response({'error': 'Payment proof required'}, status=400)
        
        try:
            payment = Payment.objects.create(
                user=request.user,
                payment_type='activation_fee',
                amount=float(amount),
                description='Account Activation Fee',
                payment_proof=payment_proof,
                payment_method=request.data.get('payment_method', ''),
                transaction_id=request.data.get('transaction_id', ''),
                status='pending'
            )
            return Response(PaymentSerializer(payment).data, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class MemberShareViewSet(viewsets.ModelViewSet):
    """User-facing share management"""
    serializer_class = ShareTransactionSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        return ShareTransaction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Purchase shares"""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                share_transaction = serializer.save(
                    user=request.user,
                    buyer_name=request.user.get_full_name()
                )
                return Response(ShareTransactionSerializer(share_transaction).data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    
    @action(detail=False, methods=['get'])
    def my_shares(self, request):
        """Get user's current share information"""
        user = request.user
        return Response({
            'total_shares': user.shares,
            'shares_owned': user.shares_owned,
            'available_shares': user.available_shares,
            'is_active_member': user.is_active_member,
            'membership_type': user.membership_type,
            'share_value': user.shares * 25,  # $25 per share
            'transactions': ShareTransactionSerializer(
                ShareTransaction.objects.filter(user=user).order_by('-created_at')[:10], 
                many=True
            ).data
        })

class MemberDocumentViewSet(viewsets.ModelViewSet):
    """User-facing document management"""
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MemberDashboardViewSet(viewsets.ViewSet):
    """User dashboard with membership overview"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get member dashboard overview"""
        user = request.user
        
        # Get recent applications
        recent_applications = Application.objects.filter(user=user).order_by('-created_at')[:5]
        
        # Get recent claims
        recent_claims = Claim.objects.filter(user=user).order_by('-created_at')[:5]
        
        # Get recent payments
        recent_payments = Payment.objects.filter(user=user).order_by('-created_at')[:5]
        
        # Get recent share transactions
        recent_shares = ShareTransaction.objects.filter(user=user).order_by('-created_at')[:5]
        
        return Response({
            'user_info': {
                'username': user.username,
                'full_name': user.get_full_name(),
                'email': user.email,
                'is_active_member': user.is_active_member,
                'membership_type': user.membership_type,
                'membership_date': user.membership_date,
                'shares': user.shares,
                'share_value': user.shares * 25
            },
            'recent_applications': ApplicationSerializer(recent_applications, many=True).data,
            'recent_claims': ClaimSerializer(recent_claims, many=True).data,
            'recent_payments': PaymentSerializer(recent_payments, many=True).data,
            'recent_shares': ShareTransactionSerializer(recent_shares, many=True).data,
            'stats': {
                'total_applications': Application.objects.filter(user=user).count(),
                'total_claims': Claim.objects.filter(user=user).count(),
                'total_payments': Payment.objects.filter(user=user).count(),
                'total_share_transactions': ShareTransaction.objects.filter(user=user).count()
            }
        })
    
    @action(detail=False, methods=['get'])
    def membership_status(self, request):
        """Get detailed membership status"""
        user = request.user
        
        # Check if user has pending applications
        pending_application = Application.objects.filter(
            user=user, status='pending'
        ).first()
        
        # Check activation requirements
        activation_requirements = {
            'has_approved_application': Application.objects.filter(
                user=user, status='approved'
            ).exists(),
            'has_minimum_shares': user.shares >= 20,
            'is_active_member': user.is_active_member
        }
        
        return Response({
            'membership_status': {
                'is_member': user.is_member,
                'is_active_member': user.is_active_member,
                'membership_type': user.membership_type,
                'activation_date': user.activation_date,
                'deactivation_reason': user.deactivation_reason
            },
            'shares_info': {
                'current_shares': user.shares,
                'minimum_required': 20,
                'meets_requirement': user.shares >= 20,
                'share_value': user.shares * 25
            },
            'pending_application': ApplicationSerializer(pending_application).data if pending_application else None,
            'activation_requirements': activation_requirements,
            'next_steps': self._get_next_steps(user, activation_requirements)
        })
    
    def _get_next_steps(self, user, requirements):
        """Get recommended next steps for user"""
        steps = []
        
        if not requirements['has_approved_application']:
            if Application.objects.filter(user=user, status='pending').exists():
                steps.append("Wait for application approval")
            else:
                steps.append("Submit membership application")
        
        if not requirements['has_minimum_shares']:
            needed_shares = 20 - user.shares
            steps.append(f"Purchase {needed_shares} more shares (${needed_shares * 25})")
        
        if requirements['has_approved_application'] and requirements['has_minimum_shares'] and not user.is_active_member:
            steps.append("Contact admin for account activation")
        
        if not steps:
            steps.append("You're all set! Enjoy your membership benefits.")
        
        return steps