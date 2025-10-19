from django.contrib import admin
from .models import Meeting, MeetingRegistration

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'type', 'require_registration', 'created_by', 'created_at']
    list_filter = ['type', 'require_registration', 'date']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(MeetingRegistration)
class MeetingRegistrationAdmin(admin.ModelAdmin):
    list_display = ['meeting', 'user', 'registered_at']
    list_filter = ['registered_at']
    search_fields = ['meeting__title', 'user__username']