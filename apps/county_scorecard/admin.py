from django.contrib import admin
from .models import CountyScorecard, ScorecardHistory

@admin.register(CountyScorecard)
class ScorecardAdmin(admin.ModelAdmin):
    list_display = ('county', 'overall_score', 'rank', 'updated_at')
    
@admin.register(ScorecardHistory)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('county', 'snapshot_date')
