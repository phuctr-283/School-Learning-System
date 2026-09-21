from django.urls import path

from apps.class_sections.presentation.views.get_class_sections_view import (
    GetClassSectionsView
)
from apps.class_sections.presentation.views.import_class_section_view import ImportClassSectionView
from apps.class_sections.presentation.views.get_teacher_subjects_view import (
    GetTeacherSubjectsView,
)

from apps.class_sections.presentation.views.get_teacher_class_section_views import (
    GetTeacherClassSectionsView,
)
from apps.class_sections.presentation.views.get_student_class_section_view import (
    GetStudentClassSectionsView
)

from apps.class_sections.presentation.views.class_section_student_view import ImportClassSectionStudentsByTeacherView
from apps.class_sections.presentation.views.get_teacher_active_subjects_view import GetTeacherActiveSubjectsView
from apps.class_sections.presentation.views.get_teacher_active_planned_subjects_view import GetTeacherActivePlannedSubjectsView
from apps.class_sections.presentation.views.get_teacher_active_planned_class_sections_view import GetTeacherActivePlannedClassSectionsView
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
        "teacher/active-subjects/",
        GetTeacherActiveSubjectsView.as_view(),
        name="teacher-active-subjects",
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
    path(
        "student/class-sections/",
        GetStudentClassSectionsView.as_view(),
        name="student-subjects",
    ),
    path(
        "teacher/academic-year/<str:academic_year_id>/semester/<str:semester_id>/subjects",
        GetTeacherActivePlannedSubjectsView.as_view(),
        name="get-teacher-active-planned-subjects",
    ),
    path(
        "teacher/academic-year/<str:academic_year_id>/semester/<str:semester_id>/subjects/<str:subject_id>/class-sections/",
        GetTeacherActivePlannedClassSectionsView.as_view(),
        name="get-teacher-active-planned-class-sections"
    ),
]