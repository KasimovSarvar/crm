from django.http import JsonResponse
import jwt
from django.conf import settings
from .models import User

class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if not auth_header.startswith('Bearer '):
                return JsonResponse({"detail": "Unauthorized"}, status=401)

            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            role = payload.get("role")

            user = User.objects.get(id=user_id)
            request.user = user
            request.user_role = role

        except jwt.ExpiredSignatureError:
            return JsonResponse({"detail": "Access token expired, use refresh token to get a new access token."}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"detail": "Unauthorized"}, status=401)
        except User.DoesNotExist:
            return JsonResponse({"detail": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=500)

        return self.get_response(request)