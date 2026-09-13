from django.urls import path

from apps.students.presentation.views.get_students_view import (
    GetStudentsView,
)
from apps.students.presentation.views.import_students_view import ImportStudentsView
urlpatterns = [
    path(
        "list/",
        GetStudentsView.as_view(),
        name="student-list",
    ),
    path(
        "import/",
        ImportStudentsView.as_view(),
        name="student-import",
    ),
]
