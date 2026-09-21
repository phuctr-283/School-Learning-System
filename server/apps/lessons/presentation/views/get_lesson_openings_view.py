from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.lessons.infrastructure.dependencies.lesson_opening_dependency import (
    get_lesson_openings_use_case,
)

from apps.lessons.presentation.serializers.lesson_opening_serializer import (
    LessonOpeningSerializer,
)


class GetLessonOpeningsView(
    APIView
):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
        class_section_lesson_plan_id,
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

            lesson_openings = (
                get_lesson_openings_use_case
                .execute(
                    university_id=university_id,
                    class_section_lesson_plan_id=(
                        class_section_lesson_plan_id
                    ),
                )
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=400,
            )

        serializer = LessonOpeningSerializer(
            lesson_openings,
            many=True,
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=200,
        )