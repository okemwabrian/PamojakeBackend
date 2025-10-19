from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Beneficiary
from .serializers import BeneficiarySerializer

class BeneficiaryViewSet(viewsets.ModelViewSet):
    serializer_class = BeneficiarySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Beneficiary.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_request(request):
    # Handle beneficiary change request
    return Response({
        'message': 'Beneficiary change request submitted successfully',
        'status': 'pending'
    }, status=status.HTTP_201_CREATED)