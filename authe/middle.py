from django.shortcuts import HttpResponse
from .models import User


class CustomUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the user_id from session or header
        user_id = request.session.get("user_id")  # Or from header: request.headers.get("X-USER-ID")

        if user_id:
            try:
                request.user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                request.user = None
        else:
            request.user = None

        # Continue processing the request
        response = self.get_response(request)
        return response




