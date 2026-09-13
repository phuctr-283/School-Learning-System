from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.departments.infrastructure.persistence.repositories.mongo_department_repository import (
    MongoDepartmentRepository,
)

from apps.universities.infrastructure.persistence.repositories.mongo_university_repository import (
    MongoUniversityRepository,
)

from apps.departments.application.use_cases.get_active_departments_by_university import (
    GetActiveDepartmentsByUniversityUseCase,
)

from apps.departments.presentation.serializers.get_active_departments_by_university_serializer import (
    GetActiveDepartmentsByUniversitySerializer,
)


class GetActiveDepartmentsByUniversityView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):

        university_id = request.query_params.get("university_id")

        try:

            department_repository = MongoDepartmentRepository()

            university_repository = MongoUniversityRepository()

            use_case = GetActiveDepartmentsByUniversityUseCase(
                department_repository,
                university_repository,
            )

            departments = use_case.execute(university_id)

            serializer = GetActiveDepartmentsByUniversitySerializer(
                departments,
                many=True,
            )

            return Response(
                {
                    "success": True,
                    "message": "Lấy danh sách khoa thành công",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
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
                "GET ACTIVE DEPARTMENTS ERROR:",
                error,
            )

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
