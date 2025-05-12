from django.contrib.auth.views import LoginView
from django.urls import path
from  authe.views import home_view,register_view,login_view,control_user_view,control_lead_view,control_student_view
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
urlpatterns = [
    path('', home_view),
    path('register/', register_view),
    path('login/', login_view),
    path('control/user/', control_user_view),
    path('control/lead/', control_lead_view),
    path('control/student/', control_student_view),
]