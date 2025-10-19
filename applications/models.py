from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Application(models.Model):
    TYPE_CHOICES = [
        ('single', 'Single Family'),
        ('double', 'Double Family')
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('payment_submitted', 'Payment Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)  # Alias for backward compatibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Basic Info
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    confirm_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15)
    phone_main = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    id_number = models.CharField(max_length=20, blank=True)
    
    # Address
    address = models.TextField()  # Main address field
    address_1 = models.CharField(max_length=200, blank=True)  # Backward compatibility
    address_2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default='Minnesota')  # Main state field
    state_province = models.CharField(max_length=50, default='MN', blank=True)  # Backward compatibility
    zip_code = models.CharField(max_length=10)  # Main zip field
    zip_postal = models.CharField(max_length=20, blank=True)  # Backward compatibility
    
    # Emergency Contact
    EMERGENCY_RELATIONSHIP_CHOICES = [
        ('spouse', 'Spouse'),
        ('parent', 'Parent'),
        ('sibling', 'Sibling'),
        ('child', 'Child'),
        ('friend', 'Friend')
    ]
    
    emergency_name = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    emergency_relationship = models.CharField(max_length=50, choices=EMERGENCY_RELATIONSHIP_CHOICES, blank=True)
    
    # Spouse Info (for double membership)
    spouse_first_name = models.CharField(max_length=100, blank=True, null=True)
    spouse_last_name = models.CharField(max_length=100, blank=True, null=True)
    spouse_email = models.EmailField(blank=True, null=True)
    spouse_phone = models.CharField(max_length=15, blank=True)
    spouse_date_of_birth = models.DateField(null=True, blank=True)
    spouse_id_number = models.CharField(max_length=20, blank=True)
    spouse = models.CharField(max_length=200, blank=True)  # Backward compatibility
    authorized_rep = models.CharField(max_length=200, blank=True)
    
    # Children Info
    children_info = models.JSONField(default=list, blank=True)  # List of children details
    
    # Legacy children fields for backward compatibility
    child_1 = models.CharField(max_length=200, blank=True)
    child_2 = models.CharField(max_length=200, blank=True)
    child_3 = models.CharField(max_length=200, blank=True)
    child_4 = models.CharField(max_length=200, blank=True)
    child_5 = models.CharField(max_length=200, blank=True)
    
    # Parents
    parent_1 = models.CharField(max_length=200, blank=True)
    parent_2 = models.CharField(max_length=200, blank=True)
    spouse_parent_1 = models.CharField(max_length=200, blank=True)
    spouse_parent_2 = models.CharField(max_length=200, blank=True)
    
    # Siblings
    sibling_1 = models.CharField(max_length=200, blank=True)
    sibling_2 = models.CharField(max_length=200, blank=True)
    sibling_3 = models.CharField(max_length=200, blank=True)
    
    # Agreements
    declaration_accepted = models.BooleanField(default=False)
    constitution_agreed = models.BooleanField(default=False)
    
    # Documents
    id_document = models.FileField(upload_to='applications/ids/', null=True, blank=True)
    spouse_id_document = models.FileField(upload_to='applications/spouse_ids/', null=True, blank=True)
    payment_proof = models.FileField(upload_to='applications/payments/', null=True, blank=True)
    
    # Legacy fields for backward compatibility
    phone_legacy = models.CharField(max_length=15, blank=True)
    address_legacy = models.TextField(blank=True)
    state_legacy = models.CharField(max_length=50, blank=True)
    
    # Payment Info
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    
    # Legacy activation fee fields
    activation_fee_paid = models.BooleanField(default=False)
    activation_fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=50.00, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)
    payment_verified = models.BooleanField(default=False)
    payment_verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_applications')
    payment_verified_at = models.DateTimeField(null=True, blank=True)
    
    # Admin fields
    admin_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Sync new fields with legacy fields for backward compatibility
        if self.membership_type and not self.type:
            self.type = self.membership_type
        elif self.type and not self.membership_type:
            self.membership_type = self.type
            
        if self.address and not self.address_1:
            self.address_1 = self.address
        elif self.address_1 and not self.address:
            self.address = self.address_1
            
        if self.state and not self.state_province:
            self.state_province = self.state[:50]  # Truncate if needed
        elif self.state_province and not self.state:
            self.state = self.state_province
            
        if self.zip_code and not self.zip_postal:
            self.zip_postal = self.zip_code
        elif self.zip_postal and not self.zip_code:
            self.zip_code = self.zip_postal
            
        # Sync spouse name fields
        if self.spouse_first_name and self.spouse_last_name and not self.spouse:
            self.spouse = f"{self.spouse_first_name} {self.spouse_last_name}"
        elif self.spouse and not (self.spouse_first_name and self.spouse_last_name):
            name_parts = self.spouse.split(' ', 1)
            self.spouse_first_name = name_parts[0] if name_parts else ''
            self.spouse_last_name = name_parts[1] if len(name_parts) > 1 else ''
            
        super().save(*args, **kwargs)
    
    @property
    def phone_number(self):
        return self.phone or self.phone_main or self.phone_legacy

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.membership_type or self.type}"