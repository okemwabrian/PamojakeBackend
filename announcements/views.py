from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .models import Announcement
from .serializers import AnnouncementSerializer
from accounts.email_templates import send_announcement_email

User = get_user_model()

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.filter(is_active=True)
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]  # Allow all users to see announcements
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        announcement = serializer.save(author=self.request.user)
        
        # Send email to all active users
        active_users = User.objects.filter(is_active=True)
        send_announcement_email(active_users, announcement)