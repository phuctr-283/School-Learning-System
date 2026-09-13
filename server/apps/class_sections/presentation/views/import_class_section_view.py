from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated,
)

from rest_framework import status


from apps.class_sections.presentation.serializers.import_class_section_serializer import (
    ImportClassSectionSerializer,
)

from apps.class_sections.infrastructure.dependencies.class_section_dependency import (
    excel_class_section_import_service,
    import_class_sections_use_case,
)


class ImportClassSectionView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(
        self,
        request,
    ):

        try:

            # =================================================
            # UNIVERSITY FROM SCHOOL ADMIN
            # =================================================

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
                    status=(status.HTTP_400_BAD_REQUEST),
                )

            # =================================================
            # VALIDATE FILE
            # =================================================

            serializer = ImportClassSectionSerializer(
                data=request.data,
            )

            serializer.is_valid(
                raise_exception=True,
            )

            file = serializer.validated_data["file"]

            # =================================================
            # READ EXCEL
            # =================================================

            rows = excel_class_section_import_service.read(file)

            # =================================================
            # IMPORT
            #
            # PHASE 1
            # VALIDATE ALL
            #
            # PHASE 2
            # CREATE ALL
            # =================================================

            result = import_class_sections_use_case.execute(
                rows=rows,
                university_id=university_id,
            )

            return Response(
                {
                    "success": True,
                    "message": ("Import lớp học phần " "thành công."),
                    "data": {
                        "created_count": (result["created_count"]),
                        "skipped_count": (result["skipped_count"]),
                        "skipped_items": (result["skipped_items"]),
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
                "IMPORT CLASS SECTION ERROR:",
                str(error),
            )

            return Response(
                {
                    "success": False,
                    "message": ("Không thể import " "lớp học phần."),
                },
                status=(status.HTTP_500_INTERNAL_SERVER_ERROR),
            )
