from django.contrib import admin
from .models import IncidentReport

@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display  = ['sms_ref_code', 'abuse_type', 'county', 'urgency_score', 'flagged_for_review', 'created_at']
    list_filter   = ['abuse_type', 'county', 'flagged_for_review']
    readonly_fields = ['id', 'sms_ref_code', 'created_at']
