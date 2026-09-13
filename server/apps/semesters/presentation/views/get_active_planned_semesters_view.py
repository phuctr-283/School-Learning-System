from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.semesters.presentation.serializers.semester_content_reponse_serializer import (
    SemesterContentResponseSerializer,
)

from apps.semesters.infrastructure.dependencies.semester_dependency import (
    get_active_planned_semesters_dependency,
)


class GetActivePlannedSemestersView(APIView):

    def get(
        self,
        request,
    ):

        # =========================================
        # 1. LẤY UNIVERSITY TỪ USER ĐĂNG NHẬP
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
                        "Tài khoản không thuộc "
                        "trường đại học."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # =========================================
        # 2. LẤY USE CASE
        # =========================================

        use_case = (
            get_active_planned_semesters_dependency
        )

        # =========================================
        # 3. EXECUTE
        # =========================================

        semesters = use_case.execute(
            university_id=university_id,
        )

        # =========================================
        # 4. SERIALIZE
        # =========================================

        response_serializer = (
            SemesterContentResponseSerializer(
                semesters,
                many=True,
            )
        )

        # =========================================
        # 5. RESPONSE
        # =========================================

        return Response(
            {
                "success": True,
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )