from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_type', 'status', 'payment_method', 'transaction_id', 'created_at')
    list_filter = ('payment_type', 'status', 'payment_method', 'created_at')
    search_fields = ('user__username', 'transaction_id', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    fieldsets = (
        ('Payment Info', {
            'fields': ('user', 'amount', 'payment_type', 'payment_method', 'transaction_id', 'payment_proof')
        }),
        ('Status', {
            'fields': ('status', 'description', 'admin_notes')
        }),
        ('Processing', {
            'fields': ('processed_by', 'processed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        })
    )
