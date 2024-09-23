from django.utils import timezone


class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and hasattr(request.user, "is_online"):
            if request.user.is_online:
                request.user.last_login = timezone.now()
                request.user.save(update_fields=["last_login"])
        return response
