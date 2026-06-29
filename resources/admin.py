from django.contrib import admin
from .models import Resource

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_downloadable', 'is_active')
    list_filter = ('category', 'is_downloadable', 'is_active')
    search_fields = ('title', 'description')
