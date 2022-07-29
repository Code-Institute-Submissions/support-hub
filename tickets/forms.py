"""Forms for tickets application"""


from django import forms
from django_summernote.fields import SummernoteWidget
from crispy_forms.helper import FormHelper
from accounts.models import CustomUser
from .models import Comment, Ticket


class CustomerTicketUpdateForm(forms.ModelForm):
    """Ticket Update Form used for users with the role of Customer.

    Provides limited fields from the ticket model. All other ticket forms
    inherit from this.
    """

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


class CustomerTicketCreationForm(CustomerTicketUpdateForm, forms.ModelForm):
    """Ticket Creation Form for Customer.

    Form inherits from the Customer Ticket Update Form, exposing more fields
    from the Ticket Model.
    """

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


class ElevatedUserTicketForm(CustomerTicketCreationForm, forms.ModelForm):
    """Ticket Creation and Update Form for users with elevated roles.

    Form inherits from the Customer Ticket Creation Form, exposing more fields
    from the Ticket Model.
    """

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


class CommentForm(forms.ModelForm):
    """Ticket Comment Form for all users."""

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
