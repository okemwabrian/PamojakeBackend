from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from .models import ContactMessage
from .serializers import ContactMessageSerializer

class ContactMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ContactMessageSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return ContactMessage.objects.all()
            return ContactMessage.objects.filter(user=self.request.user)
        return ContactMessage.objects.none()
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            # Auto-fill name and email for authenticated users
            name = f"{self.request.user.first_name} {self.request.user.last_name}".strip()
            serializer.save(
                user=self.request.user,
                name=name or self.request.user.username,
                email=self.request.user.email
            )
        else:
            serializer.save()