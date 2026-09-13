from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.academic_years.presentation.serializers.academic_year_serializer import (
    AcademicYearSerializer,
)

from apps.academic_years.infrastructure.dependencies.academic_year_dependency import (
    get_active_and_planned_academic_years_use_case,
)


class GetActiveAndPlannedAcademicYearsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

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
                        "message": "Không xác định được trường đại học.",
                    },
                    status=400,
                )

            academic_years = (
                get_active_and_planned_academic_years_use_case
                .execute(
                    university_id=university_id
                )
            )

            serializer = AcademicYearSerializer(
                academic_years,
                many=True,
            )

            return Response(
                {
                    "success": True,
                    "data": serializer.data,
                },
                status=200,
            )

        except Exception as error:

            print(
                "GET ACTIVE AND PLANNED ACADEMIC YEARS ERROR:",
                str(error),
            )

            return Response(
                {
                    "success": False,
                    "message": "Không thể lấy danh sách năm học.",
                },
                status=500,
            )