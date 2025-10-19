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
from accounts.views import user_status

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/user/', user_status, name='user-status'),
    path('api/auth/', include('accounts.urls')),
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
