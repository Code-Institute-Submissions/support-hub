from django.shortcuts import render
from django.views import generic
from .models import CustomUser
from .forms import ProfileUpdateForm

## LOGIN REQUIRED ETC!!!!

# Create demo home page view to be used for initial testing of authentication
def demo_home_page_view(request):
    return render(request, "index.html", {})


class ProfileDetailView(generic.DetailView):
    model = CustomUser
    template_name = "profile_detail.html"
    context_object_name = "profile"


class ProfileUpdateView(generic.UpdateView):
    model = CustomUser
    template_name = "profile_update.html"
    form_class = ProfileUpdateForm
