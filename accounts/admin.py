from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_member', 'is_staff', 'is_active', 'membership_date')
    list_filter = ('is_member', 'is_staff', 'is_active', 'membership_date', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    list_editable = ('is_member', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone', 'address', 'city', 'state', 'date_of_birth', 'emergency_contact', 'emergency_phone', 'is_member', 'membership_date')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'first_name', 'last_name', 'phone', 'is_member')
        }),
    )
