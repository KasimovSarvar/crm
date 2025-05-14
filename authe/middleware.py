from django.http import JsonResponse
from django.conf import settings
from .models import User
import jwt

ROLE_ACCESS = {
    1: "*",  
    2: [
        'register/', 'create/', 'create_user/', 'create_student/',
        'change_lead_admin/', 'change_student_admin/',
        'lead_list/', 'student_list/', 'lead_update/', 'student_update/', 'student_detail/',
    ],
    3: [
        'payment_list/', 'create_payment/', 'update_payment/', 'balance_report/',
    ],
    4: [
        'create_student/', 'amdin_lead_list/', 'lead_update/',
        'my_students_list/', 'student_detail/',
    ],
}

class RoleCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.lstrip('/') 

        if path.startswith('login/') or path.startswith('swagger/') or path == '' or path.startswith('register/'):
            return self.get_response(request)

        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({"detail": "Authorization header missing or malformed."}, status=401)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            user_id = payload.get("user_id")
            role = payload.get("role")

            try:
                user = User.objects.get(id=user_id)
                request.user = user
                request.user_role = role
            except User.DoesNotExist:
                return JsonResponse({"detail": "User not found"}, status=404)

            allowed_paths = ROLE_ACCESS.get(role, [])
            if allowed_paths == "*":
                return self.get_response(request)

            if not any(path.startswith(p) for p in allowed_paths):
                return JsonResponse({"detail": "You do not have permission to access this resource."}, status=403)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"detail": "Access token expired, use refresh token to get a new one."}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"detail": "Invalid token"}, status=401)

        return self.get_response(request)
