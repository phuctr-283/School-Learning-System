from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.semesters.presentation.serializers.create_semester_serializer import (
    CreateSemesterSerializer,
)

from apps.semesters.presentation.serializers.semester_serializer import (
    SemesterSerializer,
)

from apps.semesters.application.dto.create_semester_dto import (
    CreateSemesterDTO,
)

from apps.semesters.infrastructure.dependencies.semester_dependency import (
    create_semester_use_case,
)


class CreateSemesterView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            university_id = getattr(
                request.user,
                "university_id",
                None,
            )

            if not university_id:

                return Response(
                    {
                        "success": False,
                        "message": ("Không xác định được " "trường đại học."),
                    },
                    status=400,
                )

            serializer = CreateSemesterSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            dto = CreateSemesterDTO(
                academic_year_id=(serializer.validated_data["academic_year_id"]),
                semester_number=(serializer.validated_data["semester_number"]),
                start_date=(serializer.validated_data["start_date"]),
                end_date=(serializer.validated_data["end_date"]),
            )

            semester = create_semester_use_case.execute(
                data=dto,
                university_id=university_id,
            )

            response_serializer = SemesterSerializer(semester)

            return Response(
                {
                    "success": True,
                    "message": ("Tạo học kỳ thành công."),
                    "data": response_serializer.data,
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
                "CREATE SEMESTER ERROR:",
                str(error),
            )

            return Response(
                {
                    "success": False,
                    "message": ("Không thể tạo học kỳ."),
                },
                status=500,
            )
