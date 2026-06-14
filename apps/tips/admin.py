from django.contrib import admin
from .models import AnonymousTip

@admin.register(AnonymousTip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('id', 'incident_county', 'is_urgent', 'created_at', 'is_reviewed')
    list_filter = ('is_urgent', 'is_reviewed', 'incident_county')
