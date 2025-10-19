from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import send_mail
from django.conf import settings
from .models import Claim
from .serializers import ClaimSerializer
from accounts.email_templates import send_claim_status_email

class ClaimViewSet(viewsets.ModelViewSet):
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Claim.objects.all()
        return Claim.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                claim = serializer.save(user=request.user)
                
                # Send notification to admin
                send_mail(
                    subject=f'New Claim Submitted - {request.user.username}',
                    message=f'''
                    New claim submitted:
                    
                    User: {request.user.get_full_name()}
                    Email: {request.user.email}
                    Type: {claim.claim_type}
                    Amount: ${claim.amount_requested}
                    Description: {claim.description}
                    Date: {claim.created_at}
                    
                    Please review in admin panel.
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['pamojakeny@gmail.com'],
                    fail_silently=True,
                )
                
                return Response(ClaimSerializer(claim).data, status=201)
            return Response({'message': 'Invalid claim data'}, status=400)
        except Exception as e:
            return Response({'message': str(e)}, status=400)
    
    def perform_create(self, serializer):
        claim = serializer.save(user=self.request.user)
        # Send pending email notification
        try:
            send_claim_status_email(self.request.user, claim, 'pending')
        except Exception as e:
            pass  # Continue even if email fails
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        claim = self.get_object()
        claim.status = 'approved'
        claim.admin_notes = request.data.get('notes', '')
        claim.save()
        try:
            send_claim_status_email(claim.user, claim, 'approved')
        except Exception as e:
            pass
        return Response({'status': 'approved'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        claim = self.get_object()
        claim.status = 'rejected'
        claim.admin_notes = request.data.get('notes', '')
        claim.save()
        try:
            send_claim_status_email(claim.user, claim, 'rejected')
        except Exception as e:
            pass
        return Response({'status': 'rejected'})
    
    @action(detail=False, methods=['get'])
    def admin_list(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        claims = Claim.objects.all().order_by('-created_at')
        serializer = self.get_serializer(claims, many=True)
        return Response(serializer.data)