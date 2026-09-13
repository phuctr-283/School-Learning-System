from django.urls import path

from apps.teachers.presentation.views.get_university_teachers_view import (
    GetUniversityTeachersView,
)
from apps.teachers.presentation.views.register_teacher_view import RegisterTeacherView

urlpatterns = [
    path(
        "list/",
        GetUniversityTeachersView.as_view(),
        name="university-teachers-list",
    ),
    path(
        "register/",
        RegisterTeacherView.as_view(),
        name="register-teacher",
    ),
]
