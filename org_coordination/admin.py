from django.contrib import admin
from .models import ResourceInventory, CaseMatching, InterOrgMessage, Volunteer, HotspotAlert

@admin.register(ResourceInventory)
class ResourceInventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'organisation', 'resource_type', 'available_count', 'total_capacity', 'last_updated')
    list_filter = ('resource_type',)

@admin.register(CaseMatching)
class CaseMatchingAdmin(admin.ModelAdmin):
    list_display = ('id', 'case_ref', 'matched_organisation', 'match_score', 'status', 'created_at')
    list_filter = ('status',)

@admin.register(InterOrgMessage)
class InterOrgMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_org', 'to_org', 'message', 'is_read', 'created_at')
    list_filter = ('is_read',)

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('id', 'organisation', 'user', 'role', 'hours_this_month', 'is_active')
    list_filter = ('is_active', 'role')

@admin.register(HotspotAlert)
class HotspotAlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'county', 'sub_county', 'predicted_risk_score', 'expires_at')
    list_filter = ('county',)
