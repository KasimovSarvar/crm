# from django.urls import reverse
# from django.utils.deprecation import MiddlewareMixin
# from django.http import JsonResponse
# from authe.models import User
# from django.shortcuts import redirect
#
# class BasicMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         target_url = [reverse("register")]
#         if request.user.path in target_url:
#             if request.user.role == 1:
#                 return redirect(reverse("boshqa"))
