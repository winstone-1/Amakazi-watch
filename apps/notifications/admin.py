from django.contrib import admin
from .models import Notification, AuditLog


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["user", "type", "title", "is_read", "created_at"]
    list_filter  = ["type", "is_read"]
    actions      = ["mark_as_read"]

    @admin.action(description="Mark selected as read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display   = ["user", "action", "model_name", "object_id", "ip_address", "created_at"]
    list_filter    = ["model_name"]
    readonly_fields = ["user", "action", "model_name", "object_id", "details", "ip_address", "created_at"]
