from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class UserDashboardViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        user = request.user
        
        # Import models to avoid circular imports
        from applications.models import Application
        from payments.models import Payment
        from shares.models import SharePurchase
        from claims.models import Claim
        from documents.models import Document
        
        stats = {
            'total_applications': Application.objects.filter(user=user).count(),
            'total_payments': Payment.objects.filter(user=user).count(),
            'total_shares': SharePurchase.objects.filter(user=user, status='approved').aggregate(
                total=Sum('quantity'))['total'] or 0,
            'total_claims': Claim.objects.filter(user=user).count(),
            'total_documents': Document.objects.filter(user=user).count(),
            'pending_claims': Claim.objects.filter(user=user, status='pending').count(),
            'pending_shares': SharePurchase.objects.filter(user=user, status='pending').count(),
            'pending_payments': Payment.objects.filter(user=user, status='pending').count(),
            'activation_status': user.is_activated,
            'membership_status': user.is_member,
        }
        
        return Response(stats)