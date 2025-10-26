"""
URL configuration for pamojabackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.utils import timezone
from accounts.views import user_status
from applications.urls import submit_single_application
from payments.urls import submit_activation_fee
from shares.urls import buy_shares

def api_root(request):
    return JsonResponse({
        'message': 'Pamoja Backend API',
        'version': '1.0',
        'status': 'active'
    })

def test_connection(request):
    return JsonResponse({
        'message': 'Backend connection successful',
        'status': 'connected',
        'timestamp': timezone.now().isoformat()
    })

urlpatterns = [
    path('', api_root, name='api_root'),
    path('test-connection/', test_connection, name='test-connection'),
    path('admin/', admin.site.urls),
    path('api/auth/user/', user_status, name='user-status'),
    path('api/auth/', include('accounts.urls')),
    
    # Required endpoints for frontend
    path('api/applications/single/submit/', submit_single_application, name='submit-single-application'),
    path('api/payments/activation/submit/', submit_activation_fee, name='submit-activation-fee'),
    path('api/shares/buy/', buy_shares, name='buy-shares'),
    
    path('api/applications/', include('applications.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/shares/', include('shares.urls')),
    path('api/claims/', include('claims.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/announcements/', include('announcements.urls')),
    path('api/meetings/', include('meetings.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/beneficiaries/', include('beneficiaries.urls')),
    path('api/admin/', include('admin_panel.urls')),
    path('api/core/', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
