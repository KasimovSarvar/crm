from django.http import JsonResponse
import jwt
from django.conf import settings
from .models import User

ROLE_ACCESS = {
    1: "*",  
    2: ['register/', 'create_lead/', 'create_user/', 'create_student/', 'change_lead_admin/', 'change_student_admin/',
    'lead_list/', 'student_list/', 'lead_update/', 'student_update/', 'student_detail/',  ],
    3: ['payment_list/', 'create_payment/', 'update_payment/', 'balance_report/'],
    4: ['admin_create_student/', 'admin_lead_list/', 'lead_update/', 'create_student/',
    'my_students_list/', 'student_detail/', ], 
}

class RoleCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        if path.startswith('/login/') or path.startswith('/swagger/') or path.startswith("/")  or path.startswith("/admin/"):
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

            allowed_roles = ROLE_ACCESS.get(role, [])
            if allowed_roles == "*": 
                return self.get_response(request)

            if not any(path.startswith(p) for p in allowed_roles):
                return JsonResponse({"detail": "You do not have permission to access this resource."}, status=403)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"detail": "Access token expired, use refresh token to get a new access token."}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"detail": "Invalid token"}, status=401)

        return self.get_response(request)
