from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN     = 'admin',     'Admin'
        ORG_STAFF = 'org_staff', 'Organisation Staff'
        PUBLIC    = 'public',    'Public'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PUBLIC
    )

    def is_org_staff(self):
        return self.role == self.Role.ORG_STAFF

    def is_platform_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def __str__(self):
        return self.username
