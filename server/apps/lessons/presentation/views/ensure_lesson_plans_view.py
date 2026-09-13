from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.lessons.infrastructure.dependencies.lesson_dependency import (
    ensure_lesson_plans_dependency,
)

from apps.lessons.presentation.serializers.course_lesson_plan_serializer import (
    CourseLessonPlanResponseSerializer,
)

from apps.lessons.presentation.serializers.class_section_lesson_plan_serializer import (
    ClassSectionLessonPlanResponseSerializer,
)


class EnsureLessonPlansView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(
        self,
        request,
    ):

        university_id = getattr(
            request.user,
            "university_id",
            None,
        )

        if not university_id:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Tài khoản không thuộc "
                        "trường đại học."
                    ),
                },
                status=400,
            )

        try:

            result = (
                ensure_lesson_plans_dependency.execute(
                    university_id=university_id,
                )
            )

            course_lesson_plans = (
                CourseLessonPlanResponseSerializer(
                    result["course_lesson_plans"],
                    many=True,
                ).data
            )

            class_section_lesson_plans = (
                ClassSectionLessonPlanResponseSerializer(
                    result[
                        "class_section_lesson_plans"
                    ],
                    many=True,
                ).data
            )

            return Response(
                {
                    "success": True,
                    "data": {
                        "course_lesson_plans": (
                            course_lesson_plans
                        ),
                        "class_section_lesson_plans": (
                            class_section_lesson_plans
                        ),
                    },
                },
                status=200,
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=400,
            )

        except Exception as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=500,
            )