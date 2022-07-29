from django.shortcuts import redirect
from django.views import generic, View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.http import Http404
from django.core.mail import send_mail
from smtplib import SMTPException
from django.conf import settings
from .models import Ticket, Comment
from .filters import CustomerTicketFilter, ElevatedUserTicketFilter
from common.utils import is_slug_a_number
from .utils import is_user_elevated_role
from .forms import (
    CustomerTicketCreationForm,
    CustomerTicketUpdateForm,
    ElevatedUserTicketForm,
    CommentForm,
)


# Create listview to retrieve a list of tickets from the database
class TicketListView(LoginRequiredMixin, generic.ListView):
    template_name = "ticket_list.html"
    context_object_name = "tickets"

    # Present different queryset based on user role
    #
    # This allows elevated users to see all requests where non-elevated users
    # see only tickets they have authored
    def get_queryset(self):
        if is_user_elevated_role(self.request.user):
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
        if is_user_elevated_role(self.request.user):
            context["filter"] = ElevatedUserTicketFilter(
                self.request.GET,
                user=self.request.user,
                queryset=self.get_queryset(),
            )
        else:
            context["filter"] = CustomerTicketFilter(
                self.request.GET, queryset=self.get_queryset()
            )
        return context


# CreateView to facilitate the creation of tickets
class TicketCreateView(
    LoginRequiredMixin, SuccessMessageMixin, generic.CreateView
):
    model = Ticket
    template_name = "ticket_create.html"
    success_message = "Ticket created successfully."

    # Present different forms base on user roles
    def get_form_class(self):
        if is_user_elevated_role(self.request.user):
            form = ElevatedUserTicketForm
        else:
            form = CustomerTicketCreationForm
        return form

    # Populate the author form field when form used in view is loaded
    def get_initial(self):
        return {
            "author": self.request.user,
        }

    def form_valid(self, form):

        # Get the ticket model objet
        ticket_obj = form.save(commit=False)

        # If the user has customer role, this forces the author to be set as
        # themselves whereas elevated users can set another user as the author
        #
        # Add data to form when using CreateView
        # CREDIT: Piyush Maurya - Stack Overflow
        # URL: https://stackoverflow.com/a/45221181
        if self.request.user.role == "customer":
            form.instance.author = self.request.user

        # If the ticket object contains an image, try to save the form by
        # returning valid. This will catch any cloudinary errors not caught by
        # the model validation (invalid api key etc.)
        if ticket_obj.ticket_image:
            try:
                return super(TicketCreateView, self).form_valid(form)
            except Exception as e:
                messages.error(
                    self.request,
                    (
                        "An error occurred when processing your request. "
                        "Your ticket has not been saved.</br></br>"
                        f"Error detail: {e}"
                    ),
                )
                return redirect("ticket_list")
        return super(TicketCreateView, self).form_valid(form)


# Ticket DetailView to display individual tickets with comment form
# CREDIT: Adapted from Django Documentation
# URL: https://docs.djangoproject.com/en/4.0/topics/class-based-views/mixins/#an-alternative-better-solution
class TicketDetailView(
    LoginRequiredMixin, UserPassesTestMixin, generic.DetailView
):
    template_name = "ticket_detail.html"
    model = Ticket

    def dispatch(self, request, *args, **kwargs):
        if is_slug_a_number(request, kwargs["pk"]):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

    # Test to check the currently logged on user is the author of the ticket or
    # has the elevated permissions required to view any ticket.
    def test_func(self):
        logged_in_user = self.request.user
        current_ticket = self.get_object()

        if current_ticket.author == logged_in_user or is_user_elevated_role(
            logged_in_user
        ):
            return True
        else:
            return False


# Comment FormView to handle form validation and post requests
# CREDIT: Adapted from Django Documentation
# URL: https://docs.djangoproject.com/en/4.0/topics/class-based-views/mixins/#an-alternative-better-solution
class CommentFormView(SingleObjectMixin, generic.FormView):
    template_name = "ticket_detail.html"
    form_class = CommentForm
    model = Ticket

    def form_valid(self, form):
        form = self.get_form()
        comment = form.save(commit=False)
        comment.ticket = self.object
        comment.author = self.request.user
        comment.save()

        # Call the model function to set its updated_on field to the current
        # time
        comment.ticket.set_ticket_updated_now()

        if comment.ticket.author != comment.author:
            try:
                send_mail(
                    subject=f"Support Hub - {comment.ticket}",
                    message=(
                        "Your Ticket has an update!\n\n"
                        f"Update posted by '{comment.author}':\n"
                        f"'{comment.body_without_tags}'\n\n"
                        f"Current ticket status is '{comment.ticket.status}'\n"
                        "Use this link to view this ticket in Support Hub "
                        f"'http://127.0.0.1:8000{comment.ticket.get_absolute_url()}'"
                    ),
                    html_message=(
                        "<h2>Your Ticket has an update!</h2>"
                        f"<p>Update posted by '{comment.author}':</p>"
                        f"<p>'{comment.body_without_tags}'</p>"
                        "<br>"
                        f"<p>Current ticket status is '{comment.ticket.status}'</p>"
                        "<p>Click the link to view this ticket in Support Hub "
                        f"<a href='{self.request.META['HTTP_HOST']}{comment.ticket.get_absolute_url()}'>Ticket Link</a></p>"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[comment.ticket.author.email],
                    fail_silently=False,
                )
            except SMTPException as e:
                messages.error(
                    self.request,
                    f"Error sending email update to ticket owner - '{comment.ticket.author}'{e}",
                )

        return super().form_valid(comment)

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
        view = CommentFormView.as_view()
        return view(request, *args, **kwargs)


class TicketUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    queryset = Ticket.objects.all()
    template_name = "ticket_update.html"
    success_message = "Ticket updated successfully."

    def dispatch(self, request, *args, **kwargs):
        if is_slug_a_number(request, kwargs["pk"]):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("home")

    # Present different forms base on user roles
    def get_form_class(self):
        if is_user_elevated_role(self.request.user):
            form = ElevatedUserTicketForm
        else:
            form = CustomerTicketUpdateForm
        return form

    def form_valid(self, form):

        # Get the ticket objet
        ticket_obj = form.save(commit=False)

        # If the ticket object contains an image, try to save the form by
        # returning valid. This will catch any cloudinary errors not caught by
        # the model validation (invalid api key etc.)
        if ticket_obj.ticket_image:
            try:
                return super(TicketUpdateView, self).form_valid(form)
            except Exception as e:
                messages.error(
                    self.request,
                    (
                        "An error occurred when processing your request. "
                        "Your changes have not been saved.</br></br>"
                        f"Error detail: {e}"
                    ),
                )
                return redirect("ticket_list")
        else:
            return super(TicketUpdateView, self).form_valid(form)

    def test_func(self):
        logged_in_user = self.request.user
        current_ticket = self.get_object()

        if current_ticket.author == logged_in_user or is_user_elevated_role(
            logged_in_user
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
        if not is_user_elevated_role(logged_in_user):
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
