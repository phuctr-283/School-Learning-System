from django.urls import path

from apps.departments.presentation.views.get_university_departments_view import (
    GetUniversityDepartmentsView,
)

from apps.departments.presentation.views.create_department_view import (
    CreateDepartmentView,
)
from apps.departments.presentation.views.get_active_departments_by_university_view import (
    GetActiveDepartmentsByUniversityView,
)
from apps.departments.presentation.views.get_active_departments_view import GetActiveDepartmentsView
urlpatterns = [
    path(
        "list/",
        GetUniversityDepartmentsView.as_view(),
        name="get-university-departments",
    ),
    path(
        "create/",
        CreateDepartmentView.as_view(),
        name="create-department",
    ),
    path(
        "active/",
        GetActiveDepartmentsByUniversityView.as_view(),
        name="active-departments",
    ),
    path(
        "actives/",
        GetActiveDepartmentsView.as_view(),
        name="department-active",
    ),
]
