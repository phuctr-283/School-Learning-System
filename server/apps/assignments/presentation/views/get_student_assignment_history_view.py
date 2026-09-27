from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.assignments.infrastructure.dependencies.student_assignment_dependencies import (
    get_student_assignment_history_use_case,
)

from apps.assignments.presentation.serializers.assignment_history_serializer import (
    AssignmentHistorySerializer,
)

from apps.assignments.application.exceptions.assignment_exceptions import (
    AssignmentBadRequestError,
    AssignmentForbiddenError,
    AssignmentLockedError,
    AssignmentNotFoundError,
)


class GetStudentAssignmentHistoryView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
        assignment_application_id,
        class_section_id,
        student_id,
    ):
        try:
            authenticated_student_id = (str(getattr(request.user,"username","",)).strip().upper())

            requested_student_id = str(student_id).strip().upper()

            if authenticated_student_id:                
                if authenticated_student_id != requested_student_id:
                    return Response(
                        {
                            "success": False,
                            "message": (
                                "Bạn không có quyền " "xem bài làm của sinh viên khác."
                            ),
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

            use_case = get_student_assignment_history_use_case()

            history = use_case.execute(
                assignment_application_id=(assignment_application_id),
                student_id=(requested_student_id),
                class_section_id=(class_section_id),
            )

            serializer = AssignmentHistorySerializer(history)

            return Response(
                {
                    "success": True,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except AssignmentBadRequestError as error:
            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except AssignmentForbiddenError as error:
            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        except AssignmentLockedError as error:
            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_423_LOCKED,
            )

        except AssignmentNotFoundError as error:
            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception:
            import traceback

            traceback.print_exc()

            return Response(
                {
                    "success": False,
                    "message": ("Không thể tải lịch sử bài làm."),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
