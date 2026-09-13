from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from apps.academic_years.infrastructure.dependencies.academic_year_dependency import (
    get_academic_years_use_case,
)

from apps.academic_years.presentation.serializers.academic_year_serializer import (
    AcademicYearSerializer,
)


class GetAcademicYearsView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    # =====================================================
    # GET
    # =====================================================

    def get(
        self,
        request,
    ):

        # =================================================
        # GET UNIVERSITY FROM AUTHENTICATED USER
        # =================================================

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
                        "Tài khoản chưa được gán trường đại học"
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # =================================================
        # GET ACADEMIC YEARS
        # =================================================

        try:

            academic_years = (
                get_academic_years_use_case.execute(
                    university_id=university_id,
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
                status=status.HTTP_200_OK,
            )

        except Exception as error:

            print(
                "GET ACADEMIC YEARS ERROR:",
                str(error),
            )

            return Response(
                {
                    "success": False,
                    "message": (
                        "Không thể lấy danh sách năm học"
                    ),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )