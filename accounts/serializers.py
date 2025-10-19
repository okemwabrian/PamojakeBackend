from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'phone', 
                 'address', 'city', 'state', 'date_of_birth', 'emergency_contact', 
                 'emergency_phone', 'is_member', 'membership_date', 'is_staff', 
                 'is_active', 'is_activated', 'activation_date', 'date_joined', 'shares_owned', 'available_shares', 
                 'deactivation_reason', 'profile_completed')
        read_only_fields = ('id', 'date_joined', 'is_activated', 'activation_date')
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'phone', 'address', 'city', 'state', 'date_of_birth', 'emergency_contact', 'emergency_phone']
        extra_kwargs = {
            'password': {'write_only': True},
            'phone': {'required': False},
            'address': {'required': False},
            'city': {'required': False},
            'state': {'required': False},
            'date_of_birth': {'required': False},
            'emergency_contact': {'required': False},
            'emergency_phone': {'required': False}
        }
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('A user with this username already exists.')
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', ''),
            city=validated_data.get('city', ''),
            state=validated_data.get('state', ''),
            date_of_birth=validated_data.get('date_of_birth'),
            emergency_contact=validated_data.get('emergency_contact', ''),
            emergency_phone=validated_data.get('emergency_phone', ''),
            is_active=False  # Users inactive by default, require admin activation
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Check if user exists
            try:
                user_exists = User.objects.get(username=username)
            except User.DoesNotExist:
                raise serializers.ValidationError('Invalid username or password')
            
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid username or password')
            # Allow login for registered users, but limit access based on activation status
            # if not user.is_active:
            #     raise serializers.ValidationError('Account is inactive. Please wait for admin activation or contact support.')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Username and password are required')