"""Views for tickets application"""


from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View, generic
from django.views.generic.detail import SingleObjectMixin
from smtplib import SMTPException
from common.utils import is_slug_a_number
from .filters import CustomerTicketFilter, ElevatedUserTicketFilter
from .forms import (
    CommentForm,
    CustomerTicketCreationForm,
    CustomerTicketUpdateForm,
    ElevatedUserTicketForm,
)
from .models import Ticket
from .utils import is_user_elevated_role


class TicketListView(LoginRequiredMixin, generic.ListView):
    """ListView - Used to show a list of ticket objects"""

    template_name = "ticket_list.html"
    context_object_name = "tickets"

    def get_queryset(self):
        """Get different queryset based on user role.

        User role determines the queryset that is returned. Elevated users will
        see an unfiltered list of all tickets in the database whereas
        non-elevated users see only tickets they have authored.

        Returns:
            QuerySet: QuerySet filtered based on user role
        """
        if is_user_elevated_role(self.request.user):
            queryset = Ticket.objects.all()
        else:
            queryset = Ticket.objects.filter(author=self.request.user)
        return queryset

    # CREDIT: Filtering adapted from The Dumbfounds: Django Filtering System
    #         with django-filter
    # URL: https://www.youtube.com/watch?v=nle3u6Ww6Xk
    def get_context_data(self, **kwargs):
        """Add data to the context based on user role so it can be rendered in
        the template.

        User role determines the filter that is added to the context. Elevated
        users will see an a greater set of filter fields whereas non-elevated
        user options will be limited.

        Returns:
            dict: Context data with the filter added
        """
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
    """CreateView - Used to create a new ticket object."""

    model = Ticket
    template_name = "ticket_create.html"
    success_message = "Ticket created successfully."

    def get_form_class(self):
        """Return the form class to be used when creating a ticket

        User role determines the form that will be returned. Elevated users
        will see an a greater set of form fields whereas non-elevated user
        fields will be limited.

        Returns:
            ModelFormMetaclass: Form object to be used when creating a ticket
            (either ElevatedUserTicketForm or CustomerTicketCreationForm)
        """
        if is_user_elevated_role(self.request.user):
            form = ElevatedUserTicketForm
        else:
            form = CustomerTicketCreationForm
        return form

    def get_initial(self):
        """Initial data to be used for the form

        Returns:
            dict: Contains a SimpleLazyObject containing the user object
        """
        return {
            "author": self.request.user,
        }

    def form_valid(self, form):
        """Check form is valid and insert data in to the form before saving the
        model object.

        Args:
            form (Form object): Form object (either ElevatedUserTicketForm or
            CustomerTicketCreationForm) containing form contents
        """

        # Get the ticket model objet
        ticket_obj = form.save(commit=False)

        # If the current user has the customer role, force the author to be set
        # as themselves whereas elevated users can set other users as the
        # author
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
# URL: https://docs.djangoproject.com/en/4.0/topics/class-based-views/mixins/
class TicketDetailView(
    LoginRequiredMixin, UserPassesTestMixin, generic.DetailView
):
    """DetailView - Used to display individual tickets."""

    model = Ticket
    template_name = "ticket_detail.html"

    def dispatch(self, request, *args, **kwargs):
        """Take in the request and determine if able to proceed with the slug
        provided.

        Used in this case to ensure that manually entered slugs in the URL
        (that cannot be type cast as integers, do not raise errors causing
        internal servers errors but are instead reported to the user.
        """

        # Uses custom util (common.utils) to check if slug is a number and
        # return the appropriate response
        if is_slug_a_number(request, kwargs["pk"]):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("home")

    def get_context_data(self, **kwargs):
        """Add comment form to the context so it can be rendered in the
        template.

        Returns:
            dict: Context data with the comment form added
        """
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

    def test_func(self):
        """Determine if a user has permissions to view a resource

        Returns:
            bool: Result of a conditional statement to determine if the user
            can view the object
        """
        logged_in_user = self.request.user
        current_ticket = self.get_object()

        # Conditional statement to check if the currently logged on user is the
        # author of the ticket or has the elevated permissions required to view
        # any ticket. Uses the custom application util 'is_user_elevated_role'
        if current_ticket.author == logged_in_user or is_user_elevated_role(
            logged_in_user
        ):
            return True
        else:
            return False


# CREDIT: Adapted from Django Documentation
# URL: https://docs.djangoproject.com/en/4.0/topics/class-based-views/mixins/
class CommentFormView(SingleObjectMixin, generic.FormView):
    """FormView - Used to handle form validation and post requests"""

    model = Ticket
    form_class = CommentForm
    template_name = "ticket_detail.html"

    def form_valid(self, form):
        """Check form is valid and insert data in to the form before saving the
        model object.

        Args:
            form (Form object): Form object (either ElevatedUserTicketForm or
            CustomerTicketCreationForm) containing form contents
        """
        form = self.get_form()
        comment = form.save(commit=False)
        comment.ticket = self.object
        comment.author = self.request.user
        comment.save()

        # Call model function to set related ticket object's updated_on field
        # to the current time
        comment.ticket.set_ticket_updated_now()

        # If the user posting a comment to the ticket is not the author, send
        # an email to the author notifying them a comment has been left.
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
                        f"'{self.request.META['HTTP_HOST']}"
                        f"{comment.ticket.get_absolute_url()}'"
                    ),
                    html_message=(
                        "<h2>Your Ticket has an update!</h2>"
                        f"<p>Update posted by '{comment.author}':</p>"
                        f"<p>'{comment.body_without_tags}'</p>"
                        "<br>"
                        "<p>Current ticket status is "
                        f"'{comment.ticket.status}'</p>"
                        "<p>Click the link to view this ticket in Support Hub "
                        f"<a href='{self.request.META['HTTP_HOST']}"
                        f"{comment.ticket.get_absolute_url()}'>Ticket Link</a>"
                        "</p>"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[comment.ticket.author.email],
                    fail_silently=False,
                )
            # Notify users of any errors sending the email.
            except SMTPException as e:
                messages.error(
                    self.request,
                    "Error sending email update to ticket owner - "
                    f"'{comment.ticket.author}'{e}",
                )
        return super().form_valid(comment)

    def post(self, request, *args, **kwargs):
        """Handle POST requests"""
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        """Url to be returned if successful

        Returns:
            str: URL of current ticket
        """
        return reverse("ticket_detail", kwargs={"pk": self.object.pk})


#
# CREDIT: Adapted from Django Documentation
# URL: https://docs.djangoproject.com/en/4.0/topics/class-based-views/mixins/
class TicketView(View):
    """View - Used to determine which view to use based on the request type"""

    # If the request method is GET use the DetailView to display the ticket and
    # comment form
    def get(self, request, *args, **kwargs):
        view = TicketDetailView.as_view()
        return view(request, *args, **kwargs)

    # If the request method is POST use the FormView so save the comment
    def post(self, request, *args, **kwargs):
        view = CommentFormView.as_view()
        return view(request, *args, **kwargs)


class TicketUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """UpdateView - Used to update a the ticket"""

    queryset = Ticket.objects.all()
    template_name = "ticket_update.html"
    success_message = "Ticket updated successfully."

    def dispatch(self, request, *args, **kwargs):
        """Take in the request and determine if able to proceed with the slug
        provided.

        Used in this case to ensure that manually entered slugs in the URL
        (that cannot be type cast as integers, do not raise errors causing
        internal servers errors but are instead reported to the user.
        """

        # Uses custom util (common.utils) to check if slug is a number and
        # return the appropriate response
        if is_slug_a_number(request, kwargs["pk"]):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("home")

    # Present different forms base on user roles
    def get_form_class(self):
        """Return the form class to be used when updating a ticket

        User role determines the form that will be returned. Elevated users
        will see an a greater set of form fields whereas non-elevated user
        fields will be limited.

        Returns:
            ModelFormMetaclass: Form object to be used when updating a ticket
            (either ElevatedUserTicketForm or CustomerTicketUpdateForm)
        """
        if is_user_elevated_role(self.request.user):
            form = ElevatedUserTicketForm
        else:
            form = CustomerTicketUpdateForm
        return form

    def form_valid(self, form):
        """Check form is valid and insert data in to the form before saving the
        model object.

        Args:
            form (Form object): Form object (either ElevatedUserTicketForm or
            CustomerTicketCreationForm) containing form contents
        """

        # Get the ticket model objet
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
        """Determine if a user has permissions to view a resource

        Returns:
            bool: Result of a conditional statement to determine if the user
            can view the object
        """
        logged_in_user = self.request.user
        current_ticket = self.get_object()

        # Conditional statement to check if the currently logged on user is the
        # author of the ticket or has the elevated permissions required to view
        # any ticket. Uses the custom application util 'is_user_elevated_role'
        if current_ticket.author == logged_in_user or is_user_elevated_role(
            logged_in_user
        ):
            return True
        else:
            return False


class TicketDeleteView(LoginRequiredMixin, generic.DeleteView):
    """DeleteView - Used to delete an object"""

    model = Ticket

    # Override get method to raise 404 error if url entered manually as no
    # template is rendered and the view is accessed only used via model input
    def get(self, request, *args, **kwargs):
        raise Http404

    # Overwrite delete method to prevent users with non-elevated roles deleting
    # records.
    #

    def delete(self, request, *args, **kwargs):
        """Delete method used to delete and object but also in this case to
        prevent users with non-elevated roles deleting records.

        The delete button visibility is controlled using the template. This
        method prevents unauthorized users deleting records in the event the
        button is accidentally made visible during design changes.
        """
        logged_in_user = self.request.user
        if not is_user_elevated_role(logged_in_user):
            # Redirect user back to ticket detail url with message
            messages.error(
                request,
                "You do not have permission to delete this request.",
            )
            return redirect("ticket_detail", pk=kwargs["pk"])
        else:
            # Provide a success message and delete the object
            messages.info(
                request,
                f"Request #{kwargs['pk']} deleted successfully.",
            )
            return super(TicketDeleteView, self).delete(
                request, *args, **kwargs
            )

    def get_success_url(self):
        """Url to be returned if successful

        Returns:
            str: URL of current ticket
        """
        return reverse("ticket_list")
