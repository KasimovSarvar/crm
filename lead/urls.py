from django.urls import path
from . import views
from .views import is_accountant, payment_list, create_payment, update_payment, balance_report, create_lead_view, create_user_view, create_student_view, change_lead_admin_view, change_student_admin_view, lead_list_view, student_list_view ,lead_list, lead_update_view, create_student, my_students_list_view, student_update_view, student_detail

urlpatterns = [
    path('create/', create_lead_view, name='create-lead'),
    path('create_user/', create_user_view, name='create-user'),
    path('create_student/', create_student_view, name='create-student'),
    path('change_lead_admin/<int:lead_id>/', change_lead_admin_view, name='change-lead-admin'),      
    path('change_student_admin/<int:student_id>/', change_student_admin_view, name='change-student-admin'),
    path('lead_list/', lead_list_view, name='lead-list'),
    path('student_list/', student_list_view, name='student-list'),
    path('lead_list/<int:pk>/', lead_list, name='lead-list'),
    path('lead_update/<int:pk>/', lead_update_view, name='lead-update'),
    path('create_student/<int:pk>/', create_student, name='create-student'),
    path('my_students_list/', my_students_list_view, name='my-students-list'),
    path('student_update/<int:pk>/', student_update_view, name='student-update'),
    path('student_detail/<int:pk>/', student_detail, name='student-detail'),
    path('is_accountant/', is_accountant, name='is-accountant'),
    path('payment_list/', payment_list, name='payment-list'),
    path('create_payment/', create_payment, name='create-payment'),
    path('update_payment/<int:pk>/', update_payment, name='update-payment'),
    path('balance_report/', balance_report, name='balance-report'),
    path('lead_list/<int:pk>/', lead_list, name='lead-list'),
    path('lead_update/<int:pk>/', lead_update_view, name='lead-update'),
]