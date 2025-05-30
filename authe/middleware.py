from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from  django.http import JsonResponse
from django.urls import reverse
from rest_framework import status
from authe.models import User
import jwt
from lead.views import (payment_list_admin, payment_list_hr, create_payment, update_payment_admin,
                        update_payment, balance_report, create_lead_view_admin, create_lead_view_hr,
                        lead_list_view_admin, lead_list_view_hr, student_list_view_admin, student_list_view_hr,
                        lead_update_view, change_leads_admin_view, student_detail, student_detail_view,
                        create_student_view_admin, create_student_view_hr, add_comment_view,
                        student_update_view, change_students_admin_view,
)


class RoleCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.lstrip('/')

        if path.startswith('login/') or path.startswith('swagger/') or path == "" or path.startswith("admin/") or path.startswith("create_user/") or path.startswith("balance_report/"):
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
            except User.DoesNotExist:
                return JsonResponse({"detail": "User not found"}, status=404)

            user.role = role
            request.user = user

        except jwt.ExpiredSignatureError:
            return JsonResponse({"detail": "Access token expired, use refresh token to get a new access token."}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"detail": "Invalid token"}, status=401)

        return self.get_response(request)


class BasicMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        role = getattr(request.user, "role", None)
        pk_id = view_kwargs.get("pk")
        student_id = view_kwargs.get("student_id")
        payment_id = view_kwargs.get("payment_id")

        if pk_id is not None and request.path == reverse("create-student-admin", kwargs={"pk": pk_id}):
            if role == 4:
                return create_student_view_admin(request, *view_args, **view_kwargs)
            elif role in [1, 2]:
                return create_student_view_hr(request, *view_args, **view_kwargs)
            return JsonResponse({"error": "You cannot create"}, status=400)

        if pk_id is not None and request.path == reverse("lead-update", kwargs={"pk": pk_id}):
            if role == 4:
                return lead_update_view(request, *view_args, **view_kwargs)
            return JsonResponse({"error": "You cannot update"}, status=400)

        if pk_id is not None and request.path == reverse("student-update", kwargs={"pk": pk_id}):
            if role == 4:
                return student_update_view(request, *view_args, **view_kwargs)
            return JsonResponse({"error": "You cannot update"}, status=400)

        if pk_id is not None and request.path == reverse("student-detail", kwargs={"pk": pk_id}):
            if role == 4:
                return student_detail(request, *view_args, **view_kwargs)
            elif role in [1, 2]:
                return student_detail_view(request, *view_args, **view_kwargs)
            return JsonResponse({"error": "You cannot detail"}, status=400)

        if student_id is not None and payment_id is not None and request.path == reverse("update-payment-admin", kwargs={"student_id": student_id, "payment_id": payment_id}):
            if role == 4:
                return update_payment_admin(request, *view_args, **view_kwargs)
            elif role in [1, 3]:
                return update_payment(request, *view_args, **view_kwargs)
            return JsonResponse({"error": "You cannot update"}, status=400)

        if pk_id is not None and request.path == reverse("add-comment", kwargs={"pk": pk_id}):
            if role == 4:
                return add_comment_view(request, *view_args, **view_kwargs)
            return JsonResponse({"error": "You cannot add"}, status=400)


        if request.path == reverse("create-lead-admin"):
            if role == 4:
                return create_lead_view_admin(request, *view_args, **view_kwargs)
            elif role in [1, 2]:
                return create_lead_view_hr(request, *view_args, **view_kwargs)
            return JsonResponse({"error": "You are not allowed to create leads"},status=status.HTTP_400_BAD_REQUEST)

        if request.path == reverse("lead-list-admin"):
            if role == 4:
                return lead_list_view_admin(request, *view_args, **view_kwargs)
            elif role in [1, 2]:
                return lead_list_view_hr(request, *view_args, **view_kwargs)
            return JsonResponse({"error": "You are not allowed to list leads"}, status=status.HTTP_400_BAD_REQUEST)

        if request.path == reverse("change_lead_admin"):
            if role in [1, 2]:
                return change_leads_admin_view(request, *view_args, **view_kwargs)
            return JsonResponse({"error": "You are not allowed to change leads admin"}, status=status.HTTP_400_BAD_REQUEST)

        if request.path == reverse("student-list-admin"):
            if role == 4:
                return student_list_view_admin(request, *view_args, **view_kwargs)
            elif role in [1, 2]:
                return student_list_view_hr(request, *view_args, **view_kwargs)
            return JsonResponse({"error": "You are not allowed to list students"},status=status.HTTP_400_BAD_REQUEST)

        if request.path == reverse("change_student_admin"):
            if role in [1, 2]:
                return change_students_admin_view(request, *view_args, **view_kwargs)
            return JsonResponse({"error": "You are not allowed to change students admin"},status=status.HTTP_400_BAD_REQUEST)

        if request.path == reverse("payment-list"):
            if role == 4:
                return payment_list_admin(request, *view_args, **view_kwargs)
            elif role in [1, 2, 3]:
                return payment_list_hr(request, *view_args, **view_kwargs)
            return JsonResponse({"error": "You are not allowed to list payments"},status=status.HTTP_400_BAD_REQUEST)

        if request.path == reverse("create-payment"):
            if role in [1, 3, 4]:
                return create_payment(request, *view_args, **view_kwargs)
            return JsonResponse({"error": "You are not allowed to create payments"}, status=status.HTTP_400_BAD_REQUEST)

        if request.path == reverse("balance-report"):
            if role in [1, 2, 3]:
                return balance_report(request, *view_args, **view_kwargs)
            return JsonResponse({"error": "You are not allowed to view balance report"}, status=status.HTTP_400_BAD_REQUEST)

        return None
