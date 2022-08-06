"""Test Tickets Application Urls"""


from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Ticket, TicketCategory


# Create your tests here.
class TestTicketsUrlsUnauthenticatedUser(TestCase):
    def setUp(self):
        """Create a test user, ticket category and ticket for use in the
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

        ticket_category = TicketCategory.objects.create(name="Test Category")

        title = "Test Ticket"
        description = (
            "Non excepteur voluptate incididunt id cupidatat "
            "nostrud veniam non. Sint incididunt Lorem occaecat exercitation."
        )
        self.ticket = Ticket.objects.create(
            author=self.test_user_account,
            category=ticket_category,
            title=title,
            description=description,
        )

    def test_unauthenticated_ticket_list_redirects(self):
        """
        Tests url redirects to login page when unauthenticated.
        """
        response = self.client.get("/tickets/")
        self.assertRedirects(
            response,
            "/accounts/login/?next=/tickets/",
            status_code=302,
            target_status_code=200,
        )

    def test_unauthenticated_ticket_detail_redirects(self):
        """
        Tests url redirects to login page when unauthenticated.
        """
        response = self.client.get(f"/tickets/{self.ticket.id}/")
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/tickets/{self.ticket.id}/",
            status_code=302,
            target_status_code=200,
        )

    def test_unauthenticated_ticket_update_redirects(self):
        """
        Tests url redirects to login page when unauthenticated.
        """
        response = self.client.get(f"/tickets/{self.ticket.id}/edit")
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/tickets/{self.ticket.id}/edit",
            status_code=302,
            target_status_code=200,
        )


class TestUrlsAuthenticatedUser(TestCase):
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
        customer_account = get_user_model().objects.create_user(
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

        ticket_category = TicketCategory.objects.create(name="Test Category")

        shared_description = (
            "Non excepteur voluptate incididunt id cupidatat "
            "nostrud veniam non. Sint incididunt Lorem occaecat exercitation."
        )

        # create ticket with customer role as author
        title = "Test Customer Ticket"
        self.customer_ticket = Ticket.objects.create(
            author=customer_account,
            category=ticket_category,
            title=title,
            description=shared_description,
        )

        # create ticket with technician as author
        title = "Test Technician Ticket"
        self.technician_ticket = Ticket.objects.create(
            author=technician_account,
            category=ticket_category,
            title=title,
            description=shared_description,
        )

    def test_user_login_successful(self):
        """
        Tests login using the accounts created during setup is successful
        """
        self.assertTrue(
            self.client.login(
                username=self.customer_username, password=self.shared_password
            )
        )
        self.assertTrue(
            self.client.login(
                username=self.technician_username,
                password=self.shared_password,
            )
        )
        self.assertTrue(
            self.client.login(
                username=self.administrator_username,
                password=self.shared_password,
            )
        )

    def test_authenticated_ticket_list_resolves(self):
        """
        Tests url resolves when authenticated
        """
        self.assertTrue(
            self.client.login(
                username=self.customer_username, password=self.shared_password
            )
        )
        response = self.client.get("/tickets/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ticket_list.html")

    def test_authenticated_ticket_create_resolves(self):
        """
        Tests url resolves when authenticated
        """
        self.assertTrue(
            self.client.login(
                username=self.customer_username, password=self.shared_password
            )
        )
        response = self.client.get("/tickets/create/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ticket_create.html")

    # ticket_detail url
    def test_customer_is_author_ticket_detail_resolves(self):
        """
        Tests url resolves when authenticated as ticket author
        """
        self.assertTrue(
            self.client.login(
                username=self.customer_username, password=self.shared_password
            )
        )
        response_is_ticket_author = self.client.get(
            f"/tickets/{self.customer_ticket.id}/"
        )
        self.assertEqual(response_is_ticket_author.status_code, 200)
        self.assertTemplateUsed(
            response_is_ticket_author, "ticket_detail.html"
        )

    def test_customer_not_author_ticket_detail_refused(self):
        """
        Tests response is 403 when auth but not ticket author
        """
        self.assertTrue(
            self.client.login(
                username=self.customer_username, password=self.shared_password
            )
        )
        response_not_ticket_author = self.client.get(
            f"/tickets/{self.technician_ticket.id}/"
        )
        self.assertEqual(response_not_ticket_author.status_code, 403)

    def test_technician_not_author_ticket_detail_resolves(self):
        """
        Tests url resolves when auth as 'technician' role but not ticket author
        """
        self.assertTrue(
            self.client.login(
                username=self.technician_username,
                password=self.shared_password,
            )
        )
        response_not_ticket_author = self.client.get(
            f"/tickets/{self.customer_ticket.id}/"
        )
        self.assertEqual(response_not_ticket_author.status_code, 200)
        self.assertTemplateUsed(
            response_not_ticket_author, "ticket_detail.html"
        )

    # ticket_update
    def test_customer_is_author_ticket_update_resolves(self):
        """
        Tests url resolves when authenticated as ticket author.
        """
        self.assertTrue(
            self.client.login(
                username=self.customer_username, password=self.shared_password
            )
        )
        response_is_ticket_author = self.client.get(
            f"/tickets/{self.customer_ticket.id}/edit"
        )
        self.assertEqual(response_is_ticket_author.status_code, 200)
        self.assertTemplateUsed(
            response_is_ticket_author, "ticket_update.html"
        )

    def test_customer_not_author_ticket_update_refused(self):
        """
        Tests response is 403 when auth but not ticket author
        """
        self.assertTrue(
            self.client.login(
                username=self.customer_username, password=self.shared_password
            )
        )
        response_not_ticket_author = self.client.get(
            f"/tickets/{self.technician_ticket.id}/edit"
        )
        self.assertEqual(response_not_ticket_author.status_code, 403)

    def test_technician_not_author_ticket_update_resolves(self):
        """
        Tests url resolves when auth as 'technician' role but not ticket author
        """
        self.assertTrue(
            self.client.login(
                username=self.technician_username,
                password=self.shared_password,
            )
        )
        response_not_ticket_author = self.client.get(
            f"/tickets/{self.customer_ticket.id}/"
        )
        self.assertEqual(response_not_ticket_author.status_code, 200)
        self.assertTemplateUsed(
            response_not_ticket_author, "ticket_detail.html"
        )
