from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class UpdateLastActivityMiddlewareTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123", is_online=True
        )

    def test_middleware_updates_last_login(self):
        self.client.login(username="testuser", password="password123")
        last_login_before = self.user.last_login
        self.client.get(reverse("task_manager:home"))
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.last_login, last_login_before)
        self.assertTrue(self.user.is_online)
