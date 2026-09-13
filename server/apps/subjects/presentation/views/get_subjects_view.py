from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.subjects.infrastructure.dependencies.subject_dependency import (
    get_subjects_use_case,
)

from apps.subjects.presentation.serializers.subject_serializer import (
    SubjectSerializer,
)


class GetSubjectsView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        try:
            university_id = getattr(
                request.user,
                "university_id",
                None,
            )

            if not university_id:
                return Response(
                    {
                        "success": False,
                        "message": "Tài khoản chưa được liên kết với trường.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            subjects = get_subjects_use_case.execute(
                university_id=university_id,
            )

            serializer = SubjectSerializer(
                subjects,
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
                "GET SUBJECTS ERROR:",
                str(error),
            )

            return Response(
                {
                    "success": False,
                    "message": "Không thể lấy danh sách môn học.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )