from django.contrib import admin
from .models import Workshop, WorkshopAttendance

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'workshop_type', 'is_live', 'scheduled_start', 'scheduled_end')
    list_filter = ('workshop_type', 'is_live')

@admin.register(WorkshopAttendance)
class WorkshopAttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'workshop', 'attended_at', 'feedback_rating')
