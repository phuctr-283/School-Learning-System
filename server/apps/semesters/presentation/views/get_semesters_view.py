from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from apps.semesters.infrastructure.dependencies.semester_dependency import (
    get_semesters_use_case,
)


from apps.semesters.presentation.serializers.semester_serializer import (
    SemesterSerializer,
)


class GetSemestersView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    # =====================================================
    # GET
    # =====================================================

    def get(
        self,
        request,
    ):

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
                        "Tài khoản chưa được gán trường đại học"
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            semesters = (
                get_semesters_use_case
                .execute(
                    university_id=university_id,
                )
            )

            serializer = SemesterSerializer(
                semesters,
                many=True,
            )

            return Response(
                {
                    "success": True,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as error:

            print(
                "GET SEMESTERS ERROR:",
                str(error),
            )

            return Response(
                {
                    "success": False,
                    "message": (
                        "Không thể lấy danh sách học kỳ"
                    ),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )