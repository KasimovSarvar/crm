from django.urls import path
from . import views

urlpatterns = [
    path('api/home/', views.home_view),

    path('api/register/', views.register_view),

    path('api/login/', views.login_view),

    path('api/control/user/', views.control_user_view),

    path('api/control/lead/', views.control_lead_view),

    path('api/control/student/', views.control_student_view),

    path('api/user/register/', views.user_register),
]