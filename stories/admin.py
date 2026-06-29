from django.contrib import admin
from .models import Story

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_approved', 'is_anonymous', 'created_at')
    list_filter = ('category', 'is_approved', 'is_anonymous')
    search_fields = ('title', 'content')
    actions = ['approve_stories']

    def approve_stories(self, request, queryset):
        queryset.update(is_approved=True)
