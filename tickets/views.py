from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ticket


# Create listview to retrieve a list of tickets from the database
class TicketListView(generic.ListView):
    template_name = "ticket_list.html"
    context_object_name = "tickets"

    # Restrict the queryset to only tickets where the logged on user is th
    # author
    def get_queryset(self):
        queryset = Ticket.objects.filter(author=self.request.user)
        return queryset
