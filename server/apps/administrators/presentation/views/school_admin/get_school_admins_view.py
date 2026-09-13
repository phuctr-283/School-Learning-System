from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.administrators.application.use_cases.school_admin.get_school_admins import (
    GetSchoolAdminsUseCase,
)

from apps.administrators.infrastructure.persistence.repositories.mongo_school_admin_repository import (
    MongoSchoolAdminRepository,
)

from apps.administrators.presentation.serializers.school_admin.school_admin_serializer import (
    SchoolAdminSerializer,
)


repository = MongoSchoolAdminRepository()

get_school_admins_use_case = GetSchoolAdminsUseCase(
    repository
)


class GetSchoolAdminsView(APIView):

    def get(self, request):

        try:

            school_admins = get_school_admins_use_case.execute()

            serializer = SchoolAdminSerializer(
                school_admins,
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

            import traceback

            print(
                "GET SCHOOL ADMINS ERROR:",
                error,
            )

            traceback.print_exc()

            return Response(
                {
                    "success": False,
                    "message": "Không thể lấy danh sách Admin",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )