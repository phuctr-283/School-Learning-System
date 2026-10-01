from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.assignments.infrastructure.dependencies.assignment_application_dependency import (
    get_student_assignment_attempts_use_case
)

from apps.assignments.presentation.serializers.student_assignment_attempt_serializer import (
    StudentAssignmentAttemptsSerializer
)
from apps.assignments.application.exceptions.assignment_exceptions import (
    AssignmentForbiddenError,
    AssignmentNotFoundError,
    AssignmentLockedError,
    AssignmentBadRequestError,
    )
class GetStudentAssignmentAttemptsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        assignment_application_id = request.query_params.get(
            "assignment_application_id"
        )

        class_section_id = request.query_params.get(
            "class_section_id"
        )

        lesson_id = request.query_params.get(
            "lesson_id"
        )

        try:

            data = (
                get_student_assignment_attempts_use_case
                .execute(
                    assignment_application_id=(
                        assignment_application_id
                    ),
                    class_section_id=class_section_id,
                    lesson_id=lesson_id,
                )
            )

            serializer = (
                StudentAssignmentAttemptsSerializer(
                    data
                )
            )

            return Response(
                {
                    "success": True,
                    "message": (
                        "Lấy danh sách sinh viên "
                        "làm bài thành công."
                    ),
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except AssignmentForbiddenError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        except AssignmentNotFoundError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except (
            AssignmentBadRequestError,
            AssignmentLockedError,
        ) as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as error:

            print(
                "GET STUDENT ATTEMPTS ERROR:",
                error,
            )

            return Response(
                {
                    "success": False,
                    "message": (
                        "Không thể lấy danh sách "
                        "sinh viên làm bài."
                    ),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )