from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.assignments.presentation.serializers.assignment_application_content_serializer import (
    AssignmentApplicationSerializer,
)

from apps.assignments.infrastructure.dependencies.assignment_application_dependency import (
    get_student_assignment_application_use_case,
)


class GetStudentAssignmentApplicationView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
        class_section_id,
        lesson_id,
    ):

        user = request.user

        university_id = getattr(
            user,
            "university_id",
            None,
        )

        student_id = getattr(
            user,
            "username",
            None,
        )

        if not university_id:
            return Response(
                {"message": "Không xác định được trường đại học."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not student_id:
            return Response(
                {"message": "Không xác định được sinh viên."},
                status=status.HTTP_403_FORBIDDEN,
            )

        result = get_student_assignment_application_use_case.execute(
            university_id=university_id,
            student_id=student_id,
            class_section_id=class_section_id,
            lesson_id=lesson_id,
        )

        response_serializer = AssignmentApplicationSerializer(
            result,
            many=True,
        )

        return Response(
            {
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
