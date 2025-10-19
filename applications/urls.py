from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .family_views import single_family_application, double_family_application, admin_applications
from .payment_views import submit_payment

router = DefaultRouter()
router.register(r'', views.ApplicationViewSet, basename='application')

urlpatterns = [
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