from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.students.infrastructure.dependencies.student_dependency import (
    get_students_use_case,
)

from apps.students.presentation.serializers.student_serializer import (
    StudentSerializer,
)


class GetStudentsView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
    ):

        try:

            university_id = getattr(request.user,"university_id",None,)

            if not university_id:

                return Response(
                    {
                        "success": False,
                        "message": ("Tài khoản chưa được " "liên kết với trường."),
                    },
                    status=(status.HTTP_400_BAD_REQUEST),
                )

            students = get_students_use_case.execute(
                university_id=university_id,
            )

            serializer = StudentSerializer(
                students,
                many=True,
            )

            return Response(
                {
                    "success": True,
                    "message": ("Lấy danh sách sinh viên " "thành công."),
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as error:

            print(
                "GET STUDENTS ERROR:",
                str(error),
            )

            return Response(
                {
                    "success": False,
                    "message": ("Không thể lấy danh sách " "sinh viên."),
                },
                status=(status.HTTP_500_INTERNAL_SERVER_ERROR),
            )
