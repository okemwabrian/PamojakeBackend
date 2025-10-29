from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import models
from applications.models import Application
from claims.models import Claim
from payments.models import Payment
from shares.models import ShareTransaction

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_registered_members(request):
    """Get all registered members with their details"""
    
    users = User.objects.all().order_by('-date_joined')
    
    members_data = []
    
    for user in users:
        # Get user's applications
        applications = Application.objects.filter(user=user)
        approved_app = applications.filter(status='approved').first()
        
        member_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
            'date_joined': user.date_joined.isoformat(),
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            
            # Application information
            'has_approved_application': bool(approved_app),
            'application_date': approved_app.created_at.isoformat() if approved_app else None,
            'membership_type': approved_app.membership_type if approved_app else 'none',
            
            # Statistics
            'total_applications': applications.count(),
            'total_payments': Payment.objects.filter(user=user).count(),
            'total_claims': Claim.objects.filter(user=user).count(),
            'total_shares': ShareTransaction.objects.filter(user=user).count(),
            
            # Financial info
            'total_paid': float(Payment.objects.filter(
                user=user, status__in=['approved', 'completed']
            ).aggregate(total=models.Sum('amount'))['total'] or 0),
        }
        
        members_data.append(member_data)
    
    return Response({
        'members': members_data,
        'total_count': len(members_data),
        'active_members': len([m for m in members_data if m['is_active']]),
        'approved_members': len([m for m in members_data if m['has_approved_application']]),
    })

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_member_details(request, user_id):
    """Get detailed information about a specific member"""
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'Member not found'}, status=404)
    
    # Get all related data
    applications = Application.objects.filter(user=user).order_by('-created_at')
    payments = Payment.objects.filter(user=user).order_by('-created_at')
    claims = Claim.objects.filter(user=user).order_by('-created_at')
    shares = ShareTransaction.objects.filter(user=user).order_by('-created_at')
    
    return Response({
        'member': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined.isoformat(),
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'last_login': user.last_login.isoformat() if user.last_login else None,
        },
        'applications': [{
            'id': app.id,
            'membership_type': app.membership_type or app.type,
            'status': app.status,
            'created_at': app.created_at.isoformat(),
            'admin_notes': app.admin_notes,
        } for app in applications],
        'payments': [{
            'id': payment.id,
            'payment_type': payment.payment_type,
            'amount': str(payment.amount),
            'status': payment.status,
            'created_at': payment.created_at.isoformat(),
        } for payment in payments],
        'claims': [{
            'id': claim.id,
            'claim_type': claim.claim_type,
            'member_name': claim.member_name,
            'amount_requested': str(claim.amount_requested),
            'status': claim.status,
            'created_at': claim.created_at.isoformat(),
        } for claim in claims],
        'shares': [{
            'id': share.id,
            'buyer_name': share.buyer_name,
            'quantity': share.quantity,
            'total_amount': str(share.total_amount),
            'status': share.status,
            'created_at': share.created_at.isoformat(),
        } for share in shares],
        'statistics': {
            'total_applications': applications.count(),
            'total_payments': payments.count(),
            'total_claims': claims.count(),
            'total_shares': shares.count(),
            'total_paid': float(payments.filter(status__in=['approved', 'completed']).aggregate(
                total=models.Sum('amount'))['total'] or 0),
        }
    })