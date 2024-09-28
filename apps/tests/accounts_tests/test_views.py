from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()


class LoginViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )

    def test_login_view_get(self):
        # Test GET request to the login view
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_login_view_post_valid_credentials(self):
        # Test POST request with valid credentials
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "testuser",
                "password": "testpassword",
                "remember_me": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_post_invalid_credentials(self):
        # Test POST request with invalid credentials
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "wronguser",
                "password": "wrongpassword",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid credentials")


class RegisterUserTests(TestCase):
    def test_register_user_get(self):
        # Test GET request to the registration view
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_register_user_post_valid_form(self):
        # Test POST request with valid form data
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "newpassword_123",
                "password2": "newpassword_123",
                "agree_terms": True,
            },
        )

        # Debugging: Check if form errors are causing the issue
        if response.status_code == 200:
            print("Form errors:", response.context["form"].errors)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_user_post_invalid_form(self):
        # Test POST request with invalid form data
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "",
                "password1": "password",
                "password2": "differentpassword",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Form is not valid")


class ResetPasswordTests(TestCase):
    def setUp(self):
        # Create a test user and log them in
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_reset_password_view_get(self):
        # Test GET request to the reset password view
        response = self.client.get(reverse("accounts:reset_password"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/reset_password.html")

    def test_reset_password_view_post(self):
        # Test POST request with valid data to change the password
        response = self.client.post(
            reverse("accounts:reset_password"),
            {
                "old_password": "testpassword",
                "new_password1": "newpassword123",
                "new_password2": "newpassword123",
            },
        )
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("Your password was successfully changed!" in str(m) for m in messages)
        )

    def test_login_view_session_expiry_default(self):
        # Test POST request without remember_me to check default session expiry
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "testuser",
                "password": "testpassword",
                "remember_me": False,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(
            response.wsgi_request.session.get_expiry_age(), 7 * 24 * 60 * 60
        )
