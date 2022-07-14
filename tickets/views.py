from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ticket
from .forms import StaffTicketCreationForm


# Create listview to retrieve a list of tickets from the database
class TicketListView(generic.ListView):
    template_name = "ticket_list.html"
    context_object_name = "tickets"

    # Restrict the queryset to only tickets where the logged on user is th
    # author
    def get_queryset(self):
        queryset = Ticket.objects.filter(author=self.request.user)
        return queryset


# CreateView to facilitate the creation of tickets
class TicketCreateView(generic.CreateView):
    queryset = Ticket.objects.all()
    template_name = "ticket_create.html"
    form_class = StaffTicketCreationForm
    success_url = "/tickets/"

    # Add data to form when using CreateView
    # CREDIT: Piyush Maurya - Stack Overflow
    # URL: https://stackoverflow.com/a/45221181
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(TicketCreateView, self).form_valid(form)
