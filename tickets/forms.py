from django import forms
from .models import Ticket, Note
from django_summernote.fields import SummernoteWidget


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

        widgets = {
            "description": SummernoteWidget(),
        }


# Ticket Update Form for Staff
class StaffTicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = (
            "description",
            "ticket_image",
        )

        widgets = {
            "description": SummernoteWidget(),
        }


# Note Form for use in Ticket View
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("body",)

        widgets = {
            "body": SummernoteWidget(),
        }
