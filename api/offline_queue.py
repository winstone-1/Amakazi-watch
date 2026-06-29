class OfflineReportQueue(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    report_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    synced_at = models.DateTimeField(null=True)
    device_id = models.CharField(max_length=255)

# Endpoint: POST /api/offline/reports/queue/
# Mobile app can store reports offline, sync when online
