from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.assignments.infrastructure.dependencies.assignment_application_dependency import (
    get_assignment_applications_use_case,
)

from apps.assignments.presentation.serializers.assignment_application_content_serializer import (
    AssignmentApplicationContentSerializer
)


class GetAssignmentApplicationsView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
        *args,
        **kwargs,
    ):

        class_section_id = request.query_params.get("class_section_id")

        lesson_id = request.query_params.get("lesson_id")

        teacher_email = getattr(
            request.user,
            "username",
            None,
        )

        if not teacher_email:
            return Response(
                {
                    "success": False,
                    "message": ("Không xác định được tài khoản giáo viên."),
                },
                status=403,
            )

        try:

            applications = get_assignment_applications_use_case.execute(
                class_section_id=class_section_id,
                lesson_id=lesson_id,
                teacher_email=teacher_email,
            )

            serializer = AssignmentApplicationContentSerializer(
                applications,
                many=True,
            )

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
