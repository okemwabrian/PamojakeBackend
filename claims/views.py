from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import json
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

@csrf_exempt
@require_http_methods(["POST"])
def approve_claim_with_amount(request, claim_id):
    """Approve claim with specific amount"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        claim = Claim.objects.get(id=claim_id)
        
        # Get approval data from request
        data = json.loads(request.body)
        amount_approved = data.get('amount_approved')
        admin_notes = data.get('admin_notes', '')
        
        if not amount_approved:
            return JsonResponse({'error': 'Amount approved is required'}, status=400)
        
        # Update claim
        claim.status = 'approved'
        claim.amount_approved = amount_approved
        claim.admin_notes = admin_notes
        claim.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Claim approved with amount ${amount_approved}',
            'claim': {
                'id': claim.id,
                'status': claim.status,
                'amount_approved': str(claim.amount_approved),
                'admin_notes': claim.admin_notes,
            }
        })
        
    except Claim.DoesNotExist:
        return JsonResponse({'error': 'Claim not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def reject_claim_with_reason(request, claim_id):
    """Reject claim with reason"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        claim = Claim.objects.get(id=claim_id)
        
        # Get rejection data from request
        data = json.loads(request.body)
        admin_notes = data.get('admin_notes', 'Claim rejected')
        
        # Update claim
        claim.status = 'rejected'
        claim.admin_notes = admin_notes
        claim.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Claim rejected',
            'claim': {
                'id': claim.id,
                'status': claim.status,
                'admin_notes': claim.admin_notes,
            }
        })
        
    except Claim.DoesNotExist:
        return JsonResponse({'error': 'Claim not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def get_claim_details(request, claim_id):
    """Get detailed claim information"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        # Admin can view any claim, users can only view their own
        if request.user.is_staff:
            claim = Claim.objects.get(id=claim_id)
        else:
            claim = Claim.objects.get(id=claim_id, user=request.user)
        
        claim_data = {
            'id': claim.id,
            'claim_type': claim.claim_type,
            'member_name': claim.member_name,
            'relationship': claim.relationship,
            'amount_requested': str(claim.amount_requested),
            'amount_approved': str(claim.amount_approved) if claim.amount_approved else None,
            'incident_date': claim.incident_date.isoformat(),
            'description': claim.description,
            'supporting_documents': claim.supporting_documents.url if claim.supporting_documents else None,
            'status': claim.status,
            'admin_notes': claim.admin_notes,
            'created_at': claim.created_at.isoformat(),
            'updated_at': claim.updated_at.isoformat(),
        }
        
        return JsonResponse({'claim': claim_data})
        
    except Claim.DoesNotExist:
        return JsonResponse({'error': 'Claim not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)