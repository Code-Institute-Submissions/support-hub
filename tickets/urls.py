from django.urls import path
from .views import TicketListView, TicketCreateView, TicketDetailView


urlpatterns = [
    path("", TicketListView.as_view(), name="ticket_list"),
    path("create/", TicketCreateView.as_view(), name="ticket_create"),
    path("<slug:pk>/", TicketDetailView.as_view(), name="ticket_detail"),
]
