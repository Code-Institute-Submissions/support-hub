from django.shortcuts import redirect
from django.views import generic, View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.http import Http404
from .models import Ticket, Note
from .filters import StaffTicketFilter, ElevatedUserTicketFilter
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

    # Present different queryset based on user role
    #
    # This allows elevated users to see all requests where non-elevated users
    # see only tickets they have authored
    def get_queryset(self):
        self.request.user
        if (self.request.user.role == "administrator") or (
            self.request.user.role == "technician"
        ):
            queryset = Ticket.objects.all()
        else:
            queryset = Ticket.objects.filter(author=self.request.user)
        return queryset

    # Override get_context_data to add the filter to the context
    #
    # CREDIT: Filtering adapted from The Dumbfounds: Django Filtering System with
    #         django-filter
    # URL:    https://www.youtube.com/watch?v=nle3u6Ww6Xk
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Present different filter based on user role
        if (self.request.user.role == "administrator") or (
            self.request.user.role == "technician"
        ):
            context["filter"] = ElevatedUserTicketFilter(
                self.request.GET,
                user=self.request.user,
                queryset=self.get_queryset(),
            )
        else:
            context["filter"] = StaffTicketFilter(
                self.request.GET, queryset=self.get_queryset()
            )
        return context


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

    # Override get method to raise 404 error if url entered manually
    def get(self, request, *args, **kwargs):
        raise Http404

    # Overwrite delete method to prevent users with non-elevated roles deleting
    # records.
    #
    # The delete button visibility is controlled using the template. This
    # method prevents unauthorized users deleting records, in the event the
    # button is accidentally made visible during design changes.
    def delete(self, request, *args, **kwargs):
        logged_in_user = self.request.user
        if logged_in_user.role == "staff":
            # Redirect user back to ticket detail url with message
            messages.error(
                request,
                "You do not have permission to delete this request.",
            )
            return redirect("ticket_detail", pk=kwargs["pk"])
        else:
            messages.info(
                request,
                f"Request #{kwargs['pk']} deleted successfully.",
            )
            return super(TicketDeleteView, self).delete(
                request, *args, **kwargs
            )

    def get_success_url(self):
        return reverse("ticket_list")
