from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from apps.lessons.application.dto.create_lesson_dto import (
    CreateLessonDTO,
)

from apps.lessons.presentation.serializers.create_lesson_serializer import (
    CreateLessonSerializer,
)

from apps.lessons.infrastructure.dependencies.lesson_dependency import (
    create_lesson_use_case,
)


class CreateLessonView(
    APIView,
):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(
        self,
        request,
    ):

        # =====================================================
        # UNIVERSITY
        # =====================================================

        university_id = getattr(
            request.user,
            "university_id",
            None,
        )

        if not university_id:

            return Response(
                {
                    "success": False,
                    "message": ("Không xác định được trường đại học."),
                },
                status=400,
            )

        # =====================================================
        # SERIALIZER
        # =====================================================

        serializer = CreateLessonSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        data = serializer.validated_data

        # =====================================================
        # DTO
        # =====================================================

        dto = CreateLessonDTO(
            create_mode=data.get(
                "create_mode",
            ),
            lesson_number=data.get(
                "lesson_number",
            ),
            lesson_number_start=data.get(
                "lesson_number_start",
            ),
            lesson_number_end=data.get(
                "lesson_number_end",
            ),
        )

        # =====================================================
        # USE CASE
        # =====================================================

        try:

            lessons = create_lesson_use_case.execute(
                dto=dto,
                university_id=university_id,
            )

            # =================================================
            # RESPONSE
            # =================================================

            return Response(
                {
                    "success": True,
                    "message": ("Tạo buổi học thành công."),
                    "data": [
                        {
                            "lesson_id": (lesson.lesson_id),
                            "lesson_number": (lesson.lesson_number),
                            "name": (lesson.name),
                            "university_id": (lesson.university_id),
                        }
                        for lesson in lessons
                    ],
                },
                status=201,
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

            print(
                "CREATE LESSON ERROR:",
                error,
            )

            return Response(
                {
                    "success": False,
                    "message": ("Không thể tạo buổi học."),
                },
                status=500,
            )
