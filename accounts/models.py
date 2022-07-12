from django.db import models
from django.contrib.auth.models import AbstractUser
from model_utils import Choices


# Create custom user model by extending AbstractUser
# CREDIT: Adapted from Pyplane and Django Documentation
# URL: https://www.youtube.com/watch?v=1BeZxMbSZNI
class CustomUser(AbstractUser):

    ROLES = Choices(
        ("administrator", ("Administrator")),
        ("technician", ("Technician")),
        ("staff", ("Staff")),
    )

    role = models.CharField(
        max_length=13,
        choices=ROLES,
        default=ROLES.staff,
    )

    def __str__(self):
        return self.username
