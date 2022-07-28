from django import forms
from .models import Ticket, Comment
from django_summernote.fields import SummernoteWidget
from crispy_forms.helper import FormHelper
from accounts.models import CustomUser


# Ticket Update Form for Customer
#
# This Form provides the least amount of fields from the ticket model and form
# the base all other ticket forms will inherit from
class CustomerTicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = (
            "category",
            "description",
            "ticket_image",
        )

        widgets = {
            "description": SummernoteWidget(),
        }


# Ticket Creation Form for Customer
#
# This Form inherits from the Customer Ticket Update Form, adding additional
# fields and altering the order they are displayed
class CustomerTicketCreationForm(CustomerTicketUpdateForm, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerTicketCreationForm, self).__init__(*args, **kwargs)

    class Meta(CustomerTicketUpdateForm):
        model = Ticket
        fields = CustomerTicketUpdateForm.Meta.fields + (
            "type",
            "title",
        )

        widgets = {
            "description": SummernoteWidget(),
        }

    field_order = [
        "type",
        "category",
        "title",
        CustomerTicketUpdateForm.Meta.fields,
    ]


# Ticket Creation and Update Form for Users with Elevated Role
#
# This Form inherits from the Customer Ticket Creation Form, adding additional
# fields and altering the order they are displayed
class ElevatedUserTicketForm(CustomerTicketCreationForm, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ElevatedUserTicketForm, self).__init__(*args, **kwargs)
        self.fields[
            "assigned_technician"
        ].queryset = CustomUser.objects.filter(role="technician")

    class Meta(CustomerTicketCreationForm):
        model = Ticket
        fields = CustomerTicketCreationForm.Meta.fields + (
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
    ] + CustomerTicketCreationForm.field_order


# Comment Form for use in Ticket View
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)

        widgets = {
            "body": SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["body"].label = "Leave a comment:"
        self.helper = FormHelper
        self.helper.form_method = "post"
