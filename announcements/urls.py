from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'viewset', views.AnnouncementViewSet, basename='announcement')

urlpatterns = [
    path('', views.announcements_list, name='announcements_list'),
    path('<int:announcement_id>/', views.announcement_detail, name='announcement_detail'),
    path('', include(router.urls)),
]