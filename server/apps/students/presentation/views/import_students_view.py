from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.students.infrastructure.dependencies.student_dependency import (
    excel_student_import_service,
    import_students_use_case,
)

from apps.students.presentation.serializers.import_student_serializer import (
    ImportStudentSerializer,
)


class ImportStudentsView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(
        self,
        request,
    ):

        try:

            # =========================================
            # University từ authenticated user
            # =========================================

            university_id = getattr(
                request.user,
                "university_id",
                None,
            )

            if not university_id:

                return Response(
                    {
                        "success": False,
                        "message": (
                            "Tài khoản chưa được "
                            "liên kết với trường."
                        ),
                    },
                    status=(
                        status.HTTP_400_BAD_REQUEST
                    ),
                )

            # =========================================
            # Validate file
            # =========================================

            serializer = (
                ImportStudentSerializer(
                    data=request.data
                )
            )

            serializer.is_valid(
                raise_exception=True
            )

            file = (
                serializer.validated_data[
                    "file"
                ]
            )

            # =========================================
            # Read Excel
            # =========================================

            rows = (
                excel_student_import_service
                .read(file)
            )

            # =========================================
            # Import
            # =========================================

            result = (
                import_students_use_case
                .execute(
                    rows=rows,
                    university_id=university_id,
                )
            )

            return Response(
                {
                    "success": True,
                    "message": (
                        "Import sinh viên "
                        "thành công."
                    ),
                    "data": result,
                },
                status=(
                    status.HTTP_201_CREATED
                ),
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=(
                    status.HTTP_400_BAD_REQUEST
                ),
            )

        except Exception as error:

            print(
                "IMPORT STUDENTS ERROR:",
                str(error),
            )

            return Response(
                {
                    "success": False,
                    "message": (
                        "Không thể import "
                        "sinh viên."
                    ),
                },
                status=(
                    status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
            )