from rest_framework import serializers
from .models import Announcement

class AnnouncementSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ('author', 'created_at', 'updated_at')