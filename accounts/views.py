from django.shortcuts import render
from django.views import generic
from .models import CustomUser
from .forms import ProfileUpdateForm, AdminProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin

# Create demo home page view to be used for initial testing of authentication
def demo_home_page_view(request):
    return render(request, "index.html", {})


class ProfileDetailView(
    LoginRequiredMixin, UserPassesTestMixin, generic.DetailView
):
    model = CustomUser
    template_name = "profile_detail.html"
    context_object_name = "profile"

    # Test function to ensure the logged in user can only see their own
    # profile, unless their role is administrator in which case they can see
    # all profiles
    def test_func(self):
        logged_in_user = self.request.user
        current_profile = self.get_object()

        if (
            current_profile == logged_in_user
            or logged_in_user.role == "administrator"
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
    model = CustomUser
    template_name = "profile_update.html"
    form_class = ProfileUpdateForm
    success_message = "Profile Changes Saved!"

    def get_form_class(self):
        if self.request.user.role == "administrator":
            form = AdminProfileUpdateForm
        else:
            form = ProfileUpdateForm
        return form

    # Test function to ensure the logged in user can only edit their own
    # profile, unless their role is administrator in which case they can edit
    # all profiles
    def test_func(self):
        logged_in_user = self.request.user
        current_profile = self.get_object()

        if (
            current_profile == logged_in_user
            or logged_in_user.role == "administrator"
        ):
            return True
        else:
            return False


class ProfileListView(
    LoginRequiredMixin, UserPassesTestMixin, generic.ListView
):
    model = CustomUser
    template_name = "profile_list.html"
    context_object_name = "profiles"

    # Test function to ensure only a user with the administrator role can view
    # the profile list
    def test_func(self):
        logged_in_user = self.request.user

        if logged_in_user.role == "administrator":
            return True
        else:
            return False
