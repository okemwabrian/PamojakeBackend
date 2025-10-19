from rest_framework import serializers
from .models import Claim

class ClaimSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Claim
        fields = ['id', 'user', 'user_name', 'claim_type', 'member_name', 'relationship', 'amount_requested', 'amount_approved', 'incident_date', 'description', 'supporting_documents', 'status', 'admin_notes', 'created_at']
        read_only_fields = ('user', 'status', 'admin_notes', 'created_at', 'amount_approved')
    
    def validate_amount_requested(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value
    
    def validate_incident_date(self, value):
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("Incident date cannot be in the future")
        return value