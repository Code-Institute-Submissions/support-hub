"""Test Tickets Application Forms"""


from django.test import TestCase
from ..forms import CustomerTicketCreationForm


class TestCustomerTicketCreationFormValidation(TestCase):
    """
    Test form validation requires a 'title' with min 10 chars
    """
    def test_ticket_title_minimum_10_characters_required(self):
        form = CustomerTicketCreationForm({"title": "123456789"})
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors.keys())
        self.assertIn(
            "Ensure this value has at least 10 characters",
            form.errors["title"][0],
        )

    def test_ticket_title_minimum_20_characters_required(self):
        """
        Test form validation requires a 'description' with min 20 chars
        """
        form = CustomerTicketCreationForm(
            {"description": "1234567890123456789"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors.keys())
        self.assertIn(
            (
                "Field must be at least 20 characters long, "
                "you have so far entered"
            ),
            form.errors["description"][0],
        )
