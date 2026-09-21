from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from apps.lessons.application.dto.create_subject_lesson_plan_dto import (
    CreateSubjectLessonPlanDTO,
)

from apps.lessons.infrastructure.dependencies.subject_lesson_plan_dependency import (
    create_subject_lesson_plan_use_case,
)

from apps.lessons.presentation.serializers.create_subject_lesson_plan_serializer import (
    CreateSubjectLessonPlanSerializer,
)

from apps.lessons.presentation.serializers.subject_lesson_plan_serializer import (
    SubjectLessonPlanSerializer,
)


class CreateSubjectLessonPlanView(APIView):

    permission_classes = [IsAuthenticated,]

    def post(
        self,
        request,
    ):

        # =========================================
        # UNIVERSITY
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
                    "message": ("Tài khoản chưa được gán " "trường đại học."),
                },
                status=(status.HTTP_400_BAD_REQUEST),
            )

        # =========================================
        # VALIDATE REQUEST
        # =========================================

        serializer = CreateSubjectLessonPlanSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        # =========================================
        # CREATE DTO
        # =========================================

        dto = CreateSubjectLessonPlanDTO.from_dict(serializer.validated_data)

        # =========================================
        # USE CASE
        # =========================================

        try:

            plans = create_subject_lesson_plan_use_case.execute(
                dto=dto,
                university_id=university_id,
            )

            # =====================================
            # RESPONSE
            # =====================================

            response_serializer = SubjectLessonPlanSerializer(
                plans,
                many=True,
            )

            return Response(
                {
                    "success": True,
                    "message": ("Tạo quy tắc kế hoạch " "môn học thành công."),
                    "data": (response_serializer.data),
                },
                status=(status.HTTP_201_CREATED),
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=(status.HTTP_400_BAD_REQUEST),
            )

        except Exception as error:

            print(
                "CREATE SUBJECT LESSON PLAN ERROR:",
                str(error),
            )

            return Response(
                {
                    "success": False,
                    "message": ("Không thể tạo quy tắc " "kế hoạch môn học."),
                },
                status=(status.HTTP_500_INTERNAL_SERVER_ERROR),
            )
