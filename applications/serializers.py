from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    type = serializers.CharField(required=False)  # Make type optional
    id_document = serializers.FileField(required=False)  # Make id_document optional
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = (
            'user', 'status', 'admin_notes', 'created_at', 'updated_at',
            'payment_verified', 'payment_verified_by', 'payment_verified_at',
            'reviewed_by', 'activation_fee_paid'
        )
    
    def validate(self, data):
        # Set default values for required fields that might be missing
        data.setdefault('declaration_accepted', True)
        data.setdefault('constitution_agreed', True)
        data.setdefault('activation_fee_paid', False)
        data.setdefault('payment_verified', False)
        data.setdefault('payment_amount', 0)
        data.setdefault('activation_fee_amount', 50.00)
        
        # Handle membership_type and type field synchronization
        membership_type = data.get('membership_type', 'single')
        data['type'] = membership_type
        data['membership_type'] = membership_type
            
        return data