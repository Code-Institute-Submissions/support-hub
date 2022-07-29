"""Filters for tickets application"""


import django_filters
from .models import Ticket


# CREDIT: Filtering adapted from The Dumbfounds: Django Filtering System with
#         django-filter
# URL:    https://www.youtube.com/watch?v=nle3u6Ww6Xk
class CustomerTicketFilter(django_filters.FilterSet):
    """FilterSet to be presented to users with the customer role."""

    STATUS_FILTERING_CHOICES = (
        ("open", "All Open Requests"),
        ("closed", "Closed"),
    )

    DATE_ORDERING_CHOICES = (
        ("descending_created_on", "Creation Date - Descending"),
        ("ascending_created_on", "Creation Date - Ascending"),
        ("descending_updated_on", "Updated Date - Descending"),
        ("ascending_updated_on", "Updated Date - Ascending"),
    )

    # filter_by_status form field. Set the field label, choices to be
    # presented to the user and the filter method to be used
    filter_by_status = django_filters.ChoiceFilter(
        label="Status",
        choices=STATUS_FILTERING_CHOICES,
        method="get_queryset_from_status",
    )

    # order_by_creation_date form field. Set the field label, choices
    # to be presented to the user and the filter method to be used
    order_by_creation_date = django_filters.ChoiceFilter(
        label="Sort by creation date",
        choices=DATE_ORDERING_CHOICES,
        method="get_queryset_from_ordering",
    )

    class Meta:
        model = Ticket
        fields = (
            "filter_by_status",
            "order_by_creation_date",
        )

    def get_queryset_from_status(self, queryset, name, value):
        """Return queryset based on value param from STATUS_FILTERING_CHOICES.

        Args:
            queryset (QuerySet): Current queryset based on applied filters
            name (str): Form field name
            value (str): Selected value from STATUS_FILTERING_CHOICES

        Returns:
            QuerySet: Manipulated queryset
        """
        if value == "open":
            return queryset.all().exclude(status="closed")
        else:
            return queryset.filter(status="closed")

    def get_queryset_from_ordering(self, queryset, name, value):
        """Return queryset based on value param from DATE_ORDERING_CHOICES.

        Args:
            queryset (QuerySet): Current queryset based on applied filters
            name (str): Form field name
            value (str): Selected value from DATE_ORDERING_CHOICES

        Returns:
            QuerySet: Manipulated queryset
        """
        if value == "ascending_created_on":
            expression = "created_on"
        elif value == "descending_created_on":
            expression = "-created_on"
        elif value == "ascending_updated_on":
            expression = "updated_on"
        else:
            expression = "-updated_on"
        return queryset.order_by(expression)


class ElevatedUserTicketFilter(CustomerTicketFilter, django_filters.FilterSet):
    """FilterSet to be presented to users with elevated roles."""

    def __init__(self, *args, **kwargs):
        """Remove 'user' information passed from Ticket List View"""
        # CREDIT: TS Jee and nishant - Stack Overflow
        # REASON: Pass request.user from ListView
        # URL: See README Credits Section, Code Credit References - #1
        self.user = kwargs.pop("user")
        super(CustomerTicketFilter, self).__init__(*args, **kwargs)

    ASSIGNEE_CHOICES = (("me", "Me"), ("all", "All"))

    author__username = django_filters.CharFilter(
        lookup_expr="icontains", label="Requestor Username"
    )

    assigned_technician__username = django_filters.CharFilter(
        lookup_expr="icontains", label="Assigned Technician Username"
    )

    title = django_filters.CharFilter(
        lookup_expr="icontains", label="Request Title Contains"
    )

    description = django_filters.CharFilter(
        lookup_expr="icontains", label="Request Description Contains"
    )

    # filter_by_assignee form field. Set the field label, choices
    # to be presented to the user and the filter method to be used
    filter_by_assignee = django_filters.ChoiceFilter(
        label="Assigned to",
        choices=ASSIGNEE_CHOICES,
        method="get_queryset_from_assignee",
    )

    class Meta:
        model = Ticket
        fields = (
            ("filter_by_assignee",) +
            CustomerTicketFilter.Meta.fields + (
                "author__username",
                "assigned_technician__username",
                "priority",
                "assigned_team",
                "category",
                "type",
                "title",
                "description",
            )
        )

    def get_queryset_from_assignee(self, queryset, name, value):
        """Return queryset based on value param from ASSIGNEE_CHOICES.

        Args:
            queryset (QuerySet): Current queryset based on applied filters name
            (str): Form field name value (str): Selected value from
            ASSIGNEE_CHOICES

        Returns:
            QuerySet: Manipulated queryset
        """
        if value == "me":
            # Filter queryset based on user object passed from ticket list view
            # to allow filtering of all tickets assigned to the logged on user
            return queryset.filter(assigned_technician=self.user)
        else:
            return queryset.all()
