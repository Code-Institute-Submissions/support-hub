"""Test Tickets Application Models"""


from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Ticket, TicketCategory


class TestTicketDefaults(TestCase):
    def setUp(self):
        """Create a test user, ticket category and ticket

        TestTicketsUrlsUnauthenticated class.

        test_user_account: (accounts.models.CustomUser)
        ticket_category: (tickets.models.TicketCategory)
        ticket: (tickets.models.Ticket) - Ticket object with the
        'test_user_account' (customer role) as it's author
        """
        self.test_user_username = "test-user"
        self.password = "testingPa$$w0rd!"
        self.test_user_account = get_user_model().objects.create_user(
            username=self.test_user_username,
            password=self.password,
            role=get_user_model().ROLES.customer,
        )

        self.ticket_category = TicketCategory.objects.create(
            name="Test Category"
        )

    def test_ticket_type_defaults_to_request(self):
        """
        Test ticket type defaults to 'request'
        """

        title = "Test Ticket"
        description = (
            "Non excepteur voluptate incididunt id cupidatat "
            "nostrud veniam non. Sint incididunt Lorem occaecat exercitation."
        )
        ticket = Ticket.objects.create(
            author=self.test_user_account,
            category=self.ticket_category,
            title=title,
            description=description,
        )

        self.assertEquals(ticket.type, "request")
