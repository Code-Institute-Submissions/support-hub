from django.shortcuts import render, redirect
from django.views import generic
from .models import CustomUser
from .forms import ProfileUpdateForm, AdminProfileUpdateForm
from common.utils import is_slug_a_number
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
    context_object_name = "profile_user"

    def dispatch(self, request, *args, **kwargs):
        if is_slug_a_number(request, kwargs["pk"]):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("home")

    # Test function to ensure the logged in user can only see their own
    # profile, unless their role is administrator in which case they can see
    # all profiles
    def test_func(self):
        logged_in_user = self.request.user
        current_user = self.get_object()

        if (
            current_user == logged_in_user
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

    def dispatch(self, request, *args, **kwargs):
        if is_slug_a_number(request, kwargs["pk"]):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("home")

    # Method to return the user whose profile is being viewed, used when
    # cancelling the form to updated the profile
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_profile_owner = self.get_object()
        context["current_profile_owner_id"] = current_profile_owner.id
        context[
            "current_profile_owner_username"
        ] = current_profile_owner.username
        return context

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
    context_object_name = "profile_users"

    # Test function to ensure only a user with the administrator role can view
    # the profile list
    def test_func(self):
        logged_in_user = self.request.user

        if logged_in_user.role == "administrator":
            return True
        else:
            return False

    # Queryset based on form input
    # CREDIT: Willem Van Onsem and Abu Yunus - Stack Overflow
    # URL: https://stackoverflow.com/questions/63935852
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        username = self.request.GET.get("username")
        if username:
            return queryset.filter(username__icontains=username)
