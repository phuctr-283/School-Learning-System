from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.assignments.presentation.serializers.student_assignment_serializer import (
    StudentAssignmentSerializer,
    StudentAssignmentResultSerializer,
)

class GetStudentAssignmentView(APIView):

    authentication_classes = []
    permission_classes = []

    get_use_case = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request):

        try:

            student_id = request.query_params.get("student_id")
            assignment_application_id = request.query_params.get(
                "assignment_application_id"
            )
            class_section_id = request.query_params.get(
                "class_section_id"
            )
            lesson_id = request.query_params.get("lesson_id")

            if not student_id:
                raise ValueError("Thiếu student_id.")

            if not assignment_application_id:
                raise ValueError(
                    "Thiếu assignment_application_id."
                )

            if not class_section_id:
                raise ValueError(
                    "Thiếu class_section_id."
                )

            if not lesson_id:
                raise ValueError(
                    "Thiếu lesson_id."
                )

            if self.get_use_case is None:
                raise RuntimeError(
                    "GetStudentAssignmentUseCase chưa được cấu hình."
                )

            data = self.get_use_case.execute(
                student_id=student_id,
                assignment_application_id=assignment_application_id,
                class_section_id=class_section_id,
                lesson_id=lesson_id,
            )
            serializer = StudentAssignmentSerializer(
                data
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
                status=status.HTTP_400_BAD_REQUEST,
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
                raise RuntimeError(
                    "SaveStudentAssignmentUseCase chưa được cấu hình."
                )

            result = self.save_use_case.execute(
                student_id=data.get("student_id"),
                assignment_application_id=data.get(
                    "assignment_application_id"
                ),
                class_section_id=data.get(
                    "class_section_id"
                ),
                lesson_id=data.get(
                    "lesson_id"
                ),
                attempt_id=data.get(
                    "attempt_id"
                ),
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

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception:

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
                raise RuntimeError(
                    "SubmitStudentAssignmentUseCase chưa được cấu hình."
                )

            result = self.submit_use_case.execute(
                student_id=data.get("student_id"),
                assignment_application_id=data.get(
                    "assignment_application_id"
                ),
                class_section_id=data.get(
                    "class_section_id"
                ),
                lesson_id=data.get(
                    "lesson_id"
                ),
                attempt_id=data.get(
                    "attempt_id"
                ),
                answers=data.get(
                    "answers",
                    {},
                ),
            )

            serializer = StudentAssignmentResultSerializer(
                result
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
                status=status.HTTP_400_BAD_REQUEST,
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