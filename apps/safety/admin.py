from django.contrib import admin
from .models import SafetyTimer, SafeWord, RiskAssessment, EscapePlan

@admin.register(SafetyTimer)
class SafetyTimerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'duration_minutes', 'status', 'start_time')
    list_filter = ('status',)
    search_fields = ('user__username',)

@admin.register(SafeWord)
class SafeWordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code_word', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('user__username',)

@admin.register(RiskAssessment)
class RiskAssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'score', 'risk_level', 'created_at')
    list_filter = ('risk_level',)

@admin.register(EscapePlan)
class EscapePlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
