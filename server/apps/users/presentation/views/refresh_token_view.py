from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.application.dto.auth_dto import (
    RefreshTokenDTO,
)

from apps.users.presentation.serializers.refresh_token_serializer import (
    RefreshTokenSerializer,
)

from apps.users.infrastructure.dependencies.refresh_token_dependency import (
    refresh_token_use_case,
)


class RefreshTokenView(APIView):

    permission_classes = []

    def post(self, request):

        serializer = RefreshTokenSerializer(
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

            dto = RefreshTokenDTO(
                refresh_token=serializer.validated_data[
                    "refresh_token"
                ]
            )

            use_case = refresh_token_use_case()

            result = use_case.execute(dto)

            return Response(
                {
                    "success": True,
                    "message": "Refresh token thành công",
                    "data": {
                        "access_token": result["access_token"],
                        "refresh_token": result["refresh_token"],
                    },
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