import django_filters
from .models import Ticket

# CREDIT: Filtering adapted from The Dumbfounds: Django Filtering System with
#         django-filter
# URL:    https://www.youtube.com/watch?v=nle3u6Ww6Xk


class StaffTicketFilter(django_filters.FilterSet):

    STATUS_FILTERING_CHOICES = (
        ("open", "All Open Requests"),
        ("closed", "Closed"),
    )

    DATE_ORDERING_CHOICES = (
        ("descending_created_on", "Creation Date- Descending"),
        ("ascending_created_on", "Creation Date - Ascending"),
        ("descending_updated_on", "Updated Date - Descending"),
        ("ascending_updated_on", "Updated Date - Ascending"),
    )

    # Filter tickets based on status - Function to change queryset based on the
    # user choice
    def get_queryset_status(self, queryset, name, value):
        if value == "open":
            return queryset.all().exclude(status="closed")
        else:
            return queryset.filter(status="closed")

    # Filter tickets based on status - Declare the ChoiceFilter to be
    # displayed
    filter_by_status = django_filters.ChoiceFilter(
        label="Status",
        choices=STATUS_FILTERING_CHOICES,
        method="get_queryset_status",
    )

    # Order by creation date - Function to change queryset based on the
    # user choice
    def get_queryset_creation_date(self, queryset, name, value):
        if value == "ascending_created_on":
            expression = "created_on"
        elif value == "descending_created_on":
            expression = "-created_on"
        elif value == "ascending_updated_on":
            expression = "updated_on"
        else:
            expression = "-updated_on"

        return queryset.order_by(expression)

    # Filter tickets based on status - Declare the ChoiceFilter to be
    # displayed
    order_by_creation_date = django_filters.ChoiceFilter(
        label="Sort by creation date",
        choices=DATE_ORDERING_CHOICES,
        method="get_queryset_creation_date",
    )

    class Meta:
        model = Ticket
        fields = (
            "filter_by_status",
            "order_by_creation_date",
        )


class ElevatedUserTicketFilter(StaffTicketFilter, django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        # CREDIT: TS Jee and nishant - Stack Overflow
        # REASON: Pass request.user from ListView
        # URL: https://stackoverflow.com/questions/54069084/passing-request-user-to-a-queryset-in-modelchoicefilter
        self.user = kwargs.pop("user")
        super(StaffTicketFilter, self).__init__(*args, **kwargs)

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

    def get_queryset_assignee(self, queryset, name, value):
        if value == "me":
            return queryset.filter(assigned_technician=self.user)
        else:
            return queryset.all()

    filter_by_assignee = django_filters.ChoiceFilter(
        label="Assigned to",
        choices=ASSIGNEE_CHOICES,
        method="get_queryset_assignee",
    )

    class Meta:
        model = Ticket
        fields = (
            ("filter_by_assignee",)
            + StaffTicketFilter.Meta.fields
            + (
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
