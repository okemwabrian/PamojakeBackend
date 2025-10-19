from rest_framework import serializers
from .models import ShareTransaction, SharePurchase

class ShareTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareTransaction
        fields = '__all__'
        read_only_fields = ('user', 'transaction_id', 'created_at', 'updated_at')
    
    def validate_buyer_name(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Buyer name is required and must be at least 2 characters")
        return value.strip()

class SharePurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharePurchase
        fields = ['id', 'quantity', 'amount_per_share', 'total_amount', 'payment_proof',
                 'buyer_name', 'payment_method', 'status', 'created_at']
        read_only_fields = ['id', 'buyer_name', 'amount_per_share', 'total_amount', 
                           'status', 'created_at']
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value