from django.contrib import admin
from .models import LegalQuery, KenyanLawReference

@admin.register(LegalQuery)
class LegalQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_id', 'question', 'created_at')
    search_fields = ('question', 'answer')

@admin.register(KenyanLawReference)
class KenyanLawReferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'law_name', 'section', 'summary')
    search_fields = ('law_name', 'keywords')
