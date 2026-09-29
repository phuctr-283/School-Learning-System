from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.assignments.presentation.serializers.assignment_detail_serializer import (
    AssignmentDetailSerializer,
)
from apps.assignments.infrastructure.dependencies.assignment_dependency import get_assignment_by_id_use_case

class GetAssignmentByIdView(APIView):

    permission_classes = [
        IsAuthenticated
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

        try:

            assignment = (
                get_assignment_by_id_use_case
                .execute(
                    assignment_id=assignment_id,
                    university_id=university_id,
                    teacher_email=teacher_email,
                )
            )

            serializer = (
                AssignmentDetailSerializer(
                    assignment
                )
            )

            return Response(
                {
                    "success": True,
                    "message": (
                        "Lấy thông tin bài tập "
                        "thành công."
                    ),
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except PermissionError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_403_FORBIDDEN,
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

            return Response(
                {
                    "success": False,
                    "message": (
                        "Không thể tải "
                        "bài tập."
                    ),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )