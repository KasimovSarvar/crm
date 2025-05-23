from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from  django.http import JsonResponse
from django.urls import reverse
from authe.views import me_view
from lead.views import payment_list, create_payment, update_payment, balance_report, create_lead_view, \
    change_lead_admin_view, change_student_admin_view, lead_list_view, \
    student_list_view, lead_update_view, create_student_view, \
    student_update_view, student_detail, create_student, update_payment_admin,  add_comment_view ,\
    student_list_view, lead_update_view, create_student_view, \
    student_update_view, student_detail, update_payment_admin, change_leads_admin_view, change_students_admin_view


# reverse("change-lead-admin",kwargs=view_kwargs),reverse("lead-update"),reverse("change-student-admin"),reverse("student-update"),reverse("student-detail"),reverse("update-payment"),reverse("update-payment-admin"),reverse("add-comment")]

class BasicMiddleware(MiddlewareMixin):
    def process_view(self, request,view_func,view_args,view_kwargs):
        if request.path == reverse("create-lead"):
            if request.user.role in  [1,2,4]:
                return create_lead_view(request,*view_args, **view_kwargs)

        if request.path == reverse("change-leads-admin"):
            if request.user.role  in [1,2]:
                return change_leads_admin_view(request,*view_args, **view_kwargs)

        if request.path == reverse("lead-list"):
            if request.user.role in [1,2]:
                return lead_list_view(request,*view_args, **view_kwargs)
        if request.path == reverse("create-student"):
            if request.user.role in [1,2]:
                return create_student_view(request,*view_args, **view_kwargs)

        if request.path == reverse("change-students-admin"):
            if request.user.role in [1,2]:
                return change_students_admin_view(request,*view_args, **view_kwargs)

        if request.path == reverse("student-list"):
            if request.user.role  in [1,2,4]:
                return student_list_view(request,*view_args, **view_kwargs)

        if request.path == reverse("payment-list"):
            if request.user.role in [1,3,4]:
                return payment_list(request,*view_args, **view_kwargs)

        if request.path == reverse("create-payment"):
            if request.user.role in [1,3,4]:
                return create_payment(request,*view_args, **view_kwargs)

        if request.path == reverse("balance-report"):
            if request.user.role in [1,3]:
                return balance_report(request,*view_args, **view_kwargs)
            return JsonResponse(data={"hone":"mumkinmas"})




        return None