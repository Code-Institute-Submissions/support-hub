"""Views for accounts application"""


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.views import generic
from common.utils import is_slug_a_number
from .forms import AdminProfileUpdateForm, ProfileUpdateForm
from .models import CustomUser


def demo_home_page_view(request):
    """Basic home/index page - Introduction to site"""

    # If the visitor fill in the contact form, let them know that no
    # information has been saved as the site is for educational purposes
    if request.POST:
        messages.info(
            request,
            (
                "Thank you for your interest!"
                "<br><br>"
                "This site is for education purposes and your email "
                "address has not been saved."
            ),
        )

    return render(request, "index.html", {})


class ProfileDetailView(
    LoginRequiredMixin, UserPassesTestMixin, generic.DetailView
):
    """DetailView - Used to display individual profiles."""

    model = CustomUser
    template_name = "profile_detail.html"
    context_object_name = "profile_user"

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

    # Test function to ensure the logged in user can only see their own
    # profile, unless their role is administrator in which case they can see
    # all profiles
    def test_func(self):
        """Determine if a user has permissions to view a resource

        Returns:
            bool: Result of a conditional statement to determine if the user
            can view the object
        """
        logged_in_user = self.request.user
        current_profiles_user = self.get_object()

        # Conditional statement to check if the profile is that of the
        # currently logged on user or the user has the elevated permissions
        # required to view any profile.
        if (
            current_profiles_user == logged_in_user or
            logged_in_user.role == "administrator"
        ):
            return True
        else:
            return False


class ProfileUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """UpdateView - Used to update a the profile"""

    model = CustomUser
    template_name = "profile_update.html"
    form_class = ProfileUpdateForm
    success_message = "Profile Changes Saved!"

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
        """Add data to the context based on user role so it can be rendered in
        the template.

        Add the user whose profile is being viewed to the context, used in the
        template by the forms cancel button to redirect to the correct profile.

        Returns:
            dict: Context data with the filter added
        """

        context = super().get_context_data(**kwargs)
        current_profile_owner = self.get_object()
        context["current_profile_owner_id"] = current_profile_owner.id
        context[
            "current_profile_owner_username"
        ] = current_profile_owner.username
        return context

    def get_form_class(self):
        """Return the form class to be used when updating a profile

        User role determines the form that will be returned. Users with the
        'administrator' role will see an a greater set of form fields whereas
        non-elevated users will see limited fields.

        Returns:
            ModelFormMetaclass: Form object to be used when updating a profile
            (either AdminProfileUpdateForm or ProfileUpdateForm)
        """
        if self.request.user.role == "administrator":
            form = AdminProfileUpdateForm
        else:
            form = ProfileUpdateForm
        return form

    def test_func(self):
        """Determine if a user has permissions to view a resource

        Returns:
            bool: Result of a conditional statement to determine if the user
            can view the object
        """
        logged_in_user = self.request.user
        current_profile = self.get_object()

        # Conditional statement to check if the profile is that of the
        # currently logged on user or the user has the elevated permissions
        # required to view any profile. Ensures the non-elevated users can only
        # edit their own profile
        if (
            current_profile == logged_in_user or
            logged_in_user.role == "administrator"
        ):
            return True
        else:
            return False


class ProfileListView(
    LoginRequiredMixin, UserPassesTestMixin, generic.ListView
):
    """ListView - Used to show a list of user profiles"""

    model = CustomUser
    template_name = "profile_list.html"
    context_object_name = "profile_users"

    def test_func(self):
        """Determine if a user has permissions to view a resource

        Returns:
            bool: Result of a conditional statement to determine if the user
            can view the object
        """
        logged_in_user = self.request.user

        # Ensure only a user with the administrator role can view the profile
        # list
        if logged_in_user.role == "administrator":
            return True
        else:
            return False

    # Queryset based on form input
    # CREDIT: Willem Van Onsem and Abu Yunus - Stack Overflow
    # URL: https://stackoverflow.com/questions/63935852
    def get_queryset(self, *args, **kwargs):
        """Get queryset based on user form input.

        Used to allow a simple search of usernames.

        Returns:
            QuerySet: QuerySet filtered based on user form input.
        """
        queryset = super().get_queryset(*args, **kwargs)
        username = self.request.GET.get("username")
        if username:
            return queryset.filter(username__icontains=username)
