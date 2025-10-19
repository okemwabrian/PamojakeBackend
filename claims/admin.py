from django.contrib import admin
from .models import Claim

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('user', 'claim_type', 'member_name', 'amount_requested', 'amount_approved', 'status', 'incident_date', 'created_at')
    list_filter = ('claim_type', 'status', 'incident_date', 'created_at')
    search_fields = ('member_name', 'user__username', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status', 'amount_approved')
    fieldsets = (
        ('Claim Info', {
            'fields': ('user', 'claim_type', 'member_name', 'relationship', 'incident_date')
        }),
        ('Amounts', {
            'fields': ('amount_requested', 'amount_approved')
        }),
        ('Details', {
            'fields': ('description', 'status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        })
    )
