from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import views
from .serializers import ClaimSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_claim(request):
    serializer = ClaimSerializer(data=request.data)
    if serializer.is_valid():
        claim = serializer.save(user=request.user)
        return Response({
            'success': True,
            'message': 'Claim submitted successfully!',
            'claim_id': claim.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

router = DefaultRouter()
router.register(r'', views.ClaimViewSet, basename='claim')

urlpatterns = [
    path('submit/', submit_claim, name='submit-claim'),
    path('', include(router.urls)),
]