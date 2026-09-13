from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.lessons.infrastructure.dependencies.subject_lesson_plan_dependency import (
    get_subject_lesson_plans_use_case,
)

from apps.lessons.presentation.serializers.subject_lesson_plan_serializer import (
    SubjectLessonPlanSerializer,
)


class GetSubjectLessonPlansView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        university_id = getattr(
            request.user,
            "university_id",
            None,
        )

        if not university_id:

            return Response(
                {
                    "success": False,
                    "message": "Tài khoản chưa được gán trường đại học.",
                },
                status=400,
            )

        use_case = get_subject_lesson_plans_use_case

        plans = use_case.execute(
            university_id=university_id,
        )

        serializer = SubjectLessonPlanSerializer(
            plans,
            many=True,
        )
        print(serializer.data)
        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=200,
        )