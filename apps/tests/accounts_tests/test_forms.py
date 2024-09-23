from django.test import TestCase
from apps.accounts.forms import LoginForm, SignUpForm
from apps.task_manager.models import Worker


class LoginFormTests(TestCase):
    def test_login_form_valid_data(self):
        form = LoginForm(
            data={
                "username": "testuser",
                "password": "testpassword",
                "remember_me": True,
            }
        )
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password", form.errors)

    def test_login_form_field_attributes(self):
        form = LoginForm()
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"], "Username"
        )
        self.assertEqual(form.fields["username"].widget.attrs["class"], "form-control")
        self.assertEqual(
            form.fields["password"].widget.attrs["placeholder"], "Password"
        )
        self.assertEqual(form.fields["password"].widget.attrs["class"], "form-control")


class SignUpFormTests(TestCase):
    def setUp(self):
        # Create a test user if needed for tests
        self.user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "newpassword123",
            "password2": "newpassword123",
            "agree_terms": True,
        }

    def test_signup_form_valid_data(self):
        form = SignUpForm(data=self.user_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid_data(self):
        # Test case where password confirmation does not match
        invalid_data = self.user_data.copy()
        invalid_data["password2"] = "differentpassword"
        form = SignUpForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_signup_form_without_agreeing_terms(self):
        # Test case where terms and conditions are not agreed upon
        invalid_data = self.user_data.copy()
        invalid_data["agree_terms"] = False
        form = SignUpForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("agree_terms", form.errors)
        self.assertEqual(
            form.errors["agree_terms"][0],
            "You must agree to the terms & conditions to register",
        )

    def test_signup_form_field_attributes(self):
        form = SignUpForm()
        # Check attributes of username field
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"], "Username"
        )
        self.assertEqual(form.fields["username"].widget.attrs["class"], "form-control")

        # Check attributes of email field
        self.assertEqual(form.fields["email"].widget.attrs["placeholder"], "Email")
        self.assertEqual(form.fields["email"].widget.attrs["class"], "form-control")

        # Check attributes of password1 field
        self.assertEqual(
            form.fields["password1"].widget.attrs["placeholder"], "Password"
        )
        self.assertEqual(form.fields["password1"].widget.attrs["class"], "form-control")

        # Check attributes of password2 field
        self.assertEqual(
            form.fields["password2"].widget.attrs["placeholder"], "Password check"
        )
        self.assertEqual(form.fields["password2"].widget.attrs["class"], "form-control")

        # Check attributes of agree_terms field
        self.assertEqual(
            form.fields["agree_terms"].widget.attrs["class"], "form-check-input"
        )

    def test_signup_form_email_validation(self):
        # Test case with an invalid email
        invalid_email_data = self.user_data.copy()
        invalid_email_data["email"] = "invalidemail"
        form = SignUpForm(data=invalid_email_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_signup_form_duplicate_username(self):
        # Create a user to test duplicate username validation
        Worker.objects.create_user(
            username="existinguser",
            email="existinguser@example.com",
            password="password",
        )
        duplicate_username_data = self.user_data.copy()
        duplicate_username_data["username"] = "existinguser"
        form = SignUpForm(data=duplicate_username_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
