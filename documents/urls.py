from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, get_public_documents

router = DefaultRouter()
router.register(r'', DocumentViewSet, basename='document')

urlpatterns = [
    path('public/', get_public_documents, name='public-documents'),
    path('', include(router.urls)),
]