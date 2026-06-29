from django.contrib import admin
from .models import Organisation

@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'org_type', 'county', 'is_verified', 'created_at')
    list_filter = ('org_type', 'is_verified', 'county')
    search_fields = ('name', 'email', 'phone')
