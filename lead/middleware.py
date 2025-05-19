from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from authe.models import User
from django.shortcuts import redirect

from lead.views import update_payment_admin


# path('update_payment/<int:pk>/', update_payment, update_payment_admin, name='update-payment'),







class BasicMiddleware(MiddlewareMixin):
    def process_request(self, request):
        target_url = [reverse("update-payment")]
        if request.path in target_url and request.user.is_authenticated:
            if request.user.role == 4:
                return redirect(reverse(update_payment_admin()))

        return None
