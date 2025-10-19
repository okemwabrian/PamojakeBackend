from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not old_password or not new_password:
        return Response({'error': 'Both old and new passwords are required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    if not authenticate(username=user.username, password=old_password):
        return Response({'error': 'Invalid old password'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    
    return Response({'message': 'Password changed successfully'})