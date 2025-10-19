from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Application

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