from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from applications.models import Application
from claims.models import Claim
from payments.models import Payment
from contact.models import ContactMessage

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def debug_admin_data(request):
    """Debug endpoint to check data availability"""
    
    data = {
        'user': {
            'username': request.user.username,
            'is_staff': request.user.is_staff,
            'is_superuser': request.user.is_superuser,
        },
        'counts': {
            'users': User.objects.count(),
            'applications': Application.objects.count(),
            'claims': Claim.objects.count(),
            'payments': Payment.objects.count(),
            'contact_messages': ContactMessage.objects.count(),
        },
        'sample_data': {
            'users': list(User.objects.values('id', 'username', 'email', 'first_name', 'last_name')[:3]),
            'applications': list(Application.objects.values('id', 'type', 'status', 'first_name', 'last_name')[:3]),
            'claims': list(Claim.objects.values('id', 'claim_type', 'member_name', 'status')[:3]),
            'payments': list(Payment.objects.values('id', 'amount', 'type', 'status')[:3]),
            'contact_messages': list(ContactMessage.objects.values('id', 'subject', 'name', 'status')[:3]),
        }
    }
    
    return Response(data)