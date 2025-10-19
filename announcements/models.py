from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Announcement(models.Model):
    PRIORITY_CHOICES = [('high', 'High'), ('medium', 'Medium'), ('low', 'Low')]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_pinned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title