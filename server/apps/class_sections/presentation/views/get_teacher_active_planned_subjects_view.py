from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.class_sections.infrastructure.dependencies.get_teacher_subjects_dependency import (
    get_teacher_active_planned_subjects_use_case,
)

from apps.class_sections.presentation.serializers.teacher_subject_serializer import (
    TeacherSubjectSerializer,
)


class GetTeacherActivePlannedSubjectsView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, academic_year_id, semester_id):

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
                    "message": ("Tài khoản chưa được gán " "trường đại học."),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not username:
            return Response(
                {
                    "success": False,
                    "message": ("Không xác định được " "tài khoản giảng viên."),
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not academic_year_id:
            return Response(
                {
                    "success": False,
                    "message": "Thiếu mã năm học.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not semester_id:
            return Response(
                {
                    "success": False,
                    "message": "Thiếu mã học kỳ.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            subjects = get_teacher_active_planned_subjects_use_case.execute(
                university_id=university_id,
                username=username,
                academic_year_id=academic_year_id,
                semester_id=semester_id,
            )

            serializer = TeacherSubjectSerializer(
                subjects,
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
