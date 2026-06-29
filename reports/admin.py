from django.contrib import admin
from .models import IncidentReport, Report

@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'abuse_type', 'county', 'status', 'created_at')
    list_filter = ('abuse_type', 'status', 'county')
    search_fields = ('description', 'phone')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'abuse_type', 'county', 'status', 'created_at')
    list_filter = ('abuse_type', 'status', 'county')
    search_fields = ('description', 'phone')
