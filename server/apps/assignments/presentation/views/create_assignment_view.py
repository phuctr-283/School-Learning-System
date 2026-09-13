from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.assignments.presentation.serializers.create_assignment_serializer import (
    CreateAssignmentSerializer,
)

from apps.assignments.application.dto.create_assignment_dto import (
    CreateAssignmentDTO,
)

from apps.assignments.infrastructure.dependencies.assignment_dependency import (
    create_assignment_use_case,
)


class CreateAssignmentView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(
        self,
        request,
        *args,
        **kwargs,
    ):

        serializer = CreateAssignmentSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = request.user

        university_id = getattr(
            user,
            "university_id",
            None,
        )

        department_id = getattr(
            user,
            "department_id",
            None,
        )

        teacher_id = getattr(
            user,
            "teacher_id",
            None,
        )

        if not university_id:
            return Response(
                {
                    "success": False,
                    "message": ("Tài khoản chưa được gán trường đại học."),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if not department_id:
            return Response(
                {
                    "success": False,
                    "message": ("Tài khoản chưa được gán khoa."),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if not teacher_id:
            return Response(
                {
                    "success": False,
                    "message": ("Tài khoản chưa được gán giảng viên."),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:

            dto = CreateAssignmentDTO(
                university_id=university_id,
                department_id=department_id,
                teacher_id=teacher_id,
                subject_id=serializer.validated_data["subject_id"],
                title=serializer.validated_data["title"],
                description=serializer.validated_data.get(
                    "description",
                ),
                assignment_type=serializer.validated_data.get(
                    "assignment_type",
                    "practice",
                ),
                questions=serializer.validated_data["questions"],
            )

            assignment = create_assignment_use_case.execute(
                dto,
            )

            return Response(
                {
                    "success": True,
                    "message": "Tạo bài tập thành công.",
                    "data": {
                        "assignment_id": assignment.assignment_id,
                        "title": assignment.title,
                        "description": assignment.description,
                        "total_score": str(assignment.total_score),
                        "status": assignment.status,
                        "questions": len(assignment.questions),
                    },
                },
                status=status.HTTP_201_CREATED,
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
                "CREATE ASSIGNMENT ERROR:",
                error,
            )

            return Response(
                {
                    "success": False,
                    "message": ("Không thể tạo bài tập."),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
