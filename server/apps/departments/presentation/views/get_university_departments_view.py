from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from apps.departments.infrastructure.dependencies.department_dependency import (
    get_university_departments_use_case,
)


class GetUniversityDepartmentsView(APIView):

    def get(
        self,
        request,
    ):

        try:

            university_id = getattr(
                request.user,
                "university_id",
                None,
            )

            departments = get_university_departments_use_case.execute(university_id)

            return Response(
                {
                    "success": True,
                    "data": [
                        {
                            "department_id": (department.department_id),
                            "department_number": (department.department_number),
                            "name": (department.name),
                            "university_id": (department.university_id),
                            "university_name": (department.university_name),
                            "head_id": (department.head_id),
                            "head_name": (department.head_name),
                            "is_active": (department.is_active),
                        }
                        for department in departments
                    ],
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
