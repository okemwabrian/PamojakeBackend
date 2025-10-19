from rest_framework import serializers
from .models import Meeting, MeetingRegistration

class MeetingSerializer(serializers.ModelSerializer):
    registered = serializers.SerializerMethodField()
    registration_count = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = Meeting
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')
    
    def get_registered(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return MeetingRegistration.objects.filter(meeting=obj, user=request.user).exists()
        return False
    
    def get_registration_count(self, obj):
        return MeetingRegistration.objects.filter(meeting=obj).count()
    
    def get_created_by_name(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}" if obj.created_by.first_name else obj.created_by.username
    
    def get_is_expired(self, obj):
        return obj.is_expired if hasattr(obj, 'is_expired') else False