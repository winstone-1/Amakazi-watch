from django.contrib import admin
from .models import EducationContent, Quiz

@admin.register(EducationContent)
class EducationContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'format', 'topic', 'organisation', 'approved', 'created_at']
    list_filter  = ['format', 'topic', 'approved']
    actions      = ['approve_content']

    @admin.action(description='Approve selected content')
    def approve_content(self, request, queryset):
        queryset.update(approved=True)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'organisation', 'approved', 'completion_count']
    list_filter  = ['approved', 'topic']
