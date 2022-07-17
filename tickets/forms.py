from django import forms
from .models import Ticket, Note
from django_summernote.fields import SummernoteWidget
from crispy_forms.helper import FormHelper


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


# Ticket Creation and Update Form for Users with Elevated Role
#
# This Form inherits from the Staff Ticket Creation Form, adding additional
# fields and altering the order they are displayed
class ElevatedUserTicketForm(StaffTicketCreationForm, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ElevatedUserTicketForm, self).__init__(*args, **kwargs)

    class Meta(StaffTicketCreationForm):
        model = Ticket
        fields = StaffTicketCreationForm.Meta.fields + (
            "author",
            "status",
            "priority",
            "assigned_team",
            "assigned_technician",
        )

        widgets = {
            "description": SummernoteWidget(),
        }

    field_order = [
        "author",
        "status",
        "priority",
        "assigned_team",
        "assigned_technician",
        StaffTicketCreationForm.Meta.fields,
    ]


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["body"].label = "Leave a comment:"
        self.helper = FormHelper
        self.helper.form_method = "post"
