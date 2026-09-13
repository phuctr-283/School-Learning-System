from django.urls import path

from apps.subjects.presentation.views.get_subjects_view import (
    GetSubjectsView,
)
from apps.subjects.presentation.views.create_subject_view import CreateSubjectView

urlpatterns = [
    path(
        "list/",
        GetSubjectsView.as_view(),
        name="get-subjects",
    ),
    path(
        "create/",
        CreateSubjectView.as_view(),
        name="subject-create",
    ),
]
