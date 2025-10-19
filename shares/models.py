from django.db import models
from django.conf import settings
import uuid

class ShareTransaction(models.Model):
    STATUS_CHOICES = [
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
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    amount_per_share = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_proof = models.FileField(upload_to='share_payments/', null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.total_amount and self.quantity:
            self.total_amount = self.quantity * self.amount_per_share
        super().save(*args, **kwargs)
        # Auto-update shares if approved
        if self.status == 'approved':
            self.user.shares_owned += self.quantity
            self.user.save()

    def __str__(self):
        return f"{self.user.username} - {self.quantity} shares - ${self.total_amount}"

    class Meta:
        ordering = ['-created_at']

# Keep old model for backward compatibility
class SharePurchase(ShareTransaction):
    class Meta:
        proxy = True