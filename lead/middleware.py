import base64
import json
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from  django.http import JsonResponse
from django.urls import reverse
from rest_framework import status
from authe.models import User
import jwt

from lead.views import payment_list, create_payment, update_payment, balance_report, create_lead_view, \
    change_lead_admin_view, change_student_admin_view, lead_list_view, \
    student_list_view, lead_update_view, create_student_view, \
    student_update_view, student_detail, create_student, update_payment_admin,  add_comment_view ,\
    student_list_view, lead_update_view, create_student_view, \
    student_update_view, student_detail, update_payment_admin, change_leads_admin_view, change_students_admin_view





class BasicMiddleware(MiddlewareMixin):
    def process_view(self, request,view_func,view_args,view_kwargs):
        if request.path == reverse("create-lead"):
            if request.user.role in  [1,2,4]:
                return create_lead_view(request,*view_args, **view_kwargs)
            return JsonResponse(data={"error": "You are not allowed to create leads"}, status=status.HTTP_400_BAD_REQUEST)

        if request.path == reverse("change-leads-admin"):
            if request.user.role  in [1,2]:
                return change_leads_admin_view(request,*view_args, **view_kwargs)
            return JsonResponse(data={"error": "You are not allowed to change leads"}, status=status.HTTP_400_BAD_REQUEST)


        if request.path == reverse("lead-list"):
            if request.user.role in [1,2]:
                return lead_list_view(request,*view_args, **view_kwargs)
            return JsonResponse(data={"error": "You are not allowed to list leads"}, status=status.HTTP_400_BAD_REQUEST)

        if request.path == reverse("create-student"):
            if request.user.role in [1,2]:
                return create_student_view(request,*view_args, **view_kwargs)
            return JsonResponse(data={"error": "You are not allowed to create students"}, status=status.HTTP_400_BAD_REQUEST)


        if request.path == reverse("change-students-admin"):
            if request.user.role in [1,2]:
                return change_students_admin_view(request,*view_args, **view_kwargs)
            return JsonResponse(data={"error": "You are not allowed to change students"}, status=status.HTTP_400_BAD_REQUEST)


        if request.path == reverse("student-list"):
            if request.user.role  in [1,2,4]:
                return student_list_view(request,*view_args, **view_kwargs)
            return JsonResponse(data={"error": "You are not allowed to list students"}, status=status.HTTP_400_BAD_REQUEST)

        if request.path == reverse("payment-list"):
            if request.user.role in [1,3,4]:
                return payment_list(request,*view_args, **view_kwargs)
            return JsonResponse(data={"error": "You are not allowed to list payments"}, status=status.HTTP_400_BAD_REQUEST)


        if request.path == reverse("create-payment"):
            if request.user.role in [1,3,4]:
                return create_payment(request,*view_args, **view_kwargs)
            return JsonResponse(data={"error": "You are not allowed to create payments"}, status=status.HTTP_400_BAD_REQUEST)


        if request.path == reverse("balance-report"):
            if request.user.role in [1,3]:
               return balance_report(request,*view_args, **view_kwargs)
            return JsonResponse(data={"error": "You are not allowed to balance report"}, status=status.HTTP_400_BAD_REQUEST)








        return None