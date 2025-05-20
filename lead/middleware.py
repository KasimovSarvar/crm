from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from authe.models import User
from django.shortcuts import redirect
from rest_framework import status


from lead.views import create_student,update_payment_admin

class BasicMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # print(view_kwargs)
        # payment_id = view_kwargs.get("pk")
        # if not payment_id:
        #     return JsonResponse({"error": "Payment ID is required"}, status=status.HTTP_400_BAD_REQUEST)


        target_url = [reverse("create-student")]
        if request.path in target_url and request.user.is_authenticated:
            if request.user.role == 4:
                return redirect(reverse("create_student"))


        return None
