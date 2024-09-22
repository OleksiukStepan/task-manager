from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .models import Worker

@receiver(user_logged_in)
def set_user_online(sender, user, request, **kwargs):
    if isinstance(user, Worker):
        user.is_online = True
        user.last_login = timezone.now()
        user.save(update_fields=['is_online', 'last_login'])
