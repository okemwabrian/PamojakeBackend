from django.db import models
from django.conf import settings

class Document(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    TYPE_CHOICES = [
        ('id', 'Identification'),
        ('proof_income', 'Proof of Income'),
        ('bank_statement', 'Bank Statement'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    document_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='other')
    file = models.FileField(upload_to='documents/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']