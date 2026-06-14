from django.contrib import admin
from .models import AwarenessCampaign

@admin.register(AwarenessCampaign)
class AwarenessCampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'organisation', 'title', 'status', 'scheduled_for', 'sent_at')
    list_filter = ('status', 'channels')
