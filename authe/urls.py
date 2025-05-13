from django.urls import path
from authe.views import register_view,login_view, control_user_view, control_lead_view, control_student_view, control_outcome_view, control_payment_view
from config.urls import schema_view

urlpatterns = [
    path('register/', register_view),
    path('login/', login_view),
    path('control/user/', control_user_view),
    path('control/lead/', control_lead_view),
    path('control/student/', control_student_view),
    path('control/outcome/', control_outcome_view),
    path('control/payment/', control_payment_view),
]

path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),