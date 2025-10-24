from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .family_views import single_family_application, double_family_application, admin_applications
from .payment_views import submit_payment

router = DefaultRouter()
router.register(r'', views.ApplicationViewSet, basename='application')

# New application endpoints
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import ApplicationSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_single_application(request):
    data = request.data.copy()
    data['membership_type'] = 'single'
    serializer = ApplicationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Single family application submitted successfully!',
            'application_id': serializer.data['id']
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_double_application(request):
    data = request.data.copy()
    data['membership_type'] = 'double'
    serializer = ApplicationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Double family application submitted successfully!',
            'application_id': serializer.data['id']
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

urlpatterns = [
    # New endpoints for frontend
    path('single/submit/', submit_single_application, name='submit-single-application'),
    path('double/submit/', submit_double_application, name='submit-double-application'),
    
    # Existing endpoints
    path('single/', single_family_application, name='single-family-application'),
    path('double/', double_family_application, name='double-family-application'),
    path('submit-payment/', submit_payment, name='submit-payment'),
    path('', include(router.urls)),
]

# Admin URLs
admin_urlpatterns = [
    path('admin/applications/', admin_applications, name='admin-applications'),
]

urlpatterns += admin_urlpatterns