from django.contrib import admin
from .models import PeerSupporter, PeerSupportSession

@admin.register(PeerSupporter)
class PeerSupporterAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_trained', 'current_sessions', 'max_active_sessions')
    list_filter = ('is_trained',)
    search_fields = ('user__username',)

@admin.register(PeerSupportSession)
class PeerSupportSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'survivor', 'supporter', 'status', 'started_at')
    list_filter = ('status', 'is_anonymous')
