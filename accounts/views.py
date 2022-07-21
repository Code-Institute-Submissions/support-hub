from django.shortcuts import render
from django.views import generic
from .models import CustomUser
from .forms import ProfileUpdateForm
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

    # Test function to ensure the logged in user can see only their own profile
    def test_func(self):
        logged_in_user = self.request.user
        current_profile = self.get_object()

        return True if current_profile == logged_in_user else False


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

    # Test function to ensure the logged in user can edit only their own
    # profile
    def test_func(self):
        logged_in_user = self.request.user
        current_profile = self.get_object()

        return True if current_profile == logged_in_user else False
