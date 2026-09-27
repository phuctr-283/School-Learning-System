from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.assignments.presentation.serializers.student_assignment_serializer import (
    StudentAssignmentSerializer,
    StudentAssignmentResultSerializer,
)
from apps.assignments.application.exceptions.assignment_exceptions import (
    AssignmentNotFoundError,
    AssignmentLockedError,
    AssignmentForbiddenError,
    AssignmentBadRequestError,
    AssignmentApiError,
)


class GetStudentAssignmentView(APIView):

    authentication_classes = []
    permission_classes = []

    get_use_case = None

    def get(self, request):

        try:

            student_id = str(
                request.query_params.get(
                    "student_id",
                    "",
                )
            ).strip()
            assignment_application_id = str(
                request.query_params.get(
                    "assignment_application_id",
                )
            ).strip()
            class_section_id = str(
                request.query_params.get(
                    "class_section_id",
                    "",
                )
            ).strip()

            lesson_id = str(
                request.query_params.get(
                    "lesson_id",
                    "",
                )
            ).strip()

            if not student_id:
                raise AssignmentBadRequestError(
                    "Thiếu student_id."
                )

            if not assignment_application_id:
                raise AssignmentBadRequestError(
                    "Thiếu assignment_application_id."
                )

            if not class_section_id:
                raise AssignmentBadRequestError(
                    "Thiếu class_section_id."
                )

            if not lesson_id:
                raise AssignmentBadRequestError(
                    "Thiếu lesson_id."
                )

            if self.get_use_case is None:
                raise RuntimeError("GetStudentAssignmentUseCase chưa được cấu hình.")

            data = self.get_use_case.execute(
                student_id=student_id,
                assignment_application_id=assignment_application_id,
                class_section_id=class_section_id,
                lesson_id=lesson_id,
            )
            serializer = StudentAssignmentSerializer(data)

            return Response(
                {
                    "success": True,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except AssignmentApiError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=error.status_code,
            )

        except Exception as error:

            import traceback

            traceback.print_exc()

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SaveStudentAssignmentView(APIView):

    authentication_classes = []
    permission_classes = []

    save_use_case = None

    def post(self, request):

        try:

            data = request.data

            if self.save_use_case is None:
                raise RuntimeError("SaveStudentAssignmentUseCase chưa được cấu hình.")

            student_id = data.get("student_id")
            assignment_application_id = data.get(
                "assignment_application_id"
            )
            class_section_id = data.get(
                "class_section_id"
            )
            lesson_id = data.get("lesson_id")
            attempt_id = data.get("attempt_id")

            if not student_id:
                raise AssignmentBadRequestError(
                    "Thiếu student_id."
                )

            if not assignment_application_id:
                raise AssignmentBadRequestError(
                    "Thiếu assignment_application_id."
                )

            if not class_section_id:
                raise AssignmentBadRequestError(
                    "Thiếu class_section_id."
                )

            if not lesson_id:
                raise AssignmentBadRequestError(
                    "Thiếu lesson_id."
                )

            if not attempt_id:
                raise AssignmentBadRequestError(
                    "Thiếu attempt_id."
                )
            
            result = self.save_use_case.execute(
                student_id=data.get("student_id"),
                assignment_application_id=data.get("assignment_application_id"),
                class_section_id=data.get("class_section_id"),
                lesson_id=data.get("lesson_id"),
                attempt_id=data.get("attempt_id"),
                answers=data.get(
                    "answers",
                    {},
                ),
            )

            return Response(
                {
                    "success": True,
                    "data": result,
                },
                status=status.HTTP_200_OK,
            )

        except AssignmentApiError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=error.status_code,
            )

        except Exception:

            import traceback

            traceback.print_exc()

            return Response(
                {
                    "success": False,
                    "message": "Không thể lưu bài làm.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SubmitStudentAssignmentView(APIView):

    authentication_classes = []
    permission_classes = []

    submit_use_case = None

    def post(self, request):

        try:

            data = request.data

            if self.submit_use_case is None:
                raise RuntimeError("SubmitStudentAssignmentUseCase chưa được cấu hình.")

            student_id = data.get("student_id")
            assignment_application_id = data.get(
                "assignment_application_id"
            )
            class_section_id = data.get(
                "class_section_id"
            )
            lesson_id = data.get("lesson_id")
            attempt_id = data.get("attempt_id")

            if not student_id:
                raise AssignmentBadRequestError(
                    "Thiếu student_id."
                )

            if not assignment_application_id:
                raise AssignmentBadRequestError(
                    "Thiếu assignment_application_id."
                )

            if not class_section_id:
                raise AssignmentBadRequestError(
                    "Thiếu class_section_id."
                )

            if not lesson_id:
                raise AssignmentBadRequestError(
                    "Thiếu lesson_id."
                )

            if not attempt_id:
                raise AssignmentBadRequestError(
                    "Thiếu attempt_id."
                )

            result = self.submit_use_case.execute(
                student_id=data.get("student_id"),
                assignment_application_id=data.get("assignment_application_id"),
                class_section_id=data.get("class_section_id"),
                lesson_id=data.get("lesson_id"),
                attempt_id=data.get("attempt_id"),
                answers=data.get(
                    "answers",
                    {},
                ),
            )

            serializer = StudentAssignmentResultSerializer(result)

            return Response(
                {
                    "success": True,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except AssignmentApiError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=error.status_code,
            )

        except Exception:

            import traceback

            traceback.print_exc()

            return Response(
                {
                    "success": False,
                    "message": "Không thể nộp bài.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
