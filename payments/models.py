from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

PAYMENT_TYPES = [
    ('activation_fee', 'Activation Fee'),
    ('membership_single', 'Single Membership Fee'),
    ('membership_double', 'Double Membership Fee'),
    ('shares', 'Share Purchase'),
    ('share_purchase', 'Share Purchase'),
    ('membership_fee', 'Membership Fee'),
    ('claim_payout', 'Claim Payout'),
    ('share_deduction', 'Share Deduction'),
    ('other', 'Other Payment'),
]

PAYMENT_STATUS = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
]

PAYMENT_METHODS = [
    ('paypal', 'PayPal'),
    ('mpesa', 'M-Pesa'),
    ('bank', 'Bank Transfer'),
    ('system', 'System Transaction'),
]

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    reference_number = models.CharField(max_length=100, blank=True)
    
    # Required fields
    payment_proof = models.FileField(upload_to='payments/', blank=True, null=True)  # Required but allow blank for now
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, blank=True)  # Required but allow blank for now
    transaction_id = models.CharField(max_length=100, blank=True)  # Optional
    
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    admin_notes = models.TextField(blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_payments')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Auto-update shares if payment is for shares and approved
        if self.status in ['completed', 'approved'] and self.payment_type == 'shares':
            shares_to_add = int(self.amount // 25)  # $25 per share
            self.user.shares_owned += shares_to_add
            self.user.shares += shares_to_add
            self.user.save()
    
    def __str__(self):
        return f"{self.user.username} - {self.get_payment_type_display()} - ${self.amount}"
    
    class Meta:
        ordering = ['-created_at']