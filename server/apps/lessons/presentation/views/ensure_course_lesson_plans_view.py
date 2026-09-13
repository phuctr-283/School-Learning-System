from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.lessons.infrastructure.dependencies.course_lesson_plan_dependency import (
    ensure_course_lesson_plans_use_case,
)


class EnsureCourseLessonPlansView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):

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

        plans = (
            ensure_course_lesson_plans_use_case
            .execute(
                university_id=university_id,
            )
        )

        from apps.lessons.presentation.serializers.course_lesson_plan_serializer import (
            CourseLessonPlanResponseSerializer,
        )

        serializer = (
            CourseLessonPlanResponseSerializer(
                plans,
                many=True,
            )
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=200,
        )