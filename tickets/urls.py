from django.urls import path
from .views import (
    TicketListView,
    TicketCreateView,
    TicketDetailView,
    TicketUpdateView,
)


urlpatterns = [
    path("", TicketListView.as_view(), name="ticket_list"),
    path("create/", TicketCreateView.as_view(), name="ticket_create"),
    path("<slug:pk>/", TicketDetailView.as_view(), name="ticket_detail"),
    path("<slug:pk>/edit", TicketUpdateView.as_view(), name="ticket_update"),
]
