from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer, LoginSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Send registration pending email
        try:
            from .email_templates import send_registration_pending_email
            send_registration_pending_email(user)
        except Exception as e:
            print(f"Failed to send registration email: {e}")
        
        return Response({
            'message': 'Registration successful! Please wait for admin activation. Check your email for details.',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'address': user.address,
            'city': user.city,
            'state': user.state,
            'shares_owned': user.shares_owned,
            'available_shares': user.available_shares,
            'is_member': user.is_member,
            'membership_date': user.membership_date,
            'is_staff': user.is_staff,
            'is_activated': user.is_activated,
            'date_joined': user.date_joined
        }
        
        response_data = {
            'token': str(refresh.access_token),
            'user': user_data
        }
        
        # Check activation status
        if not user.is_activated:
            response_data.update({
                'requires_activation': True,
                'message': 'Account inactive. Pay activation fee to continue.'
            })
        
        return Response(response_data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    return Response({'message': 'Successfully logged out'})

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    if request.method == 'GET':
        return Response({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone': request.user.phone,
            'address': request.user.address,
            'city': request.user.city,
            'state': request.user.state,
            'shares_owned': request.user.shares_owned,
            'available_shares': request.user.available_shares,
            'is_staff': request.user.is_staff
        })
    
    elif request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            # Mark profile as completed if basic info is provided
            if user.first_name and user.last_name and user.phone and user.address:
                user.profile_completed = True
                user.save()
            
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'address': user.address,
                'city': user.city,
                'state': user.state,
                'profile_completed': user.profile_completed,
                'is_staff': user.is_staff
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not user.check_password(old_password):
        return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
    
    if len(new_password) < 6:
        return Response({'error': 'New password must be at least 6 characters'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    
    return Response({'message': 'Password changed successfully'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    from django.db import models
    from applications.models import Application
    from payments.models import Payment
    from shares.models import SharePurchase
    from claims.models import Claim
    from documents.models import Document
    
    user = request.user
    
    stats = {
        'total_applications': Application.objects.filter(user=user).count(),
        'total_payments': Payment.objects.filter(user=user).count(),
        'total_shares': SharePurchase.objects.filter(user=user, status='approved').aggregate(
            total=models.Sum('quantity'))['total'] or 0,
        'total_claims': Claim.objects.filter(user=user).count(),
        'total_documents': Document.objects.filter(user=user).count(),
        'pending_claims': Claim.objects.filter(user=user, status='pending').count(),
        'pending_shares': SharePurchase.objects.filter(user=user, status='pending').count(),
        'activation_status': user.is_activated,
        'membership_status': user.is_member,
    }
    
    return Response(stats)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_status(request):
    try:
        from .models import UserProfile
        profile = UserProfile.objects.get(user=request.user)
        is_activated = profile.is_activated
    except:
        is_activated = False
    
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'is_activated': is_activated
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def test_endpoint(request):
    return Response({'message': 'API is working', 'status': 'success'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_claims(request):
    """Get user's claims"""
    from claims.models import Claim
    claims = Claim.objects.filter(user=request.user).order_by('-created_at')
    claims_data = [{
        'id': claim.id,
        'claim_type': getattr(claim, 'claim_type', 'general'),
        'member_name': getattr(claim, 'member_name', ''),
        'amount_requested': str(claim.amount_requested),
        'amount_approved': str(claim.amount_approved) if claim.amount_approved else None,
        'status': claim.status,
        'description': getattr(claim, 'description', ''),
        'admin_notes': getattr(claim, 'admin_notes', ''),
        'created_at': claim.created_at.isoformat(),
    } for claim in claims]
    
    return Response({'claims': claims_data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_shares(request):
    """Get user's share purchases"""
    from shares.models import SharePurchase
    purchases = SharePurchase.objects.filter(user=request.user).order_by('-created_at')
    purchases_data = [{
        'id': purchase.id,
        'quantity': getattr(purchase, 'quantity', 0),
        'total_amount': str(getattr(purchase, 'total_amount', 0)),
        'payment_method': getattr(purchase, 'payment_method', ''),
        'status': purchase.status,
        'admin_notes': getattr(purchase, 'admin_notes', ''),
        'created_at': purchase.created_at.isoformat(),
    } for purchase in purchases]
    
    return Response({'purchases': purchases_data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_dashboard(request):
    """Get complete user dashboard data"""
    user = request.user
    
    # Get user profile
    try:
        from .models import UserProfile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile_data = {
            'membership_type': getattr(profile, 'membership_type', 'none'),
            'membership_status': 'active' if getattr(user, 'is_activated', False) else 'inactive',
            'shares_owned': getattr(user, 'shares_owned', 0),
            'phone': getattr(user, 'phone', ''),
            'address': getattr(user, 'address', ''),
        }
    except:
        profile_data = {
            'membership_type': getattr(user, 'membership_type', 'none'),
            'membership_status': 'active' if getattr(user, 'is_activated', False) else 'inactive',
            'shares_owned': getattr(user, 'shares_owned', 0),
            'phone': getattr(user, 'phone', ''),
            'address': getattr(user, 'address', ''),
        }
    
    # Get applications
    try:
        from applications.models import Application
        applications = Application.objects.filter(user=user).order_by('-created_at')
        applications_data = [{
            'id': app.id,
            'membership_type': getattr(app, 'membership_type', getattr(app, 'type', 'single')),
            'status': app.status,
            'created_at': app.created_at.isoformat(),
            'admin_notes': getattr(app, 'admin_notes', ''),
        } for app in applications]
    except:
        applications_data = []
    
    # Get claims
    try:
        from claims.models import Claim
        claims = Claim.objects.filter(user=user).order_by('-created_at')
        claims_data = [{
            'id': claim.id,
            'title': getattr(claim, 'claim_type', 'General Claim'),
            'status': claim.status,
            'amount_requested': str(claim.amount_requested),
            'created_at': claim.created_at.isoformat(),
        } for claim in claims]
    except:
        claims_data = []
    
    # Get payments
    try:
        from payments.models import Payment
        payments = Payment.objects.filter(user=user).order_by('-created_at')
        payments_data = [{
            'id': payment.id,
            'payment_type': payment.payment_type,
            'amount': str(payment.amount),
            'status': payment.status,
            'created_at': payment.created_at.isoformat(),
        } for payment in payments]
    except:
        payments_data = []
    
    # Get shares
    try:
        from shares.models import SharePurchase
        shares = SharePurchase.objects.filter(user=user).order_by('-created_at')
        shares_data = [{
            'id': share.id,
            'shares_requested': getattr(share, 'quantity', 0),
            'amount': str(getattr(share, 'total_amount', 0)),
            'status': share.status,
            'created_at': share.created_at.isoformat(),
        } for share in shares]
    except:
        shares_data = []
    
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        },
        'profile': profile_data,
        'applications': applications_data,
        'claims': claims_data,
        'payments': payments_data,
        'shares': shares_data,
        'stats': {
            'total_applications': len(applications_data),
            'total_claims': len(claims_data),
            'total_payments': len(payments_data),
            'total_shares': len(shares_data),
        }
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    """Simple user endpoint for frontend compatibility"""
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
        'is_activated': getattr(user, 'is_activated', False),
        'is_member': getattr(user, 'is_member', False),
        'membership_type': getattr(user, 'membership_type', 'none'),
        'membership_status': 'active' if getattr(user, 'is_activated', False) else 'inactive',
        'shares_owned': getattr(user, 'shares_owned', 0),
        'phone': getattr(user, 'phone', ''),
        'address': getattr(user, 'address', '')
    })