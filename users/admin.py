from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'role', 'county', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('phone', 'county', 'bio', 'role')}),
    )
