from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ('application_submitted', 'Application Submitted'),
        ('payment_made', 'Payment Made'),
        ('claim_submitted', 'Claim Submitted'),
        ('shares_purchased', 'Shares Purchased'),
        ('document_uploaded', 'Document Uploaded'),
        ('profile_updated', 'Profile Updated'),
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('application_updated', 'Application Updated'),
        ('payment_updated', 'Payment Updated'),
        ('claim_updated', 'Claim Updated'),
        ('application_deleted', 'Application Deleted'),
        ('payment_deleted', 'Payment Deleted'),
        ('claim_deleted', 'Claim Deleted'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.created_at}"