from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN           = "admin",           "Admin"
        COUNTY_OFFICIAL = "county_official", "County Official"
        ORG_STAFF       = "org_staff",       "Organisation Staff"
        SURVIVOR        = "survivor",        "Registered Survivor"
        PUBLIC          = "public",          "Public"

    role   = models.CharField(max_length=20, choices=Role.choices, default=Role.PUBLIC)
    county = models.CharField(max_length=100, blank=True)

    def is_org_staff(self):
        return self.role == self.Role.ORG_STAFF

    def is_county_official(self):
        return self.role == self.Role.COUNTY_OFFICIAL

    def is_platform_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def is_survivor(self):
        return self.role == self.Role.SURVIVOR

    def __str__(self):
        return self.username
