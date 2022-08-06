"""Test Tickets Application Views"""


from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from ..models import Ticket, TicketCategory
from django.urls import reverse


class TestUrlsAuthenticated(TestCase):
    def setUp(self):
        """Create test users encompassing all roles, a ticket category and 2
        tickets with different authors.

        customer_account: (accounts.models.CustomUser)
        technician_account: (accounts.models.CustomUser)
        administrator_account: (accounts.models.CustomUser)
        ticket_category: (tickets.models.TicketCategory)
        customer_ticket: (tickets.models.Ticket) - Ticket object with the
        'customer_account' ('customer' role) as it's author.
        technician_ticket: (tickets.models.Ticket) - Ticket object with the
        'technician_account' ('technician' role) as it's author.
        """

        # Create users
        self.shared_password = "testingPa$$w0rd!"

        self.customer_username = "customer_account"
        self.customer_account = get_user_model().objects.create_user(
            username=self.customer_username,
            password=self.shared_password,
            role=get_user_model().ROLES.customer,
        )
        self.technician_username = "technician_account"
        technician_account = get_user_model().objects.create_user(
            username=self.technician_username,
            password=self.shared_password,
            role=get_user_model().ROLES.technician,
        )
        self.administrator_username = "administrator_account"
        get_user_model().objects.create_user(
            username=self.administrator_username,
            password=self.shared_password,
            role=get_user_model().ROLES.administrator,
        )

        self.ticket_category = TicketCategory.objects.create(
            name="test category"
        )

        # create ticket with customer role as author
        self.shared_description = (
            "Non excepteur voluptate incididunt id cupidatat "
            "nostrud veniam non. Sint incididunt Lorem occaecat exercitation."
        )

        self.title = "Test Customer Ticket"
        self.customer_ticket = Ticket.objects.create(
            author=self.customer_account,
            category=self.ticket_category,
            title=self.title,
            description=self.shared_description,
        )

        # create ticket with technician as author
        title = "Test Technician Ticket"
        self.technician_ticket = Ticket.objects.create(
            author=technician_account,
            category=self.ticket_category,
            title=title,
            description=self.shared_description,
        )

    def test_ticket_creation(self):
        """
        Test a ticket can be created when auth as 'customer' role
        """

        expected_success_message = "Ticket created successfully."
        initial_number_of_tickets = Ticket.objects.all().count()

        self.assertTrue(
            self.client.login(
                username=self.customer_username, password=self.shared_password
            )
        )
        response = self.client.post(
            reverse("ticket_create"),
            data={
                "author": self.customer_account,
                "type": Ticket.TYPE.request,
                "category": self.ticket_category.id,
                "title": self.title,
                "description": self.shared_description,
            },
        )
        self.assertEquals(
            Ticket.objects.all().count(), initial_number_of_tickets + 1
        )
        self.assertEquals(
            str(list(response.wsgi_request._messages)[0]),
            expected_success_message,
        )

    def test_ticket_deletion(self):
        """
        Test a ticket can be deleted when auth as 'technician' role
        """

        # get the first ticket for deletion
        ticket = Ticket.objects.all()[0]
        expected_success_message = (
            f"Request #{ticket.id} deleted successfully."
        )
        initial_number_of_tickets = Ticket.objects.all().count()

        self.client = Client(HTTP_HOST="127.0.0.1:8000")
        self.assertTrue(
            self.client.login(
                username=self.technician_username,
                password=self.shared_password,
            )
        )
        response = self.client.post(f"/tickets/{ticket.id}/delete")

        # Should be 1 less ticket than when the test started
        self.assertEquals(
            Ticket.objects.all().count(), initial_number_of_tickets - 1
        )
        self.assertEquals(
            str(list(response.wsgi_request._messages)[0]),
            expected_success_message,
        )

    def test_ticket_deletion_refused(self):
        """
        Test a ticket cannot be deleted when auth as 'customer' role
        """

        # get the first ticket for deletion
        ticket = Ticket.objects.all()[0]
        expected_message = "You do not have permission to delete this request."
        initial_number_of_tickets = Ticket.objects.all().count()

        self.client = Client(HTTP_HOST="127.0.0.1:8000")
        self.assertTrue(
            self.client.login(
                username=self.customer_username,
                password=self.shared_password,
            )
        )
        response = self.client.post(f"/tickets/{ticket.id}/delete")

        # Should be the same number of tickets as when the test started
        self.assertEquals(
            Ticket.objects.all().count(), initial_number_of_tickets
        )
        self.assertEquals(
            str(list(response.wsgi_request._messages)[0]),
            expected_message,
        )
