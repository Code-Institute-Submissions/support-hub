"""URLs for tickets application"""


from django.urls import path
from .views import (
    TicketListView,
    TicketCreateView,
    TicketView,
    TicketUpdateView,
    TicketDeleteView,
)


urlpatterns = [
    path("", TicketListView.as_view(), name="ticket_list"),
    path("create/", TicketCreateView.as_view(), name="ticket_create"),
    path("<slug:pk>/", TicketView.as_view(), name="ticket_detail"),
    path("<slug:pk>/edit", TicketUpdateView.as_view(), name="ticket_update"),
    path("<slug:pk>/delete", TicketDeleteView.as_view(), name="ticket_delete"),
]
