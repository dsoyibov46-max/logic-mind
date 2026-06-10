from django.urls import path
from .views import (
    profile_settings,
    index,
    register_view,
    login_view,
    logout_view,
    student_dashboard,
    teacher_dashboard,
    parent_dashboard,
    teacher_student_detail,   # 👈 SHUNI QO‘SH
    group_create,
    group_detail,
    assignment_create,
)


urlpatterns = [
    path('dashboard/teacher/assignments/create/', assignment_create, name='assignment_create'),
    path('dashboard/teacher/groups/create/', group_create, name='group_create'),
    path('dashboard/teacher/groups/<int:group_id>/', group_detail, name='group_detail'),
    path('profile/settings/', profile_settings, name='profile_settings'),
    path('', index, name='index'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
   path('dashboard/teacher/student/<int:student_id>/',
        teacher_student_detail,
    name='teacher_student_detail'),
    

    path('dashboard/student/', student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/parent/', parent_dashboard, name='parent_dashboard'),
]