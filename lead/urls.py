from django.urls import path
from .views import payment_list, create_payment, update_payment, balance_report, create_lead_view, \
    change_lead_admin_view, change_student_admin_view, lead_list_view, \
    student_list_view, lead_update_view, create_student_view, \
    student_update_view, student_detail, create_student, update_payment_admin,  add_comment_view ,\
    student_list_view, lead_update_view, create_student_view, \
    student_update_view, student_detail, update_payment_admin, change_leads_admin_view, change_students_admin_view


urlpatterns = [
    # Lead
    path('lead/create/', create_lead_view, name='create-lead'),
    path('lead/change_admin/<int:lead_id>/', change_lead_admin_view, name='change-lead-admin'),
    path('lead/change_admins/', change_leads_admin_view, name='change-leads-admin'),
    path('lead/list/', lead_list_view, name='lead-list'),
    path('lead/update/<int:pk>/', lead_update_view, name='lead-update'),

    # Student
    path('student/create/', create_student_view, name='create-student'),
    path('student/change_admin/<int:student_id>/', change_student_admin_view, name='change-student-admin'),
    path('student/change_admins/', change_students_admin_view, name='change-students-admin'),
    path('student/list/', student_list_view, name='student-list'),
    path('student/update/<int:pk>/', student_update_view, name='student-update'),
    path('student/detail/<int:pk>/', student_detail, name='student-detail'),

    # Payment
    path('payment/list/', payment_list, name='payment-list'),
    path('payment/create/', create_payment, name='create-payment'),
    path('payment/update/<int:pk>/', update_payment, name='update-payment'),
    path('student/<int:student_id>/payment/<int:payment_id>/update/', update_payment_admin, name='update-payment-admin'),

    # Boshqa
    path('balance_report/', balance_report, name='balance-report'),
    path('comment/add/<int:pk>/', add_comment_view, name='add-comment'),
]