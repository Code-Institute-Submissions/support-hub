from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
from .models import Ticket
from .forms import StaffTicketCreationForm, StaffTicketUpdateForm


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

    # Add data to form when using CreateView
    # CREDIT: Piyush Maurya - Stack Overflow
    # URL: https://stackoverflow.com/a/45221181
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(TicketCreateView, self).form_valid(form)


class TicketDetailView(
    LoginRequiredMixin, UserPassesTestMixin, generic.DetailView
):
    template_name = "ticket_detail.html"
    queryset = Ticket.objects.all()

    # Test to check the currently logged on user is the author of the ticket or
    # has the elevated permissions required to view any ticket.
    def test_func(self):
        logged_in_user = self.request.user
        current_ticket = self.get_object()

        if (
            current_ticket.author == logged_in_user
            or logged_in_user.role == "administrator"
            or logged_in_user.role == "technician"
        ):
            return True
        else:
            return False


class TicketUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView
):
    queryset = Ticket.objects.all()
    template_name = "ticket_update.html"
    form_class = StaffTicketUpdateForm

    def test_func(self):
        logged_in_user = self.request.user
        current_ticket = self.get_object()

        if (
            current_ticket.author == logged_in_user
            or logged_in_user.role == "administrator"
            or logged_in_user.role == "technician"
        ):
            return True
        else:
            return False
