from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.application.dto.user_dto import (
    CreateUserDTO,
)

from apps.users.domain.enums.account_level import (
    AccountLevel,
)

from apps.users.presentation.serializers.create_user_serializer import (
    CreateUserSerializer,
)

from apps.users.infrastructure.dependencies.create_user_dependency import (
    create_user_use_case,
)


class CreateUserView(APIView):

    permission_classes = []

    def post(self, request):

        serializer = CreateUserSerializer(
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

            account_level = AccountLevel(
                serializer.validated_data["account_level"]
            )

            dto = CreateUserDTO(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
                account_level=account_level,
                university_id=serializer.validated_data.get(
                    "university_id"
                ),
            )

            use_case = create_user_use_case()

            user = use_case.execute(dto)

            return Response(
                {
                    "success": True,
                    "message": "Tạo tài khoản thành công",
                    "data": {
                        "user_id": user.user_id,
                        "username": user.username,
                        "account_level": user.account_level.value,
                        "university_id": user.university_id,
                        "is_active": user.is_active,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:

            return Response(
                {
                    "success": False,
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )