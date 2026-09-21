from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.assignments.presentation.serializers.verify_student_assignment_qr_serializer import (
    VerifyStudentAssignmentQrSerializer,
)

from apps.assignments.infrastructure.dependencies.verify_student_assignment_qr_dependency import (
    verify_student_assignment_qr_use_case,
)


class VerifyStudentAssignmentQrView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = VerifyStudentAssignmentQrSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": "Dữ liệu không hợp lệ.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            result = verify_student_assignment_qr_use_case.execute(
                **serializer.validated_data
            )

            return Response(
                {
                    "success": True,
                    "data": result,
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
                "VERIFY STUDENT ASSIGNMENT QR ERROR:",
                error,
            )

            return Response(
                {
                    "success": False,
                    "message": ("Không thể xác thực " "quyền truy cập bài tập."),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
