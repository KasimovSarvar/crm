from django.urls import path
from .views import payment_list_admin, create_payment, update_payment, balance_report, create_lead_view_admin, create_lead_view_hr, lead_list_view_admin, lead_list_view_hr, \
    student_list_view_admin, lead_update_view, create_student_view_hr, \
    student_detail, create_student, update_payment_admin, add_comment_view, \
    student_list_view_hr, lead_update_view, create_student_view_admin, \
    student_update_view, student_detail, update_payment_admin, change_leads_admin_view, change_students_admin_view, \
    payment_list_hr

urlpatterns = [
    path('create_lead-admin/', create_lead_view_admin, name='create-lead-admin'),
    path('create_lead-hr/', create_lead_view_hr, name='create-lead-hr'),
    path('create_student-admin/<int:lead_id>/', create_student_view_admin, name='create-student-admin'),
    path('create_student-hr/<int:lead_id>/', create_student_view_hr, name='create-student-hr'),
    path('change_lead_admin/', change_leads_admin_view, name='change-leads-admin'),
    path("change_student_admin/", change_students_admin_view, name="change-students-admin"),
    path('lead_list-admin/', lead_list_view_admin, name='lead-list-admin'),
    path('lead_list-hr/', lead_list_view_hr, name='lead-list-hr'),
    path('student_list-admin/', student_list_view_admin, name='student-list-admin'),
    path('student_list-hr/', student_list_view_hr, name='student-list-hr'),
    path('lead_update/<int:pk>/', lead_update_view, name='lead-update'),
    path('student_update/<int:pk>/', student_update_view, name='student-update'),
    path('student_detail/<int:pk>/', student_detail, name='student-detail'),
    path('payment_list/', payment_list_admin, name='payment-list'),
    path('create_payment/', create_payment, name='create-payment'),
    path('update_payment/<int:pk>/', update_payment, name='update-payment'),
    path('student/<int:student_id>/payment/<int:payment_id>/update/', update_payment_admin, name='update-payment-admin'),
    path('balance_report/', balance_report, name='balance-report'),
    path('add_comment/<int:pk>/', add_comment_view, name='add-comment'),
]
