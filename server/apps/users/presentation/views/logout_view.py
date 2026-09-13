from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.application.dto.auth_dto import (
    LogoutDTO,
)

from apps.users.presentation.serializers.logout_serializer import (
    LogoutSerializer,
)

from apps.users.infrastructure.dependencies.logout_dependency import (
    logout_use_case,
)


class LogoutView(APIView):

    permission_classes = []

    def post(self, request):

        serializer = LogoutSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            dto = LogoutDTO(
                refresh_token=serializer.validated_data[
                    "refresh_token"
                ]
            )

            use_case = logout_use_case()

            use_case.execute(dto)

            return Response(
                {
                    "success": True,
                    "message": "Đăng xuất thành công",
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as e:

            return Response(
                {
                    "success": False,
                    "message": str(e),
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )