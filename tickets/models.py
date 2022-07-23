from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.html import strip_tags
from model_utils import Choices
from datetime import datetime, timezone

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
        ("inprogress", ("In Progress")),
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
    ticket_image = models.ImageField(
        blank=True,
    )
    status = models.CharField(
        max_length=10,
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

    class Meta:
        ordering = ("-updated_on",)

    def __str__(self):
        return f"Request #: {self.id} - {self.title}"

    # CREDIT: CodingEntrepreneurs - Python & Django 3.2 Tutorial Series
    # Video 44 (get absolute url) & 45 (Django URLs Reverse)
    # URL: 44 - https://www.youtube.com/watch?v=b42B-xli-vQ
    # URL: 45 - https://www.youtube.com/watch?v=rm2YTMc2s10
    def get_absolute_url(self):
        return reverse("ticket_detail", kwargs={"pk": self.pk})

    # Property of the ticket model to be used in the template and to set the
    # tickets updated time
    @property
    def get_time_now(self):
        return datetime.now(timezone.utc)

    # Function to set the tickets updated_on field to the current time when
    # called
    def set_ticket_updated_now(self):
        self.updated_on = self.get_time_now
        self.save(update_fields=["updated_on"])


class Note(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="notes"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="note_author",
        null=True,
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    # Remove HTML tags in for note body. For use in the admin panel
    # CREDIT: arie - Stack Overflow
    # URL: https://stackoverflow.com/a/9294835
    @property
    def body_without_tags(self):
        return strip_tags(self.body)
