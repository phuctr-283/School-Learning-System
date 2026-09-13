from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.class_sections.infrastructure.dependencies.get_teacher_class_sections_dependency import (
    get_teacher_class_sections_dependency,
)

from apps.class_sections.presentation.serializers.teacher_class_section_serializer import (
    TeacherClassSectionSerializer,
)


class GetTeacherClassSectionsView(APIView):

    def get(
        self,
        request,
        subject_id,
    ):

        university_id = getattr(
            request.user,
            "university_id",
            None,
        )

        department_id = getattr(
            request.user,
            "department_id",
            None,
        )

        teacher_id = getattr(
            request.user,
            "teacher_id",
            None,
        )

        if not university_id:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Không xác định được trường đại học."
                    ),
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not department_id:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Không xác định được khoa."
                    ),
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not teacher_id:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Không xác định được giảng viên."
                    ),
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not subject_id:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Thiếu mã môn học."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            class_sections = (
                get_teacher_class_sections_dependency
                .execute(
                    university_id=university_id,
                    department_id=department_id,
                    teacher_id=teacher_id,
                    subject_id=subject_id,
                )
            )

            serializer = (
                TeacherClassSectionSerializer(
                    class_sections,
                    many=True,
                )
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