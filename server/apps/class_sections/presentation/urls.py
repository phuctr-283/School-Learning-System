from django.urls import path

from apps.class_sections.presentation.views.get_class_sections_view import (
    GetClassSectionsView
)
from apps.class_sections.presentation.views.import_class_section_view import ImportClassSectionView
from apps.class_sections.presentation.views.get_teacher_subject_views import (
    GetTeacherSubjectsView,
)

from apps.class_sections.presentation.views.get_teacher_class_section_views import (
    GetTeacherClassSectionsView,
)
from apps.class_sections.presentation.views.class_section_student_view import ImportClassSectionStudentsByTeacherView
urlpatterns = [

    path(
        "list/",
        GetClassSectionsView.as_view(),
        name="class-section-list",
    ),
    path(
        "import/",
        ImportClassSectionView.as_view(),
        name="class-section-import",
    ),
    path(
        "teacher/subjects/",
        GetTeacherSubjectsView.as_view(),
        name="get-teacher-subjects",
    ),

    path(
        "teacher/subjects/<str:subject_id>/class-sections/",
        GetTeacherClassSectionsView.as_view(),
        name="get-teacher-class-sections",
    ),
    path(
        "students/import/",
        ImportClassSectionStudentsByTeacherView.as_view(),
        name="import-class-section-students",
    ),
]