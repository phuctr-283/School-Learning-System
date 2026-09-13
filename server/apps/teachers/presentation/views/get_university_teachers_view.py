from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from apps.teachers.presentation.dependencies.teacher_dependencies import (
    get_teachers_use_case
)

from apps.teachers.presentation.serializers.teacher_serializer import (
    TeacherSerializer,
)


class GetUniversityTeachersView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

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

            if not university_id:

                return Response(
                    {
                        "success": False,
                        "message": "Tài khoản không thuộc trường đại học",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            use_case = get_teachers_use_case

            teachers = use_case.execute(
                university_id,
            )

            serializer = TeacherSerializer(
                teachers,
                many=True,
            )

            return Response(
                {
                    "success": True,
                    "message": "Lấy danh sách giảng viên thành công",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as error:

            print(
                "GET TEACHERS ERROR:",
                error,
            )

            return Response(
                {
                    "success": False,
                    "message": "Không thể lấy danh sách giảng viên",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
