from django.urls import path
from .views import demo_home_page_view


urlpatterns = [
    path("", demo_home_page_view, name="home"),
]
