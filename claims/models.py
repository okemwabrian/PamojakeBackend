from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Claim(models.Model):
    TYPE_CHOICES = [
        ('death', 'Death Benefit'),
        ('medical', 'Medical Emergency'),
        ('education', 'Education Support'),
        ('emergency', 'Emergency Assistance')
    ]
    
    RELATIONSHIP_CHOICES = [
        ('self', 'Self'),
        ('spouse', 'Spouse'),
        ('child', 'Child'),
        ('parent', 'Parent'),
        ('sibling', 'Sibling')
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    claim_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    member_name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES)
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    amount_approved = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    incident_date = models.DateField()
    description = models.TextField()
    supporting_documents = models.FileField(upload_to='claims/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.claim_type} - {self.member_name}"