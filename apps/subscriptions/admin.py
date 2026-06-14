from django.contrib import admin
from .models import Subscription, SubscriptionPayment


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display  = ["organisation", "plan", "is_active", "expires_at", "auto_renew"]
    list_filter   = ["plan", "is_active"]
    actions       = ["activate_subscriptions", "deactivate_subscriptions"]

    @admin.action(description="Activate selected subscriptions")
    def activate_subscriptions(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        queryset.update(is_active=True, started_at=timezone.now(), expires_at=timezone.now() + timedelta(days=30))

    @admin.action(description="Deactivate selected subscriptions")
    def deactivate_subscriptions(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(SubscriptionPayment)
class SubscriptionPaymentAdmin(admin.ModelAdmin):
    list_display = ["subscription", "amount", "status", "paid_at"]
    list_filter  = ["status"]
