from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.departments.infrastructure.dependencies.department_dependency import (
    get_active_departments_use_case,
)

from apps.departments.presentation.serializers.department_serializer import (
    DepartmentSerializer,
)


class GetActiveDepartmentsView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

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
                        "message": (
                            "Tài khoản chưa được "
                            "liên kết với trường."
                        ),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            departments = (
                get_active_departments_use_case
                .execute(
                    university_id=university_id,
                )
            )

            serializer = DepartmentSerializer(
                departments,
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
                "GET ACTIVE DEPARTMENTS ERROR:",
                str(error),
            )

            return Response(
                {
                    "success": False,
                    "message": (
                        "Không thể lấy danh sách khoa."
                    ),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )