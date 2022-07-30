"""Models for accounts application"""


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from model_utils import Choices
from tickets.models import Team


# CREDIT: Adapted from Pyplane and Django Documentation
# URL: https://www.youtube.com/watch?v=1BeZxMbSZNI
class CustomUser(AbstractUser):
    """Custom user model created by extending AbstractUser

    User accounts have the additional fields:
        Role - Choice between "administrator", "technician" or "customer"
        Team - Foreign key relationship to tickets.models.Team
    """

    ROLES = Choices(
        ("administrator", ("Administrator")),
        ("technician", ("Technician")),
        ("customer", ("Customer")),
    )

    role = models.CharField(
        max_length=13,
        choices=ROLES,
        default=ROLES.customer,
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="team",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.pk})
