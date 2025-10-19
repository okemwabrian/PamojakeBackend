from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Meeting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    duration_minutes = models.IntegerField(default=60)
    auto_expire = models.BooleanField(default=True)
    type = models.CharField(max_length=20, choices=[('virtual', 'Virtual'), ('in_person', 'In Person')], default='virtual')
    max_participants = models.IntegerField(null=True, blank=True)
    require_registration = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def is_expired(self):
        if self.auto_expire:
            end_time = self.date + timedelta(minutes=self.duration_minutes)
            return timezone.now() > end_time
        return False

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['date']

class MeetingRegistration(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['meeting', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.meeting.title}"