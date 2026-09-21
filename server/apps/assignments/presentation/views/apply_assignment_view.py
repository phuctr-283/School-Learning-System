from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.assignments.infrastructure.dependencies.assignment_application_dependency import (
    apply_assignment_use_case,
)

from apps.assignments.presentation.serializers.apply_assignment_serializer import (
    ApplyAssignmentSerializer,
)

from apps.assignments.presentation.serializers.assignment_application_serializer import (
    AssignmentApplicationSerializer,
)

from apps.assignments.application.dto.apply_assignment_dto import (
    ApplyAssignmentDTO,
)


class ApplyAssignmentView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(
        self,
        request,
        *args,
        **kwargs,
    ):

        username = getattr(
            request.user,
            "username",
            None,
        )

        if not username:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Không xác định được tài khoản giáo viên."
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ApplyAssignmentSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        data = serializer.validated_data

        dto = ApplyAssignmentDTO(
            assignment_id=data["assignment_id"],
            lesson_id=data["lesson_id"],
            class_section_ids=data["class_section_ids"],
            max_attempts=data["max_attempts"],
            teacher_email=username,
        )

        try:

            application = (
                apply_assignment_use_case.execute(
                    dto=dto,
                )
            )

            response_serializer = (
                AssignmentApplicationSerializer(
                    application,
                )
            )

            return Response(
                {
                    "success": True,
                    "message": (
                        "Áp dụng bài tập cho "
                        "buổi học thành công."
                    ),
                    "data": response_serializer.data,
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