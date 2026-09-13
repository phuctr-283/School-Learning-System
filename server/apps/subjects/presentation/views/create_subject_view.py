from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.subjects.infrastructure.dependencies.subject_dependency import (
    create_subject_use_case,
)
from apps.subjects.presentation.serializers.create_subject_serializer import (
    CreateSubjectSerializer,
)

from apps.subjects.presentation.serializers.subject_serializer import (
    SubjectSerializer,
)
from apps.subjects.application.dto.create_subject_dto import (
    CreateSubjectDTO,
)
class CreateSubjectView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):

        try:

            # =========================================
            # GET UNIVERSITY FROM AUTHENTICATED USER
            # =========================================

            university_id = getattr(
                request.user,
                "university_id",
                None,
            )

            if not university_id:

                return Response(
                    {
                        "success": False,
                        "message": (
                            "Tài khoản chưa được "
                            "liên kết với trường."
                        ),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # =========================================
            # VALIDATE REQUEST
            # =========================================

            serializer = CreateSubjectSerializer(
                data=request.data,
            )

            serializer.is_valid(
                raise_exception=True,
            )

            data = serializer.validated_data

            # =========================================
            # CREATE DTO
            # =========================================

            dto = CreateSubjectDTO(
                subject_id=data["subject_id"],
                name=data["name"],
                department_id=data["department_id"],
                subject_types=data["subject_types"],
                credits=data["credits"],
                process_percent=data["process_percent"],
                midterm_percent=data["midterm_percent"],
                final_percent=data["final_percent"],
            )

            # =========================================
            # CREATE SUBJECT
            # =========================================

            subject = create_subject_use_case.execute(
                data=dto,
                university_id=university_id,
            )

            # =========================================
            # RESPONSE
            # =========================================

            response_serializer = SubjectSerializer(
                subject,
            )

            return Response(
                {
                    "success": True,
                    "message": "Tạo môn học thành công.",
                    "data": response_serializer.data,
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
                "CREATE SUBJECT ERROR:",
                str(error),
            )

            return Response(
                {
                    "success": False,
                    "message": (
                        "Không thể tạo môn học."
                    ),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )