from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.departments.application.dto.create_department_dto import (
    CreateDepartmentDTO,
)

from apps.departments.presentation.serializers.create_department_serializer import (
    CreateDepartmentSerializer,
)

from apps.departments.infrastructure.dependencies.department_dependency import (
    create_department_use_case,
)


class CreateDepartmentView(APIView):

    def post(self, request):

        # =========================================
        # VALIDATE REQUEST
        # =========================================

        serializer = CreateDepartmentSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        # =========================================
        # GET UNIVERSITY FROM AUTHENTICATED USER
        # =========================================

        university_id = getattr(
            request.user,
            "university_id",
            None,
        )

        if not university_id:

            return Response(
                {
                    "success": False,
                    "message": "Tài khoản không thuộc trường đại học",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # =========================================
        # CREATE DTO
        # =========================================

        dto = CreateDepartmentDTO(**serializer.validated_data)

        # =========================================
        # EXECUTE USE CASE
        # =========================================

        try:

            department = create_department_use_case.execute(
                data=dto,
                university_id=university_id,
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
                "CREATE DEPARTMENT ERROR:",
                error,
            )

            return Response(
                {
                    "success": False,
                    "message": "Có lỗi xảy ra khi tạo khoa",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # =========================================
        # RESPONSE
        # =========================================

        response_serializer = CreateDepartmentSerializer(
            department,
        )

        return Response(
            {
                "success": True,
                "message": "Tạo khoa thành công",
                "data": response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
