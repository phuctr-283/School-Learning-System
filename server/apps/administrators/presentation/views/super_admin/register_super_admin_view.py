from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.administrators.application.dto.super_admin.register_super_admin_dto import (
    RegisterSuperAdminDTO,
)

from apps.administrators.presentation.serializers.super_admin.register_super_admin_serializer import (
    RegisterSuperAdminSerializer,
)
from apps.administrators.presentation.dependencies import (
    register_super_admin_use_case
)

class RegisterSuperAdminView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):

        serializer = RegisterSuperAdminSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:

            dto = RegisterSuperAdminDTO(**serializer.validated_data)

            admin = register_super_admin_use_case.execute(dto)

            return Response(
                {
                    "success": True,
                    "message": ("Đăng ký Super Admin thành công"),
                    "data": {
                        "super_admin_id": admin.super_admin_id,
                        "full_name": admin.full_name,
                        "email": admin.email,
                        "status": admin.status,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        except ValueError as error:
            print("Error:", error),
            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                
                status=status.HTTP_400_BAD_REQUEST,
            )
