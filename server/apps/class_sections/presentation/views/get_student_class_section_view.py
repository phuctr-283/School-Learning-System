from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.class_sections.infrastructure.dependencies.get_student_class_section_dependency import (
    get_student_class_sections_dependency,
)

from apps.class_sections.presentation.serializers.student_class_section_serializer import (
    StudentClassSectionSerializer,
)


class GetStudentClassSectionsView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        try:
            user = request.user

            student_id = getattr(
                user,
                "username",
                None,
            )

            university_id = getattr(
                user,
                "university_id",
                None,
            )

            if not student_id:
                return Response(
                    {
                        "success": False,
                        "message": ("Không xác định được mã sinh viên"),
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if not university_id:
                return Response(
                    {
                        "success": False,
                        "message": ("Không xác định được trường đại học"),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            class_sections = get_student_class_sections_dependency.execute(
                student_id=student_id,
                university_id=university_id,
            )

            serializer = StudentClassSectionSerializer(
                class_sections,
                many=True,
            )

            return Response(
                {
                    "success": True,
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
                "GET STUDENT CLASS SECTIONS ERROR:",
                error,
            )

            return Response(
                {
                    "success": False,
                    "message": ("Không thể tải danh sách lớp học phần"),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
