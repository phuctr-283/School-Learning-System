from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.class_sections.infrastructure.dependencies.get_teacher_class_sections_dependency import (
    get_teacher_class_sections_use_case,
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

        username = getattr(
            request.user,
            "username",
            None,
        )

        if not university_id:
            return Response(
                {
                    "success": False,
                    "message": "Không xác định được trường đại học.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not username:
            return Response(
                {
                    "success": False,
                    "message": "Không xác định được tài khoản giảng viên.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not subject_id:
            return Response(
                {
                    "success": False,
                    "message": "Thiếu mã môn học.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            
            class_sections = (
                get_teacher_class_sections_use_case.execute(
                    university_id=university_id,
                    username=username,
                    subject_id=subject_id,
                )
            )

            serializer = TeacherClassSectionSerializer(
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