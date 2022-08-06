"""Test Accounts Application Urls"""


from django.test import TestCase
from django.contrib.auth import get_user_model


class TestAccountsUrls(TestCase):
    def setUp(self):
        """Create test users with the customer and administrator roles.

        customer_account: (accounts.models.CustomUser)
        administrator_account: (accounts.models.CustomUser)
        """

        self.shared_password = "testingPa$$w0rd!"

        self.customer_username = "customer_account"
        self.customer_account = get_user_model().objects.create_user(
            username=self.customer_username,
            password=self.shared_password,
            role=get_user_model().ROLES.customer,
        )
        self.administrator_username = "administrator_account"
        self.administrator_account = get_user_model().objects.create_user(
            username=self.administrator_username,
            password=self.shared_password,
            role=get_user_model().ROLES.administrator,
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
                username=self.administrator_username,
                password=self.shared_password,
            )
        )

    # Anonymous url tests
    def test_home_page_resolves(self):
        """Test home page url resolves"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_login_page_resolves(self):
        """Test login page url resolves"""
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/login.html")

    def test_signup_page_resolves(self):
        """Test signup page url resolves"""
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup.html")

    def test_unauthenticated_profile_detail_redirects(self):
        response = self.client.get(
            f"/accounts/profile/{self.customer_account.id}/"
        )
        self.assertRedirects(
            response,
            (
                "/accounts/login/?next=/accounts/profile/"
                f"{self.customer_account.id}/"
            ),
            status_code=302,
            target_status_code=200,
        )

    def test_unauthenticated_profile_edit_redirects(self):
        """
        Tests url redirects to login page when unauthenticated.
        """
        response = self.client.get(
            f"/accounts/profile/{self.customer_account.id}/edit"
        )
        self.assertRedirects(
            response,
            (
                "/accounts/login/?next=/accounts/profile/"
                f"{self.customer_account.id}/edit"
            ),
            status_code=302,
            target_status_code=200,
        )

    def test_unauthenticated_profile_search_redirects(self):
        """
        Tests url redirects to login page when unauthenticated.
        """
        response = self.client.get("/accounts/profile/search")
        self.assertRedirects(
            response,
            "/accounts/login/?next=/accounts/profile/search",
            status_code=302,
            target_status_code=200,
        )

    # Authenticated url tests
    def test_login_page_redirects_when_authenticated(self):
        """
        Tests url redirects to home page when authenticated.
        """
        self.assertTrue(
            self.client.login(
                username=self.customer_username, password=self.shared_password
            )
        )
        response = self.client.get("/accounts/login/")
        self.assertRedirects(
            response, "/", status_code=302, target_status_code=200
        )

    def test_customer_view_own_profile_resolves(self):
        """
        Tests url resolves when authenticated as profile owner
        """
        self.assertTrue(
            self.client.login(
                username=self.customer_username, password=self.shared_password
            )
        )
        response_is_profile_owner = self.client.get(
            f"/accounts/profile/{self.customer_account.id}/"
        )
        self.assertEqual(response_is_profile_owner.status_code, 200)
        self.assertTemplateUsed(
            response_is_profile_owner, "profile_detail.html"
        )

    def test_customer_view_others_profile_refused(self):
        """
        Tests response is 403 when auth but not profile owner
        """
        self.assertTrue(
            self.client.login(
                username=self.customer_username, password=self.shared_password
            )
        )
        response_not_profile_owner = self.client.get(
            f"/accounts/profile/{self.administrator_account.id}/"
        )
        self.assertEqual(response_not_profile_owner.status_code, 403)

    def test_customer_edit_own_profile_resolves(self):
        """
        Tests url resolves when auth as 'administrator' role but not owner
        """
        self.assertTrue(
            self.client.login(
                username=self.customer_username, password=self.shared_password
            )
        )
        response_is_profile_owner = self.client.get(
            f"/accounts/profile/{self.customer_account.id}/edit"
        )
        self.assertEqual(response_is_profile_owner.status_code, 200)
        self.assertTemplateUsed(
            response_is_profile_owner, "profile_update.html"
        )

    def test_customer_edit_others_profile_refused(self):
        """
        Tests response is 403 when auth but not profile owner
        """
        self.assertTrue(
            self.client.login(
                username=self.customer_username, password=self.shared_password
            )
        )
        response_not_profile_owner = self.client.get(
            f"/accounts/profile/{self.administrator_account.id}/edit"
        )
        self.assertEqual(response_not_profile_owner.status_code, 403)

    def test_administrator_view_all_profiles_resolves(self):
        """
        Tests url resolves when auth as 'administrator' role but not owner
        """
        self.assertTrue(
            self.client.login(
                username=self.administrator_username,
                password=self.shared_password,
            )
        )
        response_not_profile_owner = self.client.get(
            f"/accounts/profile/{self.customer_account.id}/"
        )
        self.assertEqual(response_not_profile_owner.status_code, 200)
        self.assertTemplateUsed(
            response_not_profile_owner, "profile_detail.html"
        )

    def test_customer_view_profile_search_refused(self):
        """
        Tests response is 403 when auth as 'customer' role
        """
        self.assertTrue(
            self.client.login(
                username=self.customer_username, password=self.shared_password
            )
        )
        response_not_profile_owner = self.client.get(
            "/accounts/profile/search"
        )
        self.assertEqual(response_not_profile_owner.status_code, 403)

    def test_administrator_view_profile_search_resolves(self):
        """
        Tests url resolves when auth as 'administrator' role
        """
        self.assertTrue(
            self.client.login(
                username=self.administrator_username,
                password=self.shared_password,
            )
        )
        response_not_profile_owner = self.client.get(
            "/accounts/profile/search"
        )
        self.assertEqual(response_not_profile_owner.status_code, 200)
        self.assertTemplateUsed(
            response_not_profile_owner, "profile_list.html"
        )
