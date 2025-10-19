from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    payment_type_display = serializers.CharField(source='get_payment_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_proof_url = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'

    def get_payment_proof_url(self, obj):
        if obj.payment_proof:
            return obj.payment_proof.url
        return None

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['payment_type', 'amount', 'description', 'payment_method', 
                 'transaction_id', 'payment_proof', 'reference_number']
    
    def validate(self, data):
        # Ensure required fields are present
        if not data.get('payment_type'):
            raise serializers.ValidationError({'payment_type': 'This field is required.'})
        
        if not data.get('amount'):
            raise serializers.ValidationError({'amount': 'This field is required.'})
            
        # Set default payment_method if not provided
        if not data.get('payment_method'):
            data['payment_method'] = 'bank'
            
        return data