from django.db import models
from django.conf import settings
from model_utils import Choices


# Model to represent the Team tickets and users can be assigned
class Team(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


# Model to represent Categories that can be assigned to tickets to help
# sort them
class TicketCategory(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


# Model to represent Support Tickets that can be raised by users
class Ticket(models.Model):

    STATUS = Choices(
        ("open", ("Open")),
        ("onhold", ("On Hold")),
        ("closed", ("Closed")),
    )

    TYPE = Choices(
        ("request", ("Request")),
        ("incident", ("Incident")),
    )

    PRIORITY = Choices(
        ("low", ("Low")),
        ("medium", ("Medium")),
        ("high", ("High")),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ticket_author",
    )
    title = models.CharField(max_length=50, unique=False, blank=False)
    description = models.TextField()
    status = models.CharField(
        max_length=6,
        choices=STATUS,
        default=STATUS.open,
    )
    type = models.CharField(
        max_length=8,
        choices=TYPE,
        default=TYPE.request,
    )
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY,
        default=PRIORITY.low,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        TicketCategory,
        on_delete=models.SET_NULL,
        related_name="ticket_category",
        blank=True,
        null=True,
    )
    assigned_team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="assigned_team",
        blank=True,
        null=True,
    )
    assigned_technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="assigned_technician",
        blank=True,
        null=True,
    )
