from rest_framework import serializers
from .models import Beneficiary

class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = ['id', 'name', 'phone', 'email', 'user']
        read_only_fields = ('user',)