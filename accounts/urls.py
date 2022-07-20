from django.urls import path
from .views import demo_home_page_view, ProfileDetailView


urlpatterns = [
    path("", demo_home_page_view, name="home"),
    path(
        "accounts/<slug:pk>/",
        ProfileDetailView.as_view(),
        name="profile_detail",
    ),
]
