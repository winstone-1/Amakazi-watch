from django.contrib import admin
from .models import APIKey, APIUsageLog

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'tier', 'requests_this_month', 'monthly_limit', 'is_active')
    list_filter = ('tier', 'is_active')

@admin.register(APIUsageLog)
class APIUsageLogAdmin(admin.ModelAdmin):
    list_display = ('api_key', 'endpoint', 'requests_count', 'timestamp')
    list_filter = ('timestamp',)
