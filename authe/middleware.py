from django.http import JsonResponse
import jwt
from django.conf import settings
from .models import User 

ROLE_ACCESS = {
    '/admin/': [1,2],
    '/accountant/': [1, 3],
    '/admin-restricted/': [1, 4],
}

class RoleCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # Разрешённые публичные пути
        if path.startswith('/login/') or path.startswith('/swagger/'):
            return self.get_response(request)

        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({"detail": "Authorization header missing or malformed."}, status=401)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            if payload.get("type") != "access":
                return JsonResponse({"detail": "Invalid token type"}, status=401)

            user_id = payload.get("user_id")
            role = payload.get("role")

            try:
                request.user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({"detail": "User not found"}, status=404)

            request.user_role = role

            # Проверка доступа
            for allowed_path, allowed_roles in ROLE_ACCESS.items():
                if path.startswith(allowed_path):
                    if role not in allowed_roles:
                        return JsonResponse({"detail": "You do not have permission to access this resource."}, status=403)
                    break  # если нашлось соответствие — выйти

        except jwt.ExpiredSignatureError:
            return JsonResponse({"detail": "Access token expired, use refresh token to get a new access token."}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"detail": "Invalid token"}, status=401)

        return self.get_response(request)
