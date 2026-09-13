from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.class_sections.infrastructure.dependencies.class_section_dependency import (
    get_class_sections_use_case,
)

from apps.class_sections.presentation.serializers.class_section_serializer import (
    ClassSectionSerializer,
)


class GetClassSectionsView(APIView):

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
                        "message": ("Tài khoản chưa được " "liên kết với trường."),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            class_sections = get_class_sections_use_case.execute(
                university_id=university_id,
            )

            serializer = ClassSectionSerializer(
                class_sections,
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
                "GET CLASS SECTIONS ERROR:",
                str(error),
            )

            return Response(
                {
                    "success": False,
                    "message": ("Không thể lấy danh sách " "lớp học phần."),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
