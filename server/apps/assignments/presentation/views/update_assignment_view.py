import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.assignments.application.dto.update_assignment_dto import (
    UpdateAssignmentDTO,
)

from apps.assignments.infrastructure.dependencies.assignment_dependency import (
    update_assignment_use_case,
)

from apps.assignments.presentation.serializers.update_assignment_serializer import (
    UpdateAssignmentSerializer,
)


class UpdateAssignmentView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def put(
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

        username = getattr(
            request.user,
            "username",
            None,
        )

        if not university_id or not username:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Tài khoản chưa có " "trường đại học hoặc " "email đăng nhập."
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        payload = request.data.copy()

        if isinstance(
            payload.get("questions"),
            str,
        ):
            try:
                payload["questions"] = json.loads(
                    payload["questions"],
                )
            except json.JSONDecodeError:
                return Response(
                    {
                        "success": False,
                        "message": ("Dữ liệu câu hỏi " "không hợp lệ."),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = UpdateAssignmentSerializer(
            data=payload,
        )

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data

        dto = UpdateAssignmentDTO(
            title=data["title"],
            description=data.get(
                "description",
            ),
            subject_id=data["subject_id"],
            assignment_type=data["assignment_type"],
            duration_minutes=data["duration_minutes"],
            questions=data["questions"],
        )

        try:

            assignment = update_assignment_use_case.execute(
                assignment_id=assignment_id,
                dto=dto,
                university_id=university_id,
                teacher_email=username,
            )

            return Response(
                {
                    "success": True,
                    "message": ("Cập nhật bài tập " "thành công."),
                    "data": {
                        "assignment_id": (assignment.assignment_id),
                        "title": assignment.title,
                        "subject_id": (assignment.subject_id),
                        "assignment_type": (assignment.assignment_type),
                        "total_score": str(
                            assignment.total_score,
                        ),
                        "duration_minutes": (assignment.duration_minutes),
                    },
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

        except Exception as error:

            print(
                "UPDATE ASSIGNMENT ERROR:",
                error,
            )

            return Response(
                {
                    "success": False,
                    "message": ("Không thể cập nhật " "bài tập."),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
