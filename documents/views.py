from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import Document
from .serializers import DocumentSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Document.objects.all()
        return Document.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                document = serializer.save(user=request.user)
                
                # Send notification to admin
                send_mail(
                    subject=f'New Document Uploaded - {request.user.username}',
                    message=f'''
                    New document uploaded:
                    
                    User: {request.user.get_full_name()}
                    Email: {request.user.email}
                    Document: {document.name}
                    Type: {document.document_type}
                    Date: {document.created_at}
                    
                    Please review in admin panel.
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['pamojakeny@gmail.com'],
                    fail_silently=True,
                )
                
                return Response(DocumentSerializer(document).data, status=201)
            return Response({'message': 'Invalid document data'}, status=400)
        except Exception as e:
            return Response({'message': str(e)}, status=400)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        document = self.get_object()
        document.status = 'approved'
        document.admin_notes = request.data.get('admin_notes', '')
        document.save()
        return Response({'status': 'approved'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        document = self.get_object()
        document.status = 'rejected'
        document.admin_notes = request.data.get('admin_notes', '')
        document.save()
        return Response({'status': 'rejected'})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_public_documents(request):
    """Get all public documents for frontend"""
    documents = Document.objects.all().order_by('document_type', 'name')
    documents_data = [{
        'id': doc.id,
        'name': doc.name,
        'description': getattr(doc, 'description', ''),
        'document_type': doc.document_type,
        'file_url': doc.file.url if doc.file else None,
        'created_at': doc.created_at.isoformat(),
    } for doc in documents]
    
    return JsonResponse({'documents': documents_data})