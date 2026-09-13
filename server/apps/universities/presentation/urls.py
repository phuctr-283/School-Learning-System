from django.urls import path

from apps.universities.presentation.views.create_university_view import (
    CreateUniversityView,
)

from apps.universities.presentation.views.get_universities_view import (
    GetUniversitiesView,
)
from apps.universities.presentation.views.get_active_universities_view import GetActiveUniversityView


urlpatterns = [

    path(
        "create/",
        CreateUniversityView.as_view(),
        name="create-university",
    ),

    path(
        "list/",
        GetUniversitiesView.as_view(),
        name="get-universities",
    ),
    path(
        "active/",
        GetActiveUniversityView.as_view(),
        name="active-universities",
    ),
]