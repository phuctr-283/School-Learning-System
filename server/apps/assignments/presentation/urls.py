from django.urls import path

from apps.assignments.presentation.views.create_assignment_view import (
    CreateAssignmentView,
)

from apps.assignments.presentation.views.get_assignments_view import (
    GetAssignmentsView,
)

from apps.assignments.presentation.views.get_assignments_by_subject_view import (
    GetAssignmentsBySubjectView,
)

from apps.assignments.presentation.views.get_assignment_content_view import (
    GetAssignmentContentView,
)
from apps.assignments.presentation.views.apply_assignment_view import (
    ApplyAssignmentView,
)
from apps.assignments.presentation.views.get_assignment_applications_view import (
    GetAssignmentApplicationsView,
)
from apps.assignments.presentation.views.update_assignment_application_class_section_status_view import (
    UpdateAssignmentApplicationClassSectionStatusView,
)
from apps.assignments.presentation.views.verify_student_assignment_qr_view import (
    VerifyStudentAssignmentQrView,
)
from apps.assignments.presentation.views.student_assignment_view import (
    GetStudentAssignmentView,
    SaveStudentAssignmentView,
    SubmitStudentAssignmentView,
)
from apps.assignments.infrastructure.dependencies.student_assignment_dependencies import (
    get_student_assignment_use_case,
    get_save_student_assignment_use_case,
    get_submit_student_assignment_use_case,
)

urlpatterns = [
    path(
        "create/",
        CreateAssignmentView.as_view(),
        name="create-assignment",
    ),
    path(
        "list/",
        GetAssignmentsView.as_view(),
        name="get-assignments",
    ),
    path(
        "list/<str:subject_id>/",
        GetAssignmentsBySubjectView.as_view(),
        name="assignments-by-subject",
    ),
    path(
        "apply/",
        ApplyAssignmentView.as_view(),
        name="apply-assignment",
    ),
    path(
        "applications/",
        GetAssignmentApplicationsView.as_view(),
        name="get-assignment-applications",
    ),
    path(
        "student/qr/verify/",
        VerifyStudentAssignmentQrView.as_view(),
        name="verify-student-assignment-qr",
    ),
    path(
        "student/take/",
        GetStudentAssignmentView.as_view(
            get_use_case=(get_student_assignment_use_case())
        ),
        name="student-assignment-take",
    ),
    path(
        "student/take/save/",
        SaveStudentAssignmentView.as_view(
            save_use_case=(get_save_student_assignment_use_case())
        ),
        name="student-assignment-save",
    ),
    path(
        "student/take/submit/",
        SubmitStudentAssignmentView.as_view(
            submit_use_case=(get_submit_student_assignment_use_case())
        ),
        name="student-assignment-submit",
    ),
    path(
        "<str:assignment_id>/",
        GetAssignmentContentView.as_view(),
        name="get-assignment-content",
    ),
    path(
        "applications/<str:assignment_application_id>/class-sections/<str:class_section_id>/status/",
        UpdateAssignmentApplicationClassSectionStatusView.as_view(),
        name="update-assignment-application-class-section-status",
    ),
]
