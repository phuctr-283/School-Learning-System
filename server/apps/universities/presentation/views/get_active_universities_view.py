from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.universities.infrastructure.persistence.repositories.mongo_university_repository import (
    MongoUniversityRepository,
)

from apps.universities.application.use_cases.get_active_universities import (
    GetActiveUniversitiesUseCase,
)

from apps.universities.presentation.serializers.university_serializer import (
    UniversitySerializer,
)


class GetActiveUniversityView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):

        try:

            repository = MongoUniversityRepository()

            use_case = GetActiveUniversitiesUseCase(repository)

            universities = use_case.execute()

            serializer = UniversitySerializer(
                universities,
                many=True,
            )

            return Response(
                {
                    "success": True,
                    "message": "Lấy danh sách trường thành công",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as error:

            print(
                "GET ACTIVE UNIVERSITIES ERROR:",
                error,
            )

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
