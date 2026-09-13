from django.urls import path

from apps.academic_years.presentation.views.get_academic_years_view import (
    GetAcademicYearsView,
)
from apps.academic_years.presentation.views.create_academic_year_view import CreateAcademicYearView
from apps.academic_years.presentation.views.get_active_and_planned_academic_years import GetActiveAndPlannedAcademicYearsView

urlpatterns = [

    path(
        "list/",
        GetAcademicYearsView.as_view(),
        name="academic-year-list",
    ),
    path(
        "create/",
        CreateAcademicYearView.as_view(),
        name="academic-year-create",
    ),
    path(
        "active-planned/",
        GetActiveAndPlannedAcademicYearsView.as_view(),
        name="academic-year-active-planned",
    ),
]