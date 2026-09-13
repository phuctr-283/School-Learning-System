from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from apps.academic_years.infrastructure.dependencies.academic_year_dependency import (
    create_academic_year_use_case,
)

from apps.academic_years.presentation.serializers.create_academic_year_serializer import (
    CreateAcademicYearSerializer,
)

from apps.academic_years.application.dto.create_academic_year_dto import (
    CreateAcademicYearDTO,
)


class CreateAcademicYearView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    # =====================================================
    # POST
    # =====================================================

    def post(
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
        # SERIALIZER
        # =================================================

        serializer = CreateAcademicYearSerializer(
            data=request.data,
        )

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": "Dữ liệu không hợp lệ",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # =================================================
        # DTO
        # =================================================

        dto = CreateAcademicYearDTO(
            name=serializer.validated_data["name"],
            start_date=serializer.validated_data["start_date"],
            end_date=serializer.validated_data["end_date"],
        )

        # =================================================
        # USE CASE
        # =================================================

        try:

            academic_year = (
                create_academic_year_use_case.execute(
                    data=dto,
                    university_id=university_id,
                )
            )

            return Response(
                {
                    "success": True,
                    "message": "Tạo năm học thành công",
                    "data": {
                        "academic_year_id": (
                            academic_year.academic_year_id
                        ),
                        "name": academic_year.name,
                        "start_date": (
                            academic_year.start_date
                        ),
                        "end_date": (
                            academic_year.end_date
                        ),
                        "status": (
                            academic_year.status
                        ),
                    },
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
                "CREATE ACADEMIC YEAR ERROR:",
                str(error),
            )

            return Response(
                {
                    "success": False,
                    "message": "Không thể tạo năm học",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )