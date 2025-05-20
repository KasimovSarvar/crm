from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from  django.http import JsonResponse
from django.urls import reverse
from lead.views import create_student


class BasicMiddleware(MiddlewareMixin):
    def process_view(self, request,view_func,view_args,view_kwargs):
        target_url = [reverse("create-student")]
        if request.path in target_url:
            if request.user.role == 4:
                return redirect(reverse(create_student()))( request, *view_args, **view_kwargs)

        return None