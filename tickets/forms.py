from django import forms
from .models import Ticket


# Ticket Creation Form for Staff
class StaffTicketCreationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = (
            "type",
            "category",
            "title",
            "description",
            "ticket_image",
        )
