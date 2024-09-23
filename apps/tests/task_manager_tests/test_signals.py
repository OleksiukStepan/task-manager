from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone

User = get_user_model()


class UserSignalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123", is_online=False
        )

    def test_set_user_online_signal(self):
        user_logged_in.send(sender=self.user.__class__, request=None, user=self.user)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_online)
        self.assertIsNotNone(self.user.last_login)
        self.assertAlmostEqual(
            self.user.last_login, timezone.now(), delta=timezone.timedelta(seconds=1)
        )
