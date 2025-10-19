from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Simple health check endpoint to test backend-frontend connection"""
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    
    return Response({
        'status': 'Backend is running',
        'message': 'Pamoja Kenya MN API is working',
        'total_users': total_users,
        'active_users': active_users,
        'version': '1.0.0'
    })