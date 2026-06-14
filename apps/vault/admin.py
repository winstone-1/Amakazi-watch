from django.contrib import admin
from .models import EvidenceDocument

@admin.register(EvidenceDocument)
class VaultAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file_type', 'uploaded_at')
    list_filter = ('file_type', 'is_court_admissible')
