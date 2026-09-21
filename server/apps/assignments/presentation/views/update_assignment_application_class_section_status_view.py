from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.assignments.infrastructure.dependencies.assignment_application_dependency import (
    update_assignment_application_class_section_status_use_case,
)

from apps.assignments.presentation.serializers.assignment_application_content_serializer import (
    AssignmentApplicationContentSerializer,
)


class UpdateAssignmentApplicationClassSectionStatusView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(
        self,
        request,
        assignment_application_id,
        class_section_id,
    ):

        teacher_email = getattr(
            request.user,
            "email",
            None,
        ) or getattr(
            request.user,
            "username",
            None,
        )

        if not teacher_email:

            return Response(
                {
                    "success": False,
                    "message": ("Không xác định được " "tài khoản giáo viên."),
                },
                status=403,
            )

        status = request.data.get("status")

        if status not in (
            "active",
            "closed",
        ):

            return Response(
                {
                    "success": False,
                    "message": ("status phải là " "active hoặc closed."),
                },
                status=400,
            )

        try:

            application = (
                update_assignment_application_class_section_status_use_case.execute(
                    assignment_application_id=(assignment_application_id),
                    class_section_id=(class_section_id),
                    teacher_email=teacher_email,
                    status=status,
                )
            )

            serializer = AssignmentApplicationContentSerializer(application)

            return Response(
                {
                    "success": True,
                    "data": serializer.data,
                },
                status=200,
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=400,
            )
