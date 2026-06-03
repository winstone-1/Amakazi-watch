from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user             = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    county           = models.CharField(max_length=100, blank=True)
    bio              = models.TextField(blank=True)
    avatar_url       = models.URLField(blank=True)
    bookmarked_orgs  = models.ManyToManyField("organisations.Organisation", blank=True, related_name="bookmarked_by")
    case_refs        = models.JSONField(default=list, help_text="List of case reference codes submitted by this user")
    created_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile — {self.user.username}"
