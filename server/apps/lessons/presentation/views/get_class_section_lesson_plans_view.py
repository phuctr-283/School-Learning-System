from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.lessons.infrastructure.dependencies.class_section_lesson_plan_dependency import (
    get_class_section_lesson_plans_use_case,
)

from apps.lessons.presentation.serializers.class_section_lesson_plan_serializer import (
    ClassSectionLessonPlanResponseSerializer,
)


class GetClassSectionLessonPlansView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

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
                    "message": ("Tài khoản không thuộc " "trường đại học."),
                },
                status=400,
            )

        if not course_lesson_plan_id:

            return Response(
                {
                    "success": False,
                    "message": ("Course lesson plan ID " "không được để trống."),
                },
                status=400,
            )

        try:

            plans = get_class_section_lesson_plans_use_case.execute(
                university_id=university_id,
                course_lesson_plan_id=(course_lesson_plan_id),
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=400,
            )

        serializer = ClassSectionLessonPlanResponseSerializer(
            plans,
            many=True,
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=200,
        )
