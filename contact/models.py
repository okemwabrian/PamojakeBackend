from django.db import models
from django.conf import settings

class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    admin_reply = models.TextField(blank=True)
    replied_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='contact_replies')
    replied_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.name or self.email}"

    class Meta:
        ordering = ['-created_at']