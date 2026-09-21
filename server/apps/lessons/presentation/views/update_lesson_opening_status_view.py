from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.lessons.infrastructure.dependencies.lesson_opening_dependency import (
    update_lesson_opening_status_use_case,
)

from apps.lessons.presentation.serializers.class_section_lesson_plan_serializer import (
    ClassSectionLessonPlanResponseSerializer,
)


class UpdateLessonOpeningStatusView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def patch(
        self,
        request,
        class_section_lesson_plan_id,
        lesson_id,
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

        status = request.data.get("status")

        try:

            plan = update_lesson_opening_status_use_case.execute(
                university_id=university_id,
                class_section_lesson_plan_id=(class_section_lesson_plan_id),
                lesson_id=lesson_id,
                status=status,
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=400,
            )

        serializer = ClassSectionLessonPlanResponseSerializer(plan)

        return Response(
            {
                "success": True,
                "message": ("Cập nhật trạng thái buổi học " "thành công."),
                "data": serializer.data,
            },
            status=200,
        )
