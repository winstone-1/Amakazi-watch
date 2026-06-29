from django.contrib import admin
from .models import Plan, Subscription, SubscriptionPayment

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    list_filter = ('name', 'is_active')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'plan')

@admin.register(SubscriptionPayment)
class SubscriptionPaymentAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'amount', 'status', 'created_at')
    list_filter = ('status',)
