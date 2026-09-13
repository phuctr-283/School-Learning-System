from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.assignments.infrastructure.dependencies.assignment_dependency import (
    get_assignments_use_case,
)

from apps.assignments.presentation.serializers.assignment_list_serializer import (
    AssignmentListSerializer,
)


class GetAssignmentsView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
        *args,
        **kwargs,
    ):

        university_id = getattr(
            request.user,
            "university_id",
            None,
        )

        teacher_id = getattr(
            request.user,
            "teacher_id",
            None,
        )

        department_id = getattr(
            request.user,
            "department_id",
            None,
        )

        if not university_id or not teacher_id:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Tài khoản chưa được gán giảng viên."
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        assignments = (
            get_assignments_use_case.execute(
                university_id=university_id,
                teacher_id=teacher_id,
                department_id=department_id,
            )
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