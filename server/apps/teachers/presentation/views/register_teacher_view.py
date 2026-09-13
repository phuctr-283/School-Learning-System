from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.teachers.application.dto.register_teacher_dto import (
    RegisterTeacherDTO,
)

from apps.teachers.presentation.serializers.register_teacher_serializer import (
    RegisterTeacherSerializer,
)

from apps.teachers.presentation.dependencies.teacher_dependencies import (
    register_teacher_use_case
)


class RegisterTeacherView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = RegisterTeacherSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        dto = RegisterTeacherDTO(
            full_name=serializer.validated_data[
                "full_name"
            ],
            university_id=serializer.validated_data[
                "university_id"
            ],
            department_id=serializer.validated_data[
                "department_id"
            ],
            email=serializer.validated_data[
                "email"
            ],
            password=serializer.validated_data[
                "password"
            ],
        )

        try:

            teacher = (
                register_teacher_use_case.execute(
                    dto
                )
            )

            return Response(
                {
                    "success": True,
                    "message":
                        "Đăng ký giảng viên thành công",
                    "data": {
                        "teacher_id":
                            teacher.teacher_id,
                        "full_name":
                            teacher.full_name,
                        "email":
                            teacher.email,
                        "department_id":
                            teacher.department_id,
                        "department_name":
                            teacher.department_name,
                        "university_id":
                            teacher.university_id,
                        "university_name":
                            teacher.university_name,
                    },
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

        except Exception as error:

            print(
                "REGISTER TEACHER ERROR:",
                error,
            )

            return Response(
                {
                    "success": False,
                    "message":
                        "Có lỗi xảy ra khi đăng ký",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )