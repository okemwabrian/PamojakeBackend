from django.contrib import admin
from .models import ShareTransaction

@admin.register(ShareTransaction)
class ShareTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'quantity', 'total_amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['user__username', 'transaction_id', 'buyer_name']
    readonly_fields = ['transaction_id', 'created_at', 'updated_at']