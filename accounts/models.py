from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, default='MN')
    date_of_birth = models.DateField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=200, blank=True)
    emergency_phone = models.CharField(max_length=15, blank=True)
    is_member = models.BooleanField(default=False)
    membership_date = models.DateTimeField(null=True, blank=True)
    shares_owned = models.IntegerField(default=0)
    available_shares = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)  # Alias for shares_owned

    # Critical activation fields
    is_activated = models.BooleanField(default=False)
    is_active_member = models.BooleanField(default=False)
    activation_date = models.DateTimeField(null=True, blank=True)
    activated_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    
    # Membership type
    membership_type = models.CharField(max_length=20, choices=[
        ('single', 'Single Membership'),
        ('double', 'Double Membership')
    ], blank=True, null=True)
    
    # Additional registration details
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    deactivation_reason = models.TextField(blank=True)
    profile_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Set users inactive by default on creation
        if not self.pk and not self.is_superuser:
            self.is_active = False
            self.is_activated = False
        
        # Sync shares fields - use the higher value
        if self.shares > self.shares_owned:
            self.shares_owned = self.shares
        elif self.shares_owned > self.shares:
            self.shares = self.shares_owned
        
        # Auto-activate if shares >= 20
        if self.shares >= 20 and not self.is_active_member:
            self.is_active_member = True
            self.is_activated = True
            self.activation_date = timezone.now()
            self.deactivation_reason = ''
        elif self.shares < 20:
            self.is_active_member = False

        super().save(*args, **kwargs)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    is_activated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {'Activated' if self.is_activated else 'Not Activated'}"