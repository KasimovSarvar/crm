from django.urls import path
from . import views
from .views import lead_list, lead_update_view, create_student, my_students_list_view, student_update_view, student_detail

urlpatterns = [
    path('lead_list/', lead_list, name='lead-list'),
    path('my_students/', my_students_list_view, name='my-students-list'),
    path('create/', create_student, name='create-student'),
    path('update/<int:pk>/', lead_update_view, name='lead-update'),
    path('student/update/<int:pk>/', student_update_view, name='student-update'),
    path('student/<int:pk>/', student_detail, name='student-detail'),
    path('student/<int:pk>/update/', student_update_view, name='student-update'),
]