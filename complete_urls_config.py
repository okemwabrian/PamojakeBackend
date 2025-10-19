# COMPLETE URL CONFIGURATION FOR PAMOJA BACKEND

# 1. Main pamojabackend/urls.py
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
"""

# 2. accounts/urls.py
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .dashboard_views import UserDashboardViewSet

router = DefaultRouter()
router.register(r'dashboard', UserDashboardViewSet, basename='dashboard')

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user_profile, name='user_profile'),
    path('user-status/', views.user_status, name='user_status'),
    path('change-password/', views.change_password, name='change_password'),
    path('dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
    path('', include(router.urls)),
]
"""

# 3. applications/urls.py
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.ApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
]
"""

# 4. payments/urls.py
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]
"""

# 5. claims/urls.py
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.ClaimViewSet, basename='claim')

urlpatterns = [
    path('', include(router.urls)),
]
"""

# 6. shares/urls.py
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.ShareViewSet, basename='share')

urlpatterns = [
    path('', include(router.urls)),
]
"""

# 7. admin_panel/urls.py
"""
from django.urls import path
from admin_complete_views import (
    AdminApplicationsView, AdminPaymentsView, AdminClaimsView, 
    AdminSharesView, AdminUsersView, admin_dashboard_stats,
    bulk_approve_applications, bulk_approve_payments
)

urlpatterns = [
    path('applications/', AdminApplicationsView.as_view(), name='admin-applications'),
    path('payments/', AdminPaymentsView.as_view(), name='admin-payments'),
    path('claims/', AdminClaimsView.as_view(), name='admin-claims'),
    path('shares/', AdminSharesView.as_view(), name='admin-shares'),
    path('users/', AdminUsersView.as_view(), name='admin-users'),
    path('dashboard-stats/', admin_dashboard_stats, name='admin-dashboard-stats'),
    path('bulk-approve-applications/', bulk_approve_applications, name='bulk-approve-applications'),
    path('bulk-approve-payments/', bulk_approve_payments, name='bulk-approve-payments'),
]
"""

print("COMPLETE URL CONFIGURATION")
print("Copy each section to the respective files")
print("All endpoints will be available at:")
print("- /api/auth/ - Authentication endpoints")
print("- /api/applications/ - Application management")
print("- /api/payments/ - Payment management")
print("- /api/claims/ - Claims management")
print("- /api/shares/ - Share management")
print("- /api/admin/ - Admin panel endpoints")