from django.urls import path

from apps.assignments.presentation.views.create_assignment_view import (
    CreateAssignmentView,
)

from apps.assignments.presentation.views.get_assignments_view import (
    GetAssignmentsView,
)


urlpatterns = [
    path(
        "create/",
        CreateAssignmentView.as_view(),
        name="create-assignment",
    ),

    path(
        "/",
        GetAssignmentsView.as_view(),
        name="get-assignments",
    ),
]