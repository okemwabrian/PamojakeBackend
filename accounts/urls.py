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
    path('user/', views.get_user, name='get_user'),  # Simple user endpoint
    path('profile/', views.user_profile, name='user_profile'),  # Full profile endpoint
    path('user-status/', views.user_status, name='user_status'),
    path('test/', views.test_endpoint, name='test_endpoint'),
    path('change-password/', views.change_password, name='change_password'),
    path('dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
    
    # User data endpoints
    path('claims/', views.get_user_claims, name='get_user_claims'),
    path('shares/', views.get_user_shares, name='get_user_shares'),
    
    path('', include(router.urls)),
]