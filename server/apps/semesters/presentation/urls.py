from django.urls import path

from apps.semesters.presentation.views.get_semesters_view import (
    GetSemestersView,
)
from apps.semesters.presentation.views.create_semester_view import CreateSemesterView
from apps.semesters.presentation.views.get_active_planned_semesters_view import GetActivePlannedSemestersView
urlpatterns = [

    path(
        "list/",
        GetSemestersView.as_view(),
        name="semester-list",
    ),
    path(
        "create/",
        CreateSemesterView.as_view(),
        name="semester-create",
    ),
    path(
        "active-planned/",
        GetActivePlannedSemestersView.as_view(),
        name="active-planned-semesters",
    ),
]