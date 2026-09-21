from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.assignments.infrastructure.dependencies.assignment_dependency import (
    get_assignments_by_subject_use_case,
)

from apps.assignments.presentation.serializers.assignment_list_serializer import (
    AssignmentListSerializer,
)


class GetAssignmentsBySubjectView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
        subject_id,
        *args,
        **kwargs,
    ):

        university_id = getattr(
            request.user,
            "university_id",
            None,
        )

        teacher_email = getattr(
            request.user,
            "username",
            None,
        )

        if not university_id or not teacher_email:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Tài khoản chưa có trường đại học " "hoặc email đăng nhập."
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            assignments = get_assignments_by_subject_use_case.execute(
                university_id=university_id,
                teacher_email=teacher_email,
                subject_id=subject_id,
            )

            serializer = AssignmentListSerializer(
                assignments,
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
