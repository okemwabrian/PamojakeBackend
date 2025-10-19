from rest_framework import serializers
from .models import ContactMessage

class ContactMessageSerializer(serializers.ModelSerializer):
    replied_by_name = serializers.CharField(source='replied_by.get_full_name', read_only=True)
    
    class Meta:
        model = ContactMessage
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'replied_by', 'replied_at')