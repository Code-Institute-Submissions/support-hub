from django.shortcuts import render
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from .models import Ticket, Note
from .forms import (
    StaffTicketCreationForm,
    StaffTicketUpdateForm,
    ElevatedUserTicketForm,
    NoteForm,
)


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

    # Present different forms base on user roles
    def get_form_class(self):
        if (self.request.user.role == "administrator") or (
            self.request.user.role == "technician"
        ):
            form = ElevatedUserTicketForm
        else:
            form = StaffTicketCreationForm
        return form

    # Populate the author form field when form used in view is loaded
    def get_initial(self):
        return {
            "author": self.request.user,
        }

    # Add data to form when using CreateView
    # CREDIT: Piyush Maurya - Stack Overflow
    # URL: https://stackoverflow.com/a/45221181
    def form_valid(self, form):
        # If the user has staff role, this forces the author to be set as
        # themselves whereas elevated staff can set another user as the author
        if self.request.user.role == "staff":
            form.instance.author = self.request.user
        return super(TicketCreateView, self).form_valid(form)


# Ticket DetailView to display individual tickets with comment form
# CREDIT: Adapted from Django Documentation
# URL: https://docs.djangoproject.com/en/4.0/topics/class-based-views/mixins/#an-alternative-better-solution
class TicketDetailView(
    LoginRequiredMixin, UserPassesTestMixin, generic.DetailView
):
    template_name = "ticket_detail.html"
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = NoteForm()
        return context

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


# Note FormView to handle form validation and post requests
# CREDIT: Adapted from Django Documentation
# URL: https://docs.djangoproject.com/en/4.0/topics/class-based-views/mixins/#an-alternative-better-solution
class NoteFormView(SingleObjectMixin, generic.FormView):
    template_name = "ticket_detail.html"
    form_class = NoteForm
    model = Ticket

    def form_valid(self, form):
        form = self.get_form()
        note = form.save(commit=False)
        note.ticket = self.object
        note.author = self.request.user
        note.save()
        return super().form_valid(note)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("ticket_detail", kwargs={"pk": self.object.pk})


# Ticket View to determine which view to get based on the request type
# CREDIT: Adapted from Django Documentation
# URL: https://docs.djangoproject.com/en/4.0/topics/class-based-views/mixins/#an-alternative-better-solution
class TicketView(View):
    def get(self, request, *args, **kwargs):
        view = TicketDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = NoteFormView.as_view()
        return view(request, *args, **kwargs)


class TicketUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView
):
    queryset = Ticket.objects.all()
    template_name = "ticket_update.html"

    # Present different forms base on user roles
    def get_form_class(self):
        if (self.request.user.role == "administrator") or (
            self.request.user.role == "technician"
        ):
            form = ElevatedUserTicketForm
        else:
            form = StaffTicketUpdateForm
        return form

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


class TicketDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ticket

    def get_success_url(self):
        return reverse("ticket_list")
