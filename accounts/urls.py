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