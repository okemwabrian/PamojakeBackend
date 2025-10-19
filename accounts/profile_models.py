from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_activated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {'Activated' if self.is_activated else 'Not Activated'}"