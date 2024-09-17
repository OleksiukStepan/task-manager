import datetime
from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name="is_online")
def check_online_status(last_login):
    """Return 'online' if last_login was within the last 15 minutes, else 'offline'."""
    if last_login:
        now = timezone.now()
        online_threshold = now - datetime.timedelta(minutes=15)
        if last_login > online_threshold:
            return True
    return False
