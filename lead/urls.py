from django.urls import path
from .views import payment_list, create_payment, update_payment, balance_report, create_lead_view, \
    change_lead_admin_view, change_student_admin_view, lead_list_view, \
    student_list_view, admin_lead_view, lead_update_view, create_student_view, my_students_list_view, \
    student_update_view, student_detail, create_student, update_payment_admin,  add_comment_view,\
    student_list_view, admin_lead_view, lead_update_view, create_student_view, \
    student_update_view, student_detail, update_payment_admin, hr_lead_list_view, hr_student_list_view, hr_create_lead_view, hr_create_student_view


urlpatterns = [
    path('create_lead/', create_lead_view, name='create-lead'),
    path('create_student/', create_student_view, name='create-student'),
    path('change_lead_admin/<int:lead_id>/', change_lead_admin_view, name='change-lead-admin'),
    path('change_student_admin/<int:student_id>/', change_student_admin_view, name='change-student-admin'),
    path('lead_list/', lead_list_view, name='lead-list'),
    path('student_list/', student_list_view, name='student-list'),
    path('admin_lead_list/<int:pk>/', admin_lead_view, name='admin-lead-list'),
    path('lead_update/<int:pk>/', lead_update_view, name='lead-update'),
    # path('admin_create_student/', create_student, name='create-student'),
    path('student_update/<int:pk>/', student_update_view, name='student-update'),
    path('student_detail/<int:pk>/', student_detail, name='student-detail'),
    path('payment_list/', payment_list, name='payment-list'),
    path('create_payment/', create_payment, name='create-payment'),
    path('update_payment/<int:pk>/', update_payment, name='update-payment'),
    path('update_payment_admin/<int:pk>/', update_payment_admin, name='update-payment'),
    path('balance_report/', balance_report, name='balance-report'),
    path('add_comment/<int:lead_id>/', add_comment_view, name='add-comment'),
    path('hr_lead_list/', hr_lead_list_view, name='hr-lead-list'),
    path('hr_student_list/', hr_student_list_view, name='hr-student-list'),
    path('hr_create_lead/', hr_create_lead_view, name='hr-create-lead'),
    path('hr_create_student/<int:lead_id>/', hr_create_student_view, name='hr-create-student'),
]