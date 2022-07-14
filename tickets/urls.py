from django.urls import path
from .views import TicketListView, TicketCreateView


urlpatterns = [
    path("", TicketListView.as_view(), name="ticket_list"),
    path("create/", TicketCreateView.as_view(), name="ticket_create"),
]
