from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .profile import UserProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "email", "role", "county", "is_staff"]
    list_filter  = ["role", "is_staff"]
    fieldsets    = BaseUserAdmin.fieldsets + (
        ("AmakaziWatch", {"fields": ("role", "county")}),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "county", "created_at"]
