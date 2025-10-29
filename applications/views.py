from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils import timezone
from .models import Application
from .serializers import ApplicationSerializer
from accounts.email_templates import send_membership_status_email, send_activation_email
import logging

logger = logging.getLogger(__name__)

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Application.objects.all().order_by('-created_at')
        # Only active users can see applications
        if not self.request.user.is_active:
            return Application.objects.none()
        return Application.objects.filter(user=self.request.user).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        """Override list to return consistent format"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'applications': serializer.data})
    
    def create(self, request, *args, **kwargs):
        # Debug logging
        logger.info(f"Request data keys: {list(request.data.keys())}")
        logger.info(f"Request files: {list(request.FILES.keys())}")
        
        # Print to console for immediate debugging
        print("=== APPLICATION SUBMISSION DEBUG ===")
        print(f"Data keys: {list(request.data.keys())}")
        print(f"Files: {list(request.FILES.keys())}")
        print(f"Content-Type: {request.content_type}")
        
        # Check for required files
        if 'id_document' not in request.FILES:
            print("ERROR: id_document file missing")
            return Response(
                {"id_document": ["ID document file is required"]}, 
                status=400
            )
        
        # Check membership type for spouse document
        membership_type = request.data.get('membership_type')
        if membership_type == 'double' and 'spouse_id_document' not in request.FILES:
            print("ERROR: spouse_id_document file missing for double membership")
            return Response(
                {"spouse_id_document": ["Spouse ID document is required for double membership"]}, 
                status=400
            )
        
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        # Only active users can create applications
        if not self.request.user.is_active:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Account must be activated to submit applications')
        application = serializer.save(user=self.request.user)
        # Send pending email notification
        from accounts.email_templates import send_registration_pending_email
        send_registration_pending_email(self.request.user)
    
    @action(detail=True, methods=['post'])
    def verify_payment(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        application = self.get_object()
        application.payment_verified = True
        application.payment_verified_by = request.user
        application.payment_verified_at = timezone.now()
        application.status = 'payment_submitted'
        application.admin_notes = request.data.get('notes', '')
        application.save()
        return Response({'status': 'payment_verified'})
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        application = self.get_object()
        
        # Auto-verify payment if not already verified
        if not getattr(application, 'payment_verified', True):
            application.payment_verified = True
            application.payment_verified_by = request.user
            application.payment_verified_at = timezone.now()
        
        application.status = 'approved'
        application.user.is_member = True
        application.user.is_active = True
        application.user.is_activated = True
        application.user.is_active_member = True
        application.user.membership_date = timezone.now()
        application.user.activation_date = timezone.now()
        application.user.activated_by = request.user
        application.user.deactivation_reason = ''
        application.user.save()
        application.admin_notes = request.data.get('notes', '')
        application.save()
        
        try:
            send_membership_status_email(application.user, 'approved', application.type)
            send_activation_email(application.user)
        except Exception as e:
            pass
        
        return Response({'status': 'approved'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_application_details(request, application_id):
    """Get detailed application information"""
    try:
        # Admin can view any application, users can only view their own
        if request.user.is_staff:
            application = Application.objects.get(id=application_id)
        else:
            application = Application.objects.get(id=application_id, user=request.user)
        
        application_data = {
            'id': application.id,
            'membership_type': application.membership_type,
            'status': application.status,
            'personal_info': {
                'first_name': application.first_name,
                'middle_name': application.middle_name,
                'last_name': application.last_name,
                'email': application.email,
                'phone': application.phone,
                'date_of_birth': application.date_of_birth.isoformat() if application.date_of_birth else None,
                'id_number': application.id_number,
            },
            'contact_info': {
                'address': application.address,
                'city': application.city,
                'state': application.state,
                'zip_code': application.zip_code,
            },
            'emergency_contact': {
                'name': application.emergency_name,
                'phone': application.emergency_phone,
                'relationship': application.emergency_relationship,
            },
            'spouse_info': {
                'first_name': application.spouse_first_name,
                'last_name': application.spouse_last_name,
                'email': application.spouse_email,
                'phone': application.spouse_phone,
                'date_of_birth': application.spouse_date_of_birth.isoformat() if application.spouse_date_of_birth else None,
                'id_number': application.spouse_id_number,
            } if application.membership_type == 'double' else None,
            'children_info': application.children_info,
            'documents': {
                'id_document': application.id_document.url if application.id_document else None,
                'spouse_id_document': application.spouse_id_document.url if application.spouse_id_document else None,
            },
            'admin_notes': application.admin_notes,
            'created_at': application.created_at.isoformat(),
            'updated_at': application.updated_at.isoformat(),
        }
        
        return Response({'application': application_data})
        
    except Application.DoesNotExist:
        return Response({'error': 'Application not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        application = self.get_object()
        application.status = 'rejected'
        application.admin_notes = request.data.get('notes', '')
        application.save()
        return Response({'status': 'rejected'})
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def admin_list(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        applications = Application.objects.all().order_by('-created_at')
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)