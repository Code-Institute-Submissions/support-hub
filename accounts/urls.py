"""URLs for accounts application"""


from django.urls import path
from .views import (
    demo_home_page_view,
    ProfileDetailView,
    ProfileUpdateView,
    ProfileListView,
)


urlpatterns = [
    path("", demo_home_page_view, name="home"),
    path(
        "accounts/profile/<slug:pk>/",
        ProfileDetailView.as_view(),
        name="profile_detail",
    ),
    path(
        "accounts/profile/<slug:pk>/edit",
        ProfileUpdateView.as_view(),
        name="profile_update",
    ),
    path(
        "accounts/profile/search",
        ProfileListView.as_view(),
        name="profile_list",
    ),
]
