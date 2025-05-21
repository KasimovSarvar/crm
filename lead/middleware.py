from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from  django.http import JsonResponse
from django.urls import reverse
from lead.views import create_student


class BasicMiddleware(MiddlewareMixin):
    def process_view(self, request,view_func,view_args,view_kwargs):
        target_url = [reverse("create-student"),reverse('student-list')]
        if request.path in target_url:
            if request.user.role == 4:
                return redirect(reverse("create_student"),reverse('create_lead'),reverse('admin_create_student'),reverse('admin_lead_list'),reverse('lead_update'),reverse('admin_create_student'),reverse('student_detail'),reverse('update_payment_admin'),reverse('payment_list'),reverse('create_payment'),reverse('me'))( request, *view_args, **view_kwargs)
            elif request.user.role == 2:
                return redirect(reverse("create_lead"),reverse("create_user"),reverse("create_student"),reverse("change_lead_admin"),reverse("change_student_admin"),reverse("change_payment_admin"),reverse("lead_list"),reverse("student_list"),reverse("lead_update"),reverse("student_update"),reverse("me"),reverse("student_detail"))( request, *view_args, **view_kwargs)
            elif request.user.role == 3:
                return redirect(reverse("payment_list"),reverse("create_payment"),reverse('update_payment'),reverse('balance_report'),reverse('me'))( request, *view_args, **view_kwargs)

        return None