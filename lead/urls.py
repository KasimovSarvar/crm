from .views import create_lead_view
from django.urls import path

urlpatterns = [
    path("create-lead", create_lead_view)
]