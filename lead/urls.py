from django.urls import path
from .views import payment_list, create_payment, update_payment, balance_report, create_lead_view, lead_list_view, \
    student_list_view, lead_update_view, create_student_view, \
    student_update_view, student_detail, create_student, update_payment_admin,  add_comment_view ,\
    student_list_view, lead_update_view, create_student_view, \
    student_update_view, student_detail, update_payment_admin, change_leads_admin_view, change_students_admin_view


urlpatterns = [
    path('create_lead/', create_lead_view, name='create-lead'),
    path('create_student/', create_student_view, name='create-student'),
    path('change_leads_admin/', change_leads_admin_view, name='change-leads-admin'),
    path("chang_students_admin/", change_students_admin_view, name="change-students-admin"),
    path('lead_list/', lead_list_view, name='lead-list'),
    path('student_list/', student_list_view, name='student-list'),
    path('lead_update/<int:pk>/', lead_update_view, name='lead-update'),
    path('student_update/<int:pk>/', student_update_view, name='student-update'),
    path('student_detail/<int:pk>/', student_detail, name='student-detail'),
    path('payment_list/', payment_list, name='payment-list'),
    path('create_payment/', create_payment, name='create-payment'),
    path('update_payment/<int:pk>/', update_payment, name='update-payment'),
    path('student/<int:student_id>/payment/<int:payment_id>/update/', update_payment_admin, name='update-payment-admin'),
    path('balance_report/', balance_report, name='balance-report'),
    path('add_comment/<int:pk>/', add_comment_view, name='add-comment'),
]