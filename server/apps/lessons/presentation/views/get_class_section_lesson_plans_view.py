from rest_framework.views import APIView
from rest_framework.response import Response

from apps.lessons.presentation.serializers.class_section_lesson_plan_serializer import (
    ClassSectionLessonPlanResponseSerializer,
)

from apps.lessons.infrastructure.dependencies.class_section_lesson_plan_dependency import (
    get_class_section_lesson_plans_use_case,
)


class GetClassSectionLessonPlansView(APIView):

    def get(
        self,
        request,
        course_lesson_plan_id,
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

        if not course_lesson_plan_id:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Course lesson plan ID "
                        "không được để trống."
                    ),
                },
                status=400,
            )

        plans = (
            get_class_section_lesson_plans_use_case
            .execute(
                university_id=university_id,
                course_lesson_plan_id=course_lesson_plan_id,
            )
        )

        serializer = (
            ClassSectionLessonPlanResponseSerializer(
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