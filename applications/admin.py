from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'status', 'first_name', 'last_name', 'created_at')
    list_filter = ('type', 'status', 'created_at')
    search_fields = ('first_name', 'last_name', 'user__username', 'email')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'type', 'status', 'first_name', 'middle_name', 'last_name', 'email', 'phone_main')
        }),
        ('Address', {
            'fields': ('address_1', 'address_2', 'city', 'state_province', 'zip_postal')
        }),
        ('Family Info', {
            'fields': ('spouse', 'spouse_phone', 'authorized_rep')
        }),
        ('Admin', {
            'fields': ('admin_notes', 'created_at', 'updated_at')
        })
    )
