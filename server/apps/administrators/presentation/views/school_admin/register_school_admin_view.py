from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.administrators.application.dto.school_admin.register_school_admin_dto import (
    RegisterSchoolAdminDTO,
)

from apps.administrators.presentation.serializers.school_admin.register_school_admin_serializer import (
    RegisterSchoolAdminSerializer,
)
from apps.administrators.presentation.dependencies import (
    register_school_admin_use_case,
)


class RegisterSchoolAdminView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):

        serializer = RegisterSchoolAdminSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:

            dto = RegisterSchoolAdminDTO(**serializer.validated_data)

            admin = register_school_admin_use_case.execute(dto)

            return Response(
                {
                    "success": True,
                    "message": ("Đăng ký School Admin thành công"),
                    "data": {
                        "school_admin_id": admin.school_admin_id,
                        "full_name": admin.full_name,
                        "email": admin.email,
                        "university_id": admin.university_id,
                        "university_name": admin.university_name,
                        "status": admin.status,
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
