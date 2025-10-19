from rest_framework import serializers
from .models import Application
import os

class SingleFamilyApplicationSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name')
    middleName = serializers.CharField(source='middle_name', required=False, allow_blank=True)
    lastName = serializers.CharField(source='last_name')
    phoneMain = serializers.CharField(source='phone_main', required=False, allow_blank=True)
    address1 = serializers.CharField(source='address_1')
    stateProvince = serializers.CharField(source='state_province', default='MN')
    zip = serializers.CharField(source='zip_postal')
    spousePhone = serializers.CharField(source='spouse_phone', required=False, allow_blank=True)
    authorizedRep = serializers.CharField(source='authorized_rep', required=False, allow_blank=True)
    child1 = serializers.CharField(source='child_1', required=False, allow_blank=True)
    child2 = serializers.CharField(source='child_2', required=False, allow_blank=True)
    child3 = serializers.CharField(source='child_3', required=False, allow_blank=True)
    child4 = serializers.CharField(source='child_4', required=False, allow_blank=True)
    child5 = serializers.CharField(source='child_5', required=False, allow_blank=True)
    parent1 = serializers.CharField(source='parent_1', required=False, allow_blank=True)
    parent2 = serializers.CharField(source='parent_2', required=False, allow_blank=True)
    spouseParent1 = serializers.CharField(source='spouse_parent_1', required=False, allow_blank=True)
    spouseParent2 = serializers.CharField(source='spouse_parent_2', required=False, allow_blank=True)
    sibling1 = serializers.CharField(source='sibling_1', required=False, allow_blank=True)
    sibling2 = serializers.CharField(source='sibling_2', required=False, allow_blank=True)
    declarationAccepted = serializers.BooleanField(source='declaration_accepted', required=False)
    id_document_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Application
        fields = ['id', 'firstName', 'middleName', 'lastName', 'email', 'phoneMain', 'address1', 'city', 
                 'stateProvince', 'zip', 'spouse', 'spousePhone', 'authorizedRep', 'child1', 'child2', 
                 'child3', 'child4', 'child5', 'parent1', 'parent2', 'spouseParent1', 'spouseParent2', 
                 'sibling1', 'sibling2', 'declarationAccepted', 'id_document', 'id_document_url', 
                 'status', 'admin_notes', 'created_at', 'user']
        read_only_fields = ('id', 'status', 'admin_notes', 'created_at', 'user')
    
    def get_id_document_url(self, obj):
        if obj.id_document:
            return obj.id_document.url
        return None
    
    def validate_id_document(self, value):
        if value:
            # Check file size (5MB max)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("File size cannot exceed 5MB")
            
            # Check file type
            ext = os.path.splitext(value.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.pdf']:
                raise serializers.ValidationError("Only JPG, PNG, and PDF files are allowed")
        
        return value
    
    def validate(self, attrs):
        user = self.context['request'].user
        # Check if user already has a pending application
        if Application.objects.filter(user=user, status='pending').exists():
            raise serializers.ValidationError("You already have a pending application")
        return attrs
    
    def create(self, validated_data):
        validated_data['type'] = 'single'
        return super().create(validated_data)

class DoubleFamilyApplicationSerializer(serializers.ModelSerializer):
    confirm_email = serializers.EmailField()
    spouse_name = serializers.CharField(source='spouse', required=False, allow_blank=True)
    id_document_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Application
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'email', 'confirm_email', 'phone', 
                 'address_1', 'address_2', 'city', 'state_province', 'zip_postal', 'spouse_name', 
                 'spouse_phone', 'authorized_rep', 'child_1', 'child_2', 'child_3', 'child_4', 
                 'child_5', 'parent_1', 'parent_2', 'spouse_parent_1', 'spouse_parent_2', 
                 'sibling_1', 'sibling_2', 'sibling_3', 'constitution_agreed', 'id_document', 
                 'id_document_url', 'status', 'admin_notes', 'created_at', 'user']
        read_only_fields = ('id', 'status', 'admin_notes', 'created_at', 'user')
    
    def get_id_document_url(self, obj):
        if obj.id_document:
            return obj.id_document.url
        return None
    
    def validate_id_document(self, value):
        if value:
            # Check file size (5MB max)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("File size cannot exceed 5MB")
            
            # Check file type
            ext = os.path.splitext(value.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.pdf']:
                raise serializers.ValidationError("Only JPG, PNG, and PDF files are allowed")
        
        return value
    
    def validate(self, attrs):
        if attrs['email'] != attrs['confirm_email']:
            raise serializers.ValidationError("Email addresses must match exactly")
        
        user = self.context['request'].user
        # Check if user already has a pending application
        if Application.objects.filter(user=user, status='pending').exists():
            raise serializers.ValidationError("You already have a pending application")
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_email')
        validated_data['type'] = 'double'
        return super().create(validated_data)