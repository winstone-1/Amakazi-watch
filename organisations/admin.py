from django.contrib import admin
from .models import Organisation, Donation

@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ['name', 'county', 'verified', 'created_at']
    list_filter  = ['verified', 'county']
    actions      = ['verify_organisations']

    @admin.action(description='Mark selected as verified')
    def verify_organisations(self, request, queryset):
        queryset.update(verified=True)

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['organisation', 'amount', 'status', 'created_at']
    list_filter  = ['status']
