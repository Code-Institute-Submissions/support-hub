import django_filters
from .models import Ticket

# CREDIT: Filtering adapted from The Dumbfounds: Django Filtering System with
#         django-filter
# URL:    https://www.youtube.com/watch?v=nle3u6Ww6Xk
class StaffTicketFilter(django_filters.FilterSet):
    class Meta:
        model = Ticket
        fields = ("status", "created_on", "updated_on")


class ElevatedUserTicketFilter(StaffTicketFilter, django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(StaffTicketFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = Ticket
        fields = StaffTicketFilter.Meta.fields + (
            "priority",
            "assigned_team",
            "category",
            "type",
        )
