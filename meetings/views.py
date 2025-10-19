from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .models import Meeting, MeetingRegistration
from .serializers import MeetingSerializer
from accounts.email_templates import send_meeting_notification
from notifications.utils import send_meeting_registration_confirmation

User = get_user_model()

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]  # Allow all users to see meetings
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]  # Only authenticated users can create/edit/delete
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        # Only staff users can create meetings
        if not request.user.is_staff:
            return Response({'error': 'Only administrators can create meetings'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        # Only staff users can update meetings
        if not request.user.is_staff:
            return Response({'error': 'Only administrators can update meetings'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        # Only staff users can delete meetings
        if not request.user.is_staff:
            return Response({'error': 'Only administrators can delete meetings'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        meeting = serializer.save(created_by=self.request.user)
        
        # Send email notification to all active users
        try:
            active_users = User.objects.filter(is_active=True)
            send_meeting_notification(active_users, meeting)
        except Exception as e:
            print(f"Failed to send meeting notification: {e}")
            # Continue without failing the meeting creation
    
    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        meeting = self.get_object()
        
        # Check if meeting is expired
        if hasattr(meeting, 'is_expired') and meeting.is_expired:
            return Response({'error': 'Cannot register for expired meeting'}, status=status.HTTP_400_BAD_REQUEST)
        
        registration, created = MeetingRegistration.objects.get_or_create(
            meeting=meeting, 
            user=request.user
        )
        if created:
            # Send confirmation email
            try:
                send_meeting_registration_confirmation(request.user, meeting)
            except Exception as e:
                print(f"Failed to send registration confirmation: {e}")
            
            return Response({'message': 'Successfully registered for meeting'})
        else:
            return Response({'message': 'Already registered'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def registrations(self, request, pk=None):
        """Get all registrations for a meeting (admin only)"""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        meeting = self.get_object()
        registrations = MeetingRegistration.objects.filter(meeting=meeting).select_related('user')
        
        registration_data = [{
            'id': reg.id,
            'user_id': reg.user.id,
            'username': reg.user.username,
            'first_name': reg.user.first_name,
            'last_name': reg.user.last_name,
            'email': reg.user.email,
            'registered_at': reg.registered_at
        } for reg in registrations]
        
        return Response({
            'meeting_id': meeting.id,
            'meeting_title': meeting.title,
            'total_registrations': len(registration_data),
            'registrations': registration_data
        })