from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.class_sections.infrastructure.dependencies.get_teacher_subjects_dependency import (
    get_teacher_subjects_use_case,
)

from apps.class_sections.presentation.serializers.teacher_subject_serializer import (
    TeacherSubjectSerializer,
)


class GetTeacherSubjectsView(APIView):

    def get(self, request):

        user = request.user

        university_id = getattr(
            user,
            "university_id",
            None,
        )

        username = getattr(
            user,
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

        try:

            subjects = get_teacher_subjects_use_case.execute(
                university_id=university_id,
                username=username,
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
