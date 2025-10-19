from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .family_serializers import SingleFamilyApplicationSerializer, DoubleFamilyApplicationSerializer
from .models import Application
from django.shortcuts import get_object_or_404

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def single_family_application(request):
    serializer = SingleFamilyApplicationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        application = serializer.save(user=request.user)
        return Response({
            'id': application.id,
            'type': application.type,
            'status': application.status,
            'created_at': application.created_at,
            'message': 'Single family application submitted successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def double_family_application(request):
    serializer = DoubleFamilyApplicationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        application = serializer.save(user=request.user)
        return Response({
            'id': application.id,
            'type': application.type,
            'status': application.status,
            'created_at': application.created_at,
            'message': 'Double family application submitted successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_applications(request):
    status_filter = request.GET.get('status', 'all')
    type_filter = request.GET.get('type', 'all')
    
    applications = Application.objects.all()
    
    if status_filter != 'all':
        applications = applications.filter(status=status_filter)
    if type_filter != 'all':
        applications = applications.filter(type=type_filter)
    
    data = []
    for app in applications:
        address_parts = []
        if app.address_1 or app.address_legacy:
            address_parts.append(app.address_1 or app.address_legacy)
        if app.address_2:
            address_parts.append(app.address_2)
        if app.city:
            address_parts.append(app.city)
        if app.state_province or app.state_legacy:
            address_parts.append(f"{app.state_province or app.state_legacy} {app.zip_postal}")
        
        app_data = {
            'id': app.id,
            'user_name': app.user.get_full_name() or app.user.username,
            'user_email': app.user.email,
            'type': app.type,
            'status': app.status,
            'created_at': app.created_at,
            'first_name': app.first_name,
            'last_name': app.last_name,
            'phone': app.phone_main or app.phone_legacy or app.phone,
            'address': ', '.join(address_parts),
            'admin_notes': app.admin_notes
        }
        
        # Add spouse_name for double applications
        if app.type == 'double':
            app_data['spouse_name'] = app.spouse
        
        data.append(app_data)
    
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_payment(request):
    try:
        # Get user's latest pending application
        application = Application.objects.filter(
            user=request.user, 
            status='pending'
        ).first()
        
        if not application:
            return Response(
                {'error': 'No pending application found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Update application with payment info
        application.payment_reference = request.data.get('payment_reference', '')
        application.activation_fee_paid = True
        application.status = 'payment_submitted'
        application.save()
        
        return Response({
            'message': 'Payment information submitted successfully',
            'application_id': application.id,
            'status': application.status
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': 'Failed to submit payment information'}, 
            status=status.HTTP_400_BAD_REQUEST
        )