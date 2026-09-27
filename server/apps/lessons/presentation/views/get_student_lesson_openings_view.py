from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.lessons.infrastructure.dependencies.lesson_opening_dependency import (
    get_student_lesson_openings_use_case,
)
from apps.lessons.presentation.serializers.lesson_opening_serializer import (
    LessonOpeningSerializer,
)


class GetStudentLessonOpeningsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(
        self,
        request,
        class_section_id,
    ):

        university_id = getattr(
            request.user,
            "university_id",
            None,
        )

        student_id = getattr(
            request.user,
            "username",
            None,
        )

        if not university_id:
            return Response(
                {
                    "success": False,
                    "message": "Thiếu mã trường.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not student_id:
            return Response(
                {
                    "success": False,
                    "message": "Thiếu mã sinh viên.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            lesson_openings = get_student_lesson_openings_use_case.execute(
                university_id=university_id,
                class_section_id=class_section_id,
                student_id=student_id,
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
                status=status.HTTP_200_OK,
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception:

            import traceback

            traceback.print_exc()

            return Response(
                {
                    "success": False,
                    "message": ("Không thể tải danh sách buổi học."),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
