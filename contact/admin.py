from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'email', 'phone', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['subject', 'name', 'email', 'message']
    readonly_fields = ['created_at']
    list_editable = ['status']
    fieldsets = (
        ('Contact Info', {
            'fields': ('user', 'name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message', 'status')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        })
    )