# from django.http import JsonResponse
# from django.urls import reverse
# from django.utils.deprecation import MiddlewareMixin
# from rest_framework import status
# from authe.models import User
#
#
# # from django.utils.chek_token import get_role, validate_token
#
# #
#
# class SimpleTest(MiddlewareMixin):
#     def proccess_request(self, request):
#         target_url = [reverse('ordinary')]
#         if target_url in request.path:
#             if User.password == "d":
#                 print(User.username)
#                 return JsonResponse(data={'message': 'Hello, World!'}, status=status.HTTP_200_OK)
#         return None
#
#
#
#
#
#
#
#
# class AuthenticationRoleBasedRedirectMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         # Target URLs where authentication is needed
#         exclude_target_url = [reverse('login'), reverse('region'), reverse('district'), reverse('lead_template_create')]
#         if request.path.startswith('/api/v1/') and request.path not in exclude_target_url:
#             # Check token validity
#             payload = validate_token(request.headers.get('Authorization'))
#
#             if payload is None:
#                 return JsonResponse(data={'result': "", "error": "Unauthorized access", 'ok': False}, status=401)
#         return None
#
#
#
# class HRStatisticsRoleBasedRedirectMiddleware(MiddlewareMixin):
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         target_urls = [reverse('hr_statistics_admin'), reverse('hr_statistics_month'),
#                        reverse('hr_statistics_total'), reverse('hr_statistics_chart'), reverse('distribution_leads')]
#         if request.path in target_urls:
#             role = get_role(request.headers.get('Authorization'))
#
#             if role in [1, 2, 6]:
#                 return view_func(request, *view_args, **view_kwargs)
#             return JsonResponse(data={"result": "", "error": "Permission denied", 'ok': False}, status=403)
#         return None
#
#
#
#
# class LeadDetailRoleBasedRedirectMiddleware(MiddlewareMixin):
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         student_id = view_kwargs.get('pk')
#         if student_id is None:
#             return None
#         target_urls = reverse(viewname='detail_admin', kwargs={'pk': student_id})
#         if request.path in target_urls:
#             role = get_role(request.headers.get('Authorization'))
#
#             if role in [1, 2, 6]:
#                 return LeadViewSet.as_view({"get": "lead_detail_others", 'patch': 'lead_update_other'})(
#                     request, *view_args, **view_kwargs)
#             if role in [4]:
#                 return LeadViewSet.as_view({"get": "lead_detail_admin", 'patch': 'lead_update_admin'})(
#                     request, *view_args, **view_kwargs)
#             return JsonResponse(data={"result": "", "error": "Permission denied", 'ok': False}, status=403)
#         return None


