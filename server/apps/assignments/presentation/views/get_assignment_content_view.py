from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.assignments.infrastructure.dependencies.assignment_dependency import (
    get_assignment_content_use_case,
)

from apps.assignments.presentation.serializers.assignment_content_serializer import (
    AssignmentContentSerializer,
)


class GetAssignmentContentView(APIView):

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

        teacher_email = getattr(
            request.user,
            "username",
            None,
        )

        if not university_id:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Tài khoản chưa có trường đại học."
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if not teacher_email:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Tài khoản chưa có email đăng nhập."
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:

            assignment = (
                get_assignment_content_use_case.execute(
                    assignment_id=assignment_id,
                    university_id=university_id,
                    teacher_email=teacher_email,
                )
            )

            serializer = (
                AssignmentContentSerializer(
                    assignment,
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
                status=status.HTTP_404_NOT_FOUND,
            )