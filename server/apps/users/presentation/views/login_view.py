from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.application.dto.auth_dto import (
    LoginDTO,
)

from apps.users.presentation.serializers.login_serializer import (
    LoginSerializer,
)

from apps.users.infrastructure.dependencies.login_dependency import (
    login_use_case,
)


class LoginView(APIView):

    permission_classes = []

    def post(self, request):

        serializer = LoginSerializer(
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

            dto = LoginDTO(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )

            use_case = login_use_case()

            result = use_case.execute(dto)

            user = result["user"]
            tokens = result["tokens"]

            return Response(
                {
                    "success": True,
                    "message": "Đăng nhập thành công",
                    "data": {
                        "user": {
                            "user_id": user.user_id,
                            "username": user.username,
                            "account_level": user.account_level.value,
                            "university_id": user.university_id,
                            "is_active": user.is_active,
                            "last_login": user.last_login,
                        },
                        "access_token": tokens["access_token"],
                        "refresh_token": tokens["refresh_token"],
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