from django.urls import path

from apps.lessons.presentation.views.get_lessons_view import (
    GetLessonsView,
)

from apps.lessons.presentation.views.get_semester_lesson_plans_view import (
    GetSemesterLessonPlansView,
)

from apps.lessons.presentation.views.get_subject_lesson_plans_view import (
    GetSubjectLessonPlansView,
)

from apps.lessons.presentation.views.get_class_section_lesson_plans_view import (
    GetClassSectionLessonPlansView,
)
from apps.lessons.presentation.views.get_course_lesson_plans_view import (
    GetCourseLessonPlansView,
)
from apps.lessons.presentation.views.create_lesson_view import CreateLessonView
from apps.lessons.presentation.views.create_subject_lesson_plan_view import (
    CreateSubjectLessonPlanView,
)
from apps.lessons.presentation.views.create_semester_lesson_plan_view import (
    CreateSemesterLessonPlanView,
)
from apps.lessons.presentation.views.ensure_course_lesson_plans_view import (
    EnsureCourseLessonPlansView,
)

from apps.lessons.presentation.views.ensure_class_section_lesson_plans_view import (
    EnsureClassSectionLessonPlansView,
)
from apps.lessons.presentation.views.ensure_lesson_plans_view import (
    EnsureLessonPlansView,
)
from apps.lessons.presentation.views.get_lesson_openings_view import (
    GetLessonOpeningsView,
)
from apps.lessons.presentation.views.update_lesson_opening_status_view import UpdateLessonOpeningStatusView
from apps.lessons.presentation.views.get_student_lessons_view import GetStudentLessonsView

urlpatterns = [
    path(
        "list/",
        GetLessonsView.as_view(),
        name="get-lessons",
    ),
    path(
        "create/",
        CreateLessonView.as_view(),
        name="create-lesson",
    ),
    path(
        "semester-plans/",
        GetSemesterLessonPlansView.as_view(),
        name="get-semester-lesson-plans",
    ),
    path(
        "semester-plans/create/",
        CreateSemesterLessonPlanView.as_view(),
        name="create-semester-lesson-plan",
    ),
    path(
        "subject-plans/",
        GetSubjectLessonPlansView.as_view(),
        name="get-subject-lesson-plans",
    ),
    path(
        "subject-plans/create/",
        CreateSubjectLessonPlanView.as_view(),
        name="get-subject-lesson-plans",
    ),
    path(
        "course-lesson-plans/",
        GetCourseLessonPlansView.as_view(),
        name="get-course-lesson-plans",
    ),
    path(
        "course-lesson-plans/<str:course_lesson_plan_id>/class-sections/",
        GetClassSectionLessonPlansView.as_view(),
        name="get-class-section-lesson-plans",
    ),
    path(
        "course-lesson-plans/ensure/",
        EnsureCourseLessonPlansView.as_view(),
        name="ensure-course-lesson-plans",
    ),
    path(
        "class-section-lesson-plans/ensure/",
        EnsureClassSectionLessonPlansView.as_view(),
        name="ensure-class-section-lesson-plans",
    ),
    path(
        "lesson-plans/ensure/",
        EnsureLessonPlansView.as_view(),
        name="ensure-lesson-plans",
    ),
    path(
        "lesson-openings/class-sections/<str:class_section_lesson_plan_id>/",
        GetLessonOpeningsView.as_view(),
        name="get-lesson-openings",
    ),
    path(
        "class-sections/<str:class_section_lesson_plan_id>/lesson-openings/<str:lesson_id>/status/",
        UpdateLessonOpeningStatusView.as_view(),
        name="update-lesson-opening-status"
    ),
    path(
    "student/class-sections/<str:class_section_id>/lessons/",
    GetStudentLessonsView.as_view(),
    name="student-class-section-lessons",
),
]
