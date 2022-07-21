from django.urls import path
from .views import demo_home_page_view, ProfileDetailView, ProfileUpdateView


urlpatterns = [
    path("", demo_home_page_view, name="home"),
    path(
        "accounts/<slug:pk>/",
        ProfileDetailView.as_view(),
        name="profile_detail",
    ),
    path(
        "accounts/<slug:pk>/edit",
        ProfileUpdateView.as_view(),
        name="profile_update",
    ),
]
