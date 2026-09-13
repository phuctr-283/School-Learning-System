from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.assignments.infrastructure.dependencies.assignment_dependency import (
    assignment_repository,
)

from apps.assignments.presentation.serializers.assignment_content_serializer import (
    AssignmentContentSerializer,
)


class GetAssignmentByIdView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
        assignment_id,
        *args,
        **kwargs,
    ):

        university_id = getattr(
            request.user,
            "university_id",
            None,
        )

        if not university_id:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Tài khoản chưa được gán trường đại học."
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        assignment = assignment_repository.get_by_id(
            assignment_id=assignment_id,
            university_id=university_id,
        )

        if assignment is None:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Không tìm thấy bài tập."
                    ),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AssignmentContentSerializer(
            assignment,
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )