from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.universities.application.dto.create_university_dto import (
    CreateUniversityDTO,
)

from apps.universities.presentation.serializers.university_serializer import (
    UniversitySerializer,
)
from apps.universities.presentation.serializers.create_university_serializer import CreateUniversitySerializer
from apps.universities.presentation.dependencies import (
    create_university_use_case,
)


class CreateUniversityView(APIView):

    def post(self, request):

        serializer = CreateUniversitySerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            dto = CreateUniversityDTO(
                **serializer.validated_data
            )

            university = create_university_use_case.execute(
                dto
            )

            response_serializer = UniversitySerializer(
                university.__dict__
            )

            return Response(
                {
                    "success": True,
                    "message": "Tạo trường thành công",
                    "data": response_serializer.data,
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