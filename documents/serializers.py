from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    file_url = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
    
    def get_file_type(self, obj):
        if obj.file:
            name = obj.file.name.lower()
            if name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                return 'image'
            elif name.endswith('.pdf'):
                return 'pdf'
            else:
                return 'document'
        return None