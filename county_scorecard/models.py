from django.db import models

class CountyScorecard(models.Model):
    county = models.CharField(max_length=50, unique=True)
    reporting_rate = models.FloatField()
    conviction_rate = models.FloatField()
    org_density = models.FloatField()
    avg_response_time_hours = models.FloatField()
    shelter_capacity_ratio = models.FloatField()
    overall_score = models.FloatField()
    rank = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    
class ScorecardHistory(models.Model):
    county = models.CharField(max_length=50)
    scorecard_data = models.JSONField()
    snapshot_date = models.DateField(auto_now_add=True)