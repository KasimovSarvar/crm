from django.urls import path
from .views import (payment_list_admin, create_payment, balance_report, create_lead_view_admin,
                    lead_list_view_admin, student_list_view_admin, update_payment_admin, add_comment_view,
                    lead_update_view, create_student_view_admin, student_update_view, student_detail,
                    change_leads_admin_view, change_students_admin_view)

urlpatterns = [
    path('create_lead-admin/', create_lead_view_admin, name='create-lead-admin'),
    path('lead_list-admin/', lead_list_view_admin, name='lead-list-admin'),
    path('lead_update/<int:pk>/', lead_update_view, name='lead-update'),
    path('change_lead_admin/', change_leads_admin_view, name='change_lead_admin'),
    path('create_student-admin/<int:pk>/', create_student_view_admin, name='create-student-admin'),
    path('student_list-admin/', student_list_view_admin, name='student-list-admin'),
    path('change_student_admin/', change_students_admin_view, name='change_student_admin'),
    path('student_update/<int:pk>/', student_update_view, name='student-update'),
    path('student_detail/<int:pk>/', student_detail, name='student-detail'),
    path('create_payment/', create_payment, name='create-payment'),
    path('payment_list/', payment_list_admin, name='payment-list'),
    path('student/<int:student_id>/payment/<int:payment_id>/update/', update_payment_admin, name='update-payment-admin'),
    path('balance_report/', balance_report, name='balance-report'),
    path('add_comment/<int:pk>/', add_comment_view, name='add-comment'),
]