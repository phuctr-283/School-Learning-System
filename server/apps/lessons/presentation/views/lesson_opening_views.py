from rest_framework.views import APIView
from rest_framework.response import Response

from apps.lessons.infrastructure.dependencies.lesson_opening_dependency import (
    ensure_lesson_openings_use_case,
    get_lesson_openings_use_case,
)

from apps.lessons.presentation.serializers.lesson_opening_serializer import (
    LessonOpeningSerializer,
)


class EnsureLessonOpeningsView(APIView):

    def post(
        self,
        request,
    ):

        user_id = getattr(
            request.user,
            "user_id",
            None,
        )

        if not user_id:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Không xác định được tài khoản."
                    ),
                },
                status=401,
            )


        user = (
            request.user
        )


        university_id = getattr(
            user,
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
                ensure_lesson_openings_use_case
                .execute(
                    university_id=university_id,
                )
            )


            serializer = LessonOpeningSerializer(
                lesson_openings,
                many=True,
            )


            return Response(
                {
                    "success": True,

                    "message": (
                        "Đảm bảo danh sách buổi học "
                        "thành công."
                    ),

                    "created_count": len(
                        lesson_openings
                    ),

                    "data": serializer.data,
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


class GetLessonOpeningsView(APIView):

    def get(
        self,
        request,
        class_section_lesson_plan_id,
    ):

        user_id = getattr(
            request.user,
            "user_id",
            None,
        )

        if not user_id:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Không xác định được tài khoản."
                    ),
                },
                status=401,
            )


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


        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=400,
            )