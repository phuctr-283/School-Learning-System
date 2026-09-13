from rest_framework.views import APIView
from rest_framework.response import Response

from apps.lessons.presentation.serializers.course_lesson_plan_serializer import (
    CourseLessonPlanResponseSerializer,
)

from apps.lessons.infrastructure.dependencies.course_lesson_plan_dependency import (
    get_course_lesson_plans_use_case,
)


class GetCourseLessonPlansView(APIView):

    def get(self, request):

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

        use_case = (
            get_course_lesson_plans_use_case
        )

        plans = use_case.execute(
            university_id=university_id,
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