from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.lessons.presentation.serializers.semester_lesson_plan_serializer import (
    SemesterLessonPlanSerializer,
)
from apps.lessons.presentation.serializers.create_semester_lesson_plan_serializer import (CreateSemesterLessonPlanItemSerializer,CreateSemesterLessonPlanSerializer)

from apps.lessons.application.dto.create_semester_lesson_plan_dto import (
    CreateSemesterLessonPlanDTO,
    CreateSemesterLessonPlanItemDTO,
)


from apps.lessons.infrastructure.dependencies.semester_lesson_plan_dependency import (
    create_semester_lesson_plan_use_case
)


class CreateSemesterLessonPlanView(APIView):
    permission_classes = [
            IsAuthenticated,
        ]
    def post(self, request):

        serializer = CreateSemesterLessonPlanSerializer(data=request.data)

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": "Dữ liệu không hợp lệ.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        university_id = request.user.university_id

        semesters = [
            CreateSemesterLessonPlanItemDTO(
                semester_number=item["semester_number"],
                total_lessons=item["total_lessons"],
            )
            for item in (serializer.validated_data["semesters"])
        ]

        dto = CreateSemesterLessonPlanDTO(
            academic_year_id=(serializer.validated_data["academic_year_id"]),
            semesters=semesters,
        )

        try:

            use_case = create_semester_lesson_plan_use_case

            plans = use_case.execute(
                university_id,
                dto,
            )

            return Response(
                {
                    "success": True,
                    "message": ("Tạo kế hoạch học kỳ " "thành công."),
                    "data": [SemesterLessonPlanSerializer(plan).data for plan in plans],
                },
                status=status.HTTP_201_CREATED,
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
                "CREATE SEMESTER LESSON PLAN ERROR:",
                error,
            )

            return Response(
                {
                    "success": False,
                    "message": ("Không thể tạo kế hoạch " "học kỳ."),
                },
                status=(status.HTTP_500_INTERNAL_SERVER_ERROR),
            )
