from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.lessons.infrastructure.dependencies.get_student_lessons_dependency import (
    get_student_class_section_lesson_use_case,
)

from apps.lessons.presentation.serializers.student_class_section_lesson_plan_serializer import (
    StudentClassSectionLessonPlanSerializer,
)


class GetStudentLessonsView(APIView):

    def get(
        self,
        request,
        class_section_id,
    ):

        try:

            user = request.user

            student_id = getattr(
                user,
                "student_id",
                None,
            )

            university_id = getattr(
                user,
                "university_id",
                None,
            )

            if not student_id:
                return Response(
                    {
                        "success": False,
                        "message": "Không xác định được mã sinh viên.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if not university_id:
                return Response(
                    {
                        "success": False,
                        "message": "Không xác định được trường đại học.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            lesson_plan = get_student_class_section_lesson_use_case.execute(
                student_id=student_id,
                university_id=university_id,
                class_section_id=class_section_id,
            )

            serializer = StudentClassSectionLessonPlanSerializer(lesson_plan)

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

        except Exception as error:

            print(
                "GET STUDENT LESSONS ERROR:",
                error,
            )

            return Response(
                {
                    "success": False,
                    "message": "Không thể tải danh sách buổi học.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
