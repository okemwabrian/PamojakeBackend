from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Announcement
from .serializers import AnnouncementSerializer

User = get_user_model()

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.filter(is_active=True)
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def announcements_list(request):
    if request.method == 'GET':
        announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')
        data = [{
            'id': announcement.id,
            'title': announcement.title,
            'content': announcement.content,
            'priority': announcement.priority,
            'author': announcement.author.username,
            'created_at': announcement.created_at.isoformat(),
            'is_pinned': announcement.is_pinned,
        } for announcement in announcements]
        
        return Response({'announcements': data})
    
    elif request.method == 'POST':
        if not request.user.is_staff:
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        title = request.data.get('title')
        content = request.data.get('content')
        
        if not title or not content:
            return Response({
                'error': 'Title and content are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            announcement = Announcement.objects.create(
                title=title,
                content=content,
                priority=request.data.get('priority', 'medium'),
                author=request.user,
                is_pinned=request.data.get('is_pinned', False),
            )
            
            return Response({
                'success': True,
                'message': 'Announcement created successfully',
                'announcement': {
                    'id': announcement.id,
                    'title': announcement.title,
                    'content': announcement.content,
                    'priority': announcement.priority,
                    'created_at': announcement.created_at.isoformat(),
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': f'Failed to create announcement: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def announcement_detail(request, announcement_id):
    try:
        announcement = Announcement.objects.get(id=announcement_id)
    except Announcement.DoesNotExist:
        return Response({'error': 'Announcement not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return Response({
            'announcement': {
                'id': announcement.id,
                'title': announcement.title,
                'content': announcement.content,
                'priority': announcement.priority,
                'is_active': announcement.is_active,
                'is_pinned': announcement.is_pinned,
                'author': announcement.author.username,
                'created_at': announcement.created_at.isoformat(),
                'updated_at': announcement.updated_at.isoformat(),
            }
        })
    
    elif request.method == 'PUT':
        if not request.user.is_staff:
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            if 'title' in request.data:
                announcement.title = request.data['title']
            if 'content' in request.data:
                announcement.content = request.data['content']
            if 'priority' in request.data:
                announcement.priority = request.data['priority']
            if 'is_active' in request.data:
                announcement.is_active = request.data['is_active']
            if 'is_pinned' in request.data:
                announcement.is_pinned = request.data['is_pinned']
            
            announcement.save()
            
            return Response({
                'success': True,
                'message': 'Announcement updated successfully'
            })
            
        except Exception as e:
            return Response({
                'error': f'Failed to update announcement: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if not request.user.is_staff:
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        announcement.delete()
        return Response({
            'success': True,
            'message': 'Announcement deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)